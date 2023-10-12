import argparse
import os
import sys

from pre_commit_hooks.utils.controls import GitLeaks
from pre_commit_hooks.utils.report import print_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(sys.argv)

    c = GitLeaks(os.getcwd(), args.filenames)
    c.run_container()
    findings = c.get_relevant_findings()
    if findings:
        print_report(findings, "Secrets")
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()
