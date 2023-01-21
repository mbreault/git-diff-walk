import argparse
import os
import subprocess

def main():   
    parser = argparse.ArgumentParser(description='Check for changes in multiple local git repositories', prog='python main.py',epilog="example: python main.py '/home/git/' 'output.txt'")
    parser.add_argument('repo_root', type=str, help='The root directory of the repositories')
    parser.add_argument('output_file', type=str, help='The file to write the output to')
    args = parser.parse_args()

    with open(args.output_file, 'w') as f:
        for subdir, dirs, files in sorted(os.walk(args.repo_root)):
            for dir in sorted(dirs):
                if dir == ".git":
                    print(subdir, dir)
                    repo_path = os.path.join(subdir, dir)
                    repo_work_tree = os.path.dirname(repo_path)
                    git_status_output = subprocess.run(["git", "--git-dir="+repo_path,"--work-tree="+ repo_work_tree,"status"], capture_output=True, text=True)
                    if "Untracked files" in git_status_output.stdout or "Changes not staged for commit" in git_status_output.stdout:
                        f.write("Repo: " + repo_path + '\n')
                        f.write(git_status_output.stdout)

if __name__ == '__main__':
    main()