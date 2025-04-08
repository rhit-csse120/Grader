import importlib.util
import sys
import os
import pathlib

import print_helper as ph
from Repo import Repo

# Various constants:
PROJECTS_AND_MODULES = "../data/project_modules"

# Colors to use for output when running the tests:
IS_NOT_CLONED = "magenta"
DOES_NOT_EXIST = "yellow"
DOES_NOT_LOAD = "yellow"
DOES_NOT_RUN = "yellow"
DOES_NOT_FINISH = "cyan"
FAILS_TEST = "red"
IS_OK = "green"

# Settings to use when running the tests.
KEEP_OUTPUT_ON = False  # True if you want to see student output


class Tester:
    def __init__(self, repos, keep_output_on=KEEP_OUTPUT_ON):
        self.repos = repos
        self.tester_repo = Repo("TESTER", "TESTER", self.repos)
        self.projects_and_modules = self._get_modules_for_projects()

    def run_tests_on_all_students(self):
        if not self.check_has_all_prerequistes():
            return

        self.print_test_header()
        modules = self.projects_and_modules[self.repos.project]

        # Loop through the students:
        for repo in self.repos.repos:
            print(f"\nTesting {repo.real_name}:", end="")
            if not self.check_project_is_cloned(repo):
                continue  # to the next student

            modules_passed = 0
            # Loop through the modules, for the current student:
            for module in modules:
                print(f"  Doing {module}:", end="")
                result = self.run_tests_on_student_for_module(repo, module)
                modules_passed = modules_passed + result
            self.print_student_summary(modules_passed, len(modules))
        #             print(f"{tests_failed} failed tests")
        #             failed += tests_failed
        #         print(f"  SUMMARY over all modules: ", end="")
        #         if failed == 0:
        #             print("PASSED ALL TESTS")
        #         elif failed == 1:
        #             print(f"FAILED 1 test")
        #         else:
        #             print(f" FAILED {failed} tests")
        #     else:
        #         ph.print_colored("has NOT CLONED the project", color=NOT_CLONED)

    def print_test_header(self):
        print("\nRunning tests on all students and all relevant modules in")
        ph.print_colored(f"{self.repos.project}", color=IS_OK, end="")
        print(" for ", end="")
        ph.print_colored(f"{self.repos.term}", color=IS_OK)
        return True

    def check_has_all_prerequistes(self):
        return True  # Stub, FIXME
        # ph.print_error("Missing prerequisites.  Nothing done.")

    def run_tests_on_student_for_module(self, repo, module):
        if not self.check_student_has_module(repo, module):
            return

        module_to_test = self.get_code_to_test(repo, module)
        if not module_to_test:
            return
        testing_module = self.get_testing_code(module)
        return self.run_tests_on_student(repo, module)

        # Continue to the next student
        pass

    def get_modules_to_test_for_project(self):

        return ["m4_calling_functions_returning_values"]  # Stub

    def run_tests_on_student(self, repo, module):
        module_to_test = self.get_code_to_test(repo, module)
        if not module_to_test:
            return None
        if not testing_module:
            ph.print_error("Could not find the testing module")
            sys.exit(1)
        return 1  # testing_module.run_tests(module_to_test)

    def get_code_to_test(self, repo, module):
        sys.path.insert(0, repo.repo_source_folder)
        # stdout, stderr = Tester.turn_off_output()
        try:
            f = importlib.import_module(f"{repo.repo_name_for_importing}.{module}")
        except Exception as e:
            print("\n", e)
            raise TestingException

        # sys.stdout, sys.stderr = stdout, stderr
        sys.path.pop(0)
        return f

    @staticmethod
    def turn_off_output():
        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        return stdout, stderr

    def get_testing_code(self, module):
        sys.path.insert(0, self.solution_repo.repo_source_folder)
        f = importlib.import_module(
            f"{self.solution_repo.repo_name_for_importing}.{module}"
        )
        sys.path.pop(0)
        return f

    def check_project_is_cloned(self, repo):
        if not repo.is_already_cloned():
            ph.print_colored(" PROJECT IS NOT YET CLONED", color=IS_NOT_CLONED)
            raise TestingException("Not yet cloned")

    def check_student_has_module(self, repo: Repo, module):
        pathname = repo.repo_source_folder
        pathname += "/" + module
        pathname += ".py"
        path = pathlib.Path(pathname)
        if not path.is_file():
            ph.print_colored(" Student has no such module.", color=DOES_NOT_EXIST)
            raise TestingException("Has no such module")

    def _get_modules_for_projects(self):
        filename = PROJECTS_AND_MODULES + "-" + self.repos.term + ".txt"
        with open(filename, "r") as f:
            lines = f.read().split("\n")
        project_modules = {}
        project = lines[0]  # First line must be a project
        project_modules[project] = []
        for line in lines:
            if line.strip() == "":
                continue  # Skip blank lines
            if line.startswith(" "):
                project_modules[project].append(line.strip())
            else:
                project = line
                project_modules[project] = []
        return project_modules


class TestingException(Exception):
    pass


if __name__ == "__main__":
    tester = Tester("04-Conditionals_and_The_Accumulator_Pattern", "202530")
