import json
import os
import subprocess
from typing import List

from pre_commit_hooks.utils.git import get_git_ignored_files, get_git_root_folders


class Control:
    image = ""
    command = []
    control_name = ""
    base_findings_path = "/tmp/controls/.pre_commit_findings"
    base_findings_path_raw = "/tmp/controls/.raw_pre_commit_findings"
    security_control_output_file = ""
    log_file = "/tmp/controls/jit-standalone-pre-commit.log"

    def __init__(self, base_path, changed_files: List[str]):
        self.base_path = base_path
        self.changed_files = changed_files

    @property
    def raw_findings_path(self) -> str:
        return f"{self.base_findings_path_raw}/{self.control_name}.json"

    @property
    def relevant_findings_path(self):
        return f"{self.base_findings_path}/{self.control_name}.json"

    @property
    def environment(self):
        env_vars = {
            "FINDINGS_OUTPUT_FILE_PATH": self.raw_findings_path,
        }
        if self.security_control_output_file:
            env_vars["SECURITY_CONTROL_OUTPUT_FILE"] = self.security_control_output_file
        return env_vars

    def read_raw_findings_file(self) -> List[dict]:
        f = json.loads(open(self.raw_findings_path, "r").read())
        return f

    def create_findings_dir(self) -> None:
        os.makedirs(self.base_findings_path_raw, exist_ok=True)
        os.makedirs(self.base_findings_path, exist_ok=True)

    @property
    def container_params(self) -> dict:
        ignored_files_volumes = [
            f"/dev/null:/code/{ignored_file}"
            for ignored_file in get_git_ignored_files(self.base_path)
        ]
        ignored_folders_volumes = [
            f"/code/{ignored_file}"
            for ignored_file in get_git_root_folders(self.base_path)
        ]
        return {
            "image": self.image,
            "command": self.command,
            "volumes": [
                f"{self.base_path.strip()}:/code",
                "/tmp/controls:/tmp/controls",
                *ignored_files_volumes,
                *ignored_folders_volumes,
            ],
            "environment": self.environment,
            "remove": True,
        }

    def parse_findings(self, findings):
        response = []
        for finding in findings:
            finding["filePath"] = os.path.join(self.base_path, finding["filename"])
            finding["filename"] = os.path.basename(finding["filePath"])
            response.append(finding)
        return response

    def get_relevant_findings(self) -> List[dict]:
        findings = self.read_raw_findings_file()
        findings = [f for f in findings if f["filename"] in self.changed_files]
        open(self.relevant_findings_path, "w").write(
            json.dumps(self.parse_findings(findings))
        )
        return findings

    def run_container(self) -> None:
        self.create_findings_dir()
        volumes_list = []
        for volume in self.container_params["volumes"]:
            volumes_list.extend(["-v", volume])
        env_list = []
        for k, v in self.container_params["environment"].items():
            env_list.extend(["-e", f"{k}={v}"])
        command = (
            ["docker", "run", "--rm"]
            + env_list
            + volumes_list
            + [self.image, *self.command]
        )
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        with open(self.log_file, "w") as f:
            f.write(
                f'Stdout: {stdout.decode("utf-8")}\nStderr{stderr.decode("utf-8")}\n'
            )
        print(f"Finished running {self.control_name}\n")
        print(f"If there is an error check the log file {self.log_file}")


class GitLeaks(Control):
    control_name = "gitleaks"
    image = "899025839375.dkr.ecr.us-east-1.amazonaws.com/jit-ide:jit-gitleaks-control"

    security_control_output_file = "/tmp/controls/report.json"
    command = [
        "--",
        "detect",
        "--config",
        "/config/gitleaks.toml",
        "--source",
        "/code",
        "-v",
        "--report-format",
        "json",
        "--report-path",
        "/tmp/controls/report.json",
        "--redact",
        "--no-git",
        "--exit-code",
        "0",
    ]


class Kics(Control):
    control_name = "kics"
    image = "899025839375.dkr.ecr.us-east-1.amazonaws.com/jit-ide:jit-kics-control"
    security_control_output_file = "/tmp/controls/kics/jit-report/results.json"
    command = [
        "--",
        "scan",
        "-p",
        "/code",
        "-o",
        "/tmp/controls/kics/jit-report",
        "-f",
        "json",
        "--exclude-severities",
        "INFO,MEDIUM,LOW",
        "--disable-secrets",
    ]
