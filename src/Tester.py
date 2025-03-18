import importlib.util
import sys
import os
from Repos import Repos
from Repo import Repo


class Tester:
    def __init__(self, project, term):
        self.repos = Repos(project, term)
        self.solution_username = "TESTER"
        self.solution_realname = "TESTER"
        self.solution_project = f"{project}-{self.solution_username}"
        self.solution_repo = Repo(
            self.solution_username, self.solution_realname, self.repos
        )

    def run_tests_on_all_students(self):
        if not self.has_all_prerequistes():
            print("Missing prerequisites.  Nothing done.")
            return
        modules = self.get_modules()

        print("\nRunning tests on all students and all modules in")
        print(f"{self.repos.project} for {self.repos.term}")

        self.repos.cd_to_repos_folder()
        for repo in self.repos.repos:
            print(f"\n{repo.real_name}:", end="")
            if repo.is_already_cloned():
                print()
                failed = 0
                for module in modules:
                    print(f"  {module}: ", end="")
                    tests_failed = self.run_tests_on_student(repo, module)
                    print(f"{tests_failed} failed tests")
                    failed += tests_failed
                print(f"  SUMMARY over all modules: ", end="")
                if failed == 0:
                    print(" PASSED ALL TESTS")
                elif failed == 1:
                    print(f" FAILED 1 test")
                else:
                    print(f" FAILED {failed} tests")
            else:
                print(" has NOT CLONED the project")
        self.repos.cd_home()

    def get_modules(self):
        return ["m4_calling_functions_returning_values"]

    def run_tests_on_student(self, repo, module):
        module_to_test = self.get_code_to_test(repo, module)
        if not module_to_test:
            return None
        testing_module = self.get_testing_code(module)
        return testing_module.run_tests(module_to_test)

    def get_code_to_test(self, repo, module):
        sys.path.insert(0, repo.repo_source_folder)
        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        try:
            f = importlib.import_module(f"{repo.repo_name_for_importing}.{module}")
        except Exception as e:
            print(e)
            f = None
        sys.stdout = stdout
        sys.stderr = stderr
        sys.path.pop(0)
        return f

    def get_testing_code(self, module):
        sys.path.insert(0, self.solution_repo.repo_source_folder)
        f = importlib.import_module(
            f"{self.solution_repo.repo_name_for_importing}.{module}"
        )
        sys.path.pop(0)
        return f

    def has_all_prerequistes(self):
        return True  # Stub
