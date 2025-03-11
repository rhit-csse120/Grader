from Tester import Tester
from Repos import Repos


def main():
    # clone_and_or_pull_repos()
    show_commit_data()
    # run_tests()


def clone_and_or_pull_repos():
    project = "01-Introduction_to_Python_and_PyCharm"
    term = "202530"
    repos = Repos(project, term)
    repos.clone_repos()
    repos.pull_repos()


def show_commit_data():
    project = "01-Introduction_to_Python_and_PyCharm"
    term = "202530"
    repos = Repos(project, term)
    repos.show_not_started_repos()
    repos.show_number_of_commits()


def run_tests():
    """ Not yet completed. """
    project = "01-Introduction_to_Python_and_PyCharm"
    term = "202530"
    tester = Tester(project, term)
    tester.run_tests_on_all_students()


main()
