from Repo import Repo
import os


class Repos:

    def __init__(self, project, term):
        self.project = project
        self.term = term

        self.repos_root = f"../repos-{self.term}"
        self.repos_folder = f"{self.repos_root}/{self.project}"
        if not os.path.isdir(self.repos_root):
            os.makedirs(self.repos_root)
        if not os.path.isdir(self.repos_folder):
            os.makedirs(self.repos_folder)

        self.organization = "https://github.com/rhit-csse120"
        self.url = f"{self.organization}/{self.project}-{self.term}"

        self.repo_names_file = f"../data/repo_usernames-{term}.txt"
        self.repos = self.make_repos()

        self.home = None  # Set dynamically

    def make_repos(self):
        with open(self.repo_names_file) as f:
            names = f.readlines()
        repos = []
        for name in names:
            pair = name.split()
            repo = Repo(pair[0], pair[1], self)
            repos.append(repo)
        return repos

    def cd_to_repos_folder(self):
        self.home = os.getcwd()
        os.chdir(self.repos_folder)

    def cd_home(self):
        os.chdir(self.home)

    def clone_repos(self):
        print(f"\nCloning student repos for {self.project}-{self.term}:")
        self.cd_to_repos_folder()
        for repo in self.repos:
            repo.clone()
        self.cd_home()

    def pull_repos(self):
        print(f"\nPulling student repos for {self.project}-{self.term}:")
        self.cd_to_repos_folder()
        for repo in self.repos:
            repo.pull()
        self.cd_home()

    def show_not_started_repos(self):
        print(f"\nStudents who have not started {self.project}-{self.term}:")
        self.cd_to_repos_folder()
        for repo in self.repos:
            if not repo.is_already_cloned():
                print(repo.real_name)
        self.cd_home()

    def show_number_of_commits(self):
        print(f"\nNumber of commits by student of {self.project}-{self.term}:")
        self.cd_to_repos_folder()
        for repo in self.repos:
            print("{:16} ".format(repo.real_name), end="")
            if repo.is_already_cloned():
                print("{:2}".format(repo.number_of_commits()))
            else:
                print("Not yet cloned")
        self.cd_home()

    # def get_cloned_repos(self):
    #     cloned_repos = []
    #     for repo in self.repos:
    #         if not repo.is_not_started():
    #             cloned_repos.append(repo)
    #     return cloned_repos
