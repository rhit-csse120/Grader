from Tester import Tester
from Repos import Repos


# term = "202520"
# term = "202530"
term = "project-202530"
NO_TERM = True

# project = "01-Introduction_to_Python_and_PyCharm"
# project = "02-Objects_Functions_and_Methods"
# project = "03-Loops_Summing_and_Unit_Testing"
# project = "04-Conditionals_and_The_Accumulator_Pattern"
# project = "05a-Debugging"
# project = "05b-Exam1_Practice"
# project = "07-Sequences"
# project = "09-Patterns_For_Sequences"
# NO_TERM = True
# project = "10-Patterns_For_Sequences_Revisited"
# project = "12-Exam2_Practice"
# project = "14-Exam1_Makeup"
# project = "15-Exam2"
project = "99z-Capstone_Team_Project-202530"


def main(no_term=NO_TERM):
    clone_and_or_pull_repos(no_term=NO_TERM)
    show_commit_data(no_term=no_term)
    # run_tests()


def clone_and_or_pull_repos(no_term=False):
    repos = Repos(project, term, no_term=NO_TERM)
    repos.clone_or_pull_repos()


def show_commit_data(no_term=False):
    repos = Repos(project, term, no_term=NO_TERM)
    repos.show_not_started_repos()
    repos.show_number_of_commits()


def run_tests(no_term=False):
    """Not yet completed."""
    repos = Repos(project, term, no_term=NO_TERM)
    tester = Tester(repos)
    tester.run_tests_on_all_students()


if __name__ == "__main__":
    main()
