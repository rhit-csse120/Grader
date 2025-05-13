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
PASSES_TEST = "blue"
IS_OK = "green"

# Settings to use when running the tests.
KEEP_OUTPUT_ON = False  # True if you want to see student output


class Tester:
    """
    Tester for a single project, including all relevant modules,
    for a collection of students.
    """

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
        self.repos.cd_to_project_folder()
        for repo in self.repos.repos:
            print(f"\nTesting {repo.real_name}:", end="")
            if not self.check_project_is_cloned(repo):
                continue  # to the next student
            else:
                print()

            # Loop through the modules, for the current student:
            for module in modules:
                print(f"  Doing {module}:", end="")
                f = self.load_module_to_test(repo, module)
                if f:
                    results = self.run_tests_on_student_for_module(repo, module, f)
                self.print_results_of_tests_on_module(results)
        self.repos.cd_home()

    def print_test_header(self):
        print("\nRunning tests on all students and all relevant modules in: ", end="")
        ph.print_colored(f"{self.repos.project}", color=IS_OK, end="")
        print(" for ", end="")
        ph.print_colored(f"{self.repos.term}", color=IS_OK)
        return True

    def check_has_all_prerequistes(self, stub=True):
        # Stub, FIXME
        if stub:
            return True
        else:
            ph.print_error("Missing prerequisites.  Nothing done.")
            return False

    def load_module_to_test(self, repo, module):
        if not self.check_student_has_module(repo, module):
            return False

        sys.path.insert(0, repo.repo_source_folder)
        if not KEEP_OUTPUT_ON:
            saved_stdout, saved_stderr = Tester.turn_off_output()
        try:
            f = importlib.import_module(f"{repo.repo_name_for_importing}.{module}")
        except Exception as e:
            if not KEEP_OUTPUT_ON:
                sys.stdout, sys.stderr = saved_stdout, saved_stderr
            ph.print_colored(" Could not load module.", color=DOES_NOT_LOAD)
            # print(e)
            return False
        else:
            return f
        finally:
            if not KEEP_OUTPUT_ON:
                sys.stdout, sys.stderr = saved_stdout, saved_stderr
            sys.path.pop(0)

    def run_tests_on_student_for_module(self, repo, module, f):
        # STUB:
        testing_module = self.get_testing_code(module)
        return [FunctionTestingResult()]
        # testing_module.run_tests(module_to_test)

    @staticmethod
    def turn_off_output():
        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        return saved_stdout, saved_stderr

    def get_testing_code(self, module):
        sys.path.insert(0, self.tester_repo.repo_source_folder)
        f = importlib.import_module(
            f"{self.tester_repo.repo_name_for_importing}.{module}"
        )
        sys.path.pop(0)
        return f

    def print_results_of_tests_on_module(self, results):
        if not results:
            return
        all_passed = True
        for result in results:
            if result.failed_tests():
                all_passed = False
                break
        if all_passed:
            ph.print_colored(" PASSED all tests.", color=PASSES_TEST)
        else:
            ph.print_colored(" FAILED some tests!", color=FAILS_TEST)

    def check_project_is_cloned(self, repo):
        if not repo.is_already_cloned():
            ph.print_colored("  NOT YET CLONED", color=IS_NOT_CLONED)
            return False
        else:
            return True

    def check_student_has_module(self, repo: Repo, module):
        pathname = repo.repo_source_folder
        pathname += "/" + module
        pathname += ".py"
        path = pathlib.Path(pathname)
        if not path.is_file():
            ph.print_colored(" Student has no such module.", color=DOES_NOT_EXIST)
            return False
        else:
            return True

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


class ModuleTestingResult:
    def __init__(self):
        self.functions_that_failed_tests = 0


class FunctionTestingResult:
    def __init__(self):
        pass

    def failed_tests(self):
        return False
