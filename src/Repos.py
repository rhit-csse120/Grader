from Repo import Repo
import os


class Repos:

    def __init__(self, project, term, no_term=False):
        self.project = project
        self.term = term

        self.repos_root = f"../repos-{self.term}"
        self.project_folder = f"{self.repos_root}/{self.project}"
        if not os.path.isdir(self.repos_root):
            os.makedirs(self.repos_root)
        if not os.path.isdir(self.project_folder):
            os.makedirs(self.project_folder)

        self.organization = "https://github.com/rhit-csse120"
        self.url = f"{self.organization}/{self.project}-{self.term}"
        self.url_without_term = f"{self.organization}/{self.project}"

        self.repo_name_for_importing = f"repos-{self.term}.{self.project}"
        self.repo_names_file = f"../data/repo_usernames-{term}.txt"
        self.repos = self.make_repos(no_term=no_term)

        self.home = None  # Set dynamically

    def make_repos(self, no_term=False):
        with open(self.repo_names_file) as f:
            names = f.readlines()
        repos = []
        for name in names:
            pair = name.split()
            repo = Repo(pair[0], pair[1], self, no_term=no_term)
            repos.append(repo)
        return repos

    def cd_to_project_folder(self):
        self.home = os.getcwd()
        os.chdir(self.project_folder)

    def cd_home(self):
        os.chdir(self.home)

    def clone_repos(self):
        print(f"\nCloning student repos for {self.project}-{self.term}:")
        self.cd_to_project_folder()
        for repo in self.repos:
            repo.clone()
        self.cd_home()

    def pull_repos(self):
        print(f"\nPulling student repos for {self.project}-{self.term}:")
        self.cd_to_project_folder()
        for repo in self.repos:
            repo.pull()
        self.cd_home()

    def clone_or_pull_repos(self):
        print(f"\nCloning/pulling student repos for {self.project}-{self.term}:")
        self.cd_to_project_folder()
        for repo in self.repos:
            if not repo.is_already_cloned():
                repo.clone()
            else:
                repo.pull()
        self.cd_home()

    def show_not_started_repos(self):
        print(f"\nStudents who have not started {self.project}-{self.term}:")
        self.cd_to_project_folder()
        for repo in self.repos:
            if not repo.is_already_cloned():
                print(repo.real_name)
        self.cd_home()

    def show_number_of_commits(self):
        print(f"\nNumber of commits by student of {self.project}-{self.term}:")
        self.cd_to_project_folder()
        for repo in self.repos:
            print("{:16} ".format(repo.real_name), end="")
            number_of_commits = repo.get_number_of_commits()
            if repo.is_already_cloned():
                if number_of_commits == 0:
                    print(" 0  NO COMMITS")
                else:
                    print("{:2}".format(number_of_commits))
            else:
                print("Not yet cloned")
        self.cd_home()
