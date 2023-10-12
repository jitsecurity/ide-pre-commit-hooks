import argparse
import os
import sys

from pre_commit_hooks.utils.controls import Kics
from pre_commit_hooks.utils.report import print_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(sys.argv)

    c = Kics(os.getcwd(), args.filenames)
    c.run_container()
    findings = c.get_relevant_findings()
    if findings:
        print_report(findings, "Infrastructure as Code")
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()
