import argparse
import os
import sys
import hashlib
print()# from pre_commit_hooks.utils.controls import GitLeaks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(sys.argv)

    # md5 working directory
    # cryptography.md5(os.getcwd())
    cwd = os.getcwd()
    print(cwd)

    # md5 hex digest cwd
    cwd_hash = hashlib.md5(cwd.encode('utf-8')).hexdigest()
    print(cwd_hash)

    # c = GitLeaks(os.getcwd(), args.filenames)
    # c.run_container()
    # findings = c.get_relevant_findings()
    # if findings:
    #     exit(1)
    exit(0)


if __name__ == "__main__":
    main()