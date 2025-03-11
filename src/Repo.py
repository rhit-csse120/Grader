import os
import subprocess


class Repo:
    def __init__(self, repo_username, real_name, parent):
        self.repo_username = repo_username
        self.real_name = real_name
        self.parent = parent

        self.repo_folder = f"{self.real_name}"
        self.repo_source_folder = f"{self.real_name}/src"
        self.url = f"{self.parent.url}-{self.repo_username}"
        self.repo_name_for_importing = \
            f"{parent.repo_name_for_importing}.{self.real_name}.src"

        # self.repo_relative = self.repo_folder.replace(
        #     "../", "").replace(
        #     "/", ".")
        # print(self.repo_relative)

    def clone(self):
        print("\nCloning " + self.repo_username + " for " + self.real_name)
        if self.is_already_cloned():
            print("NOT cloned: already exists")
        else:
            try:
                subprocess.run(["git", "clone", self.url, self.repo_folder], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                if os.path.isdir(self.repo_folder):
                    subprocess.run(["rm", "-rf", self.repo_folder], check=True)

    def pull(self):
        print("\nPulling " + self.repo_username + " for " + self.real_name)
        if self.is_already_cloned():
            os.chdir(self.repo_folder)
            try:
                subprocess.run(["git", "pull"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
            os.chdir("..")
        else:
            print("NOT pulled: repo does not yet exist")

    def is_already_cloned(self):
        return os.path.isdir(self.repo_folder)

    def number_of_commits(self):
        if self.is_already_cloned():
            os.chdir(self.repo_folder)
            try:
                result = subprocess.run(
                    ["git", "rev-list", "--count", "--all"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                result = 0
                print(f"Error: {e}")
            os.chdir("..")
            # Don't count the initial commit of starting code
            return int(result.stdout) - 1
        else:
            return -1
