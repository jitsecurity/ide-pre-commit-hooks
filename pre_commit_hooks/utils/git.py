import os


def get_git_root_folders(git_repo_folder: str) -> list:
    gitignore_file = os.path.join(git_repo_folder, ".gitignore")
    with open(gitignore_file, "r") as f:
        ignored_files = f.read().splitlines()
    ignored_folders = []
    for ignored_file in ignored_files:
        if os.path.isdir(os.path.join(git_repo_folder, ignored_file)):
            ignored_folders.append(ignored_file)
    return ignored_folders


def get_git_ignored_files(git_repo_folder: str) -> list:
    gitignore_file = os.path.join(git_repo_folder, ".gitignore")
    with open(gitignore_file, "r") as f:
        ignored_files = f.read().splitlines()
    ignored_files = [
        file
        for file in ignored_files
        if os.path.isfile(os.path.join(git_repo_folder, file))
    ]
    return ignored_files
