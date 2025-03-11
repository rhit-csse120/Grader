from Repos import Repos
from Tester import Tester


def main():
    # project = "03-Loops_Summing_and_Unit_Testing"
    # term = "202520"
    project = "01-Introduction_to_Python_and_PyCharm"
    term = "202530"
    repos = Repos(project, term)
    # repos.clone_repos()
    # repos.pull_repos()
    repos.show_not_started_repos()
    repos.show_number_of_commits()

    # tester = Tester(project, term)
    # tester.run_tests_on_all_students()


main()
