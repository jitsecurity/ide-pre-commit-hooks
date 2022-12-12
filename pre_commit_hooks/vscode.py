import json
import os
import hashlib


def filter_findings(findings, configuration):
    return list(filter(lambda finding: finding["controlName"] not in configuration, findings))


def main():
    cwd = os.getcwd()
    cwd_hash = hashlib.md5(cwd.encode("utf-8")).hexdigest()
    with open("/tmp/controls/.precommit/" + cwd_hash + ".state.json", "r") as json_file:
        state = json.load(json_file)
        findings = state.get("findings", [])
        configuration = state.get("configuration", [])
        if configuration:
            print(f"Before filter {len(findings)} findings")
            findings = filter_findings(findings, configuration)
            print(f"Before filter {len(findings)} findings")

    print(f"Found {len(findings)} findings")
    if findings:
        exit(1)

    exit(0)


if __name__ == "__main__":
    main()
