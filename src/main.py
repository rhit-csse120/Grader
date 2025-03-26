from Tester import Tester
from Repos import Repos


# term = "202520"
term = "202530"

# project = "01-Introduction_to_Python_and_PyCharm"
# project = "02-Objects_Functions_and_Methods"
# project = "03-Loops_Summing_and_Unit_Testing"
# project = "04-Conditionals_and_The_Accumulator_Pattern"
# project = "05a-Debugging"
# project = "05b-Exam1_Practice"
# project = "07-Sequences"
# project = "08-Exam1"
# project = "09-Patterns_For_Sequences"


def main():
    clone_and_or_pull_repos()
    show_commit_data()
    # run_tests()


def clone_and_or_pull_repos():
    repos = Repos(project, term)
    repos.clone_repos()
    repos.pull_repos()


def show_commit_data():
    repos = Repos(project, term)
    repos.show_not_started_repos()
    repos.show_number_of_commits()


def run_tests():
    """Not yet completed."""
    tester = Tester(project, term)
    tester.run_tests_on_all_students()


if __name__ == "__main__":
    main()
