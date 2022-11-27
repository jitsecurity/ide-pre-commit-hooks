import json
import argparse
import os
import sys
import hashlib


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
    print("GUYYYYY2")

    # create a file with the hash
    with open(cwd_hash, 'w') as f:
        f.write(cwd_hash)

    # read json file /tmp/controls/.precommit/ + cwd_hash + .state.json
    with open('/tmp/controls/.precommit/' + cwd_hash + '.state.json', 'r') as json_file:
        state = json.load(json_file)

    # c = GitLeaks(os.getcwd(), args.filenames)
    # c.run_container()
    # findings = c.get_relevant_findings()
    findings = state.get('findings', [])
    if findings:
        print(f"Found {len(findings)} findings")
        exit(1)
    
    print(f"Found {len(findings)} findings")
    # exit(0)
    exit(1)


if __name__ == "__main__":
    main()