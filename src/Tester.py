import importlib.util
import os
import sys
from Repos import Repos


class Tester:
    def __init__(self, project, term):
        self.repos = Repos(project, term)
        # self.solution_folder

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
                    failed += self.run_tests_on_student(repo, module)
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
        # return ["m4_calling_functions_returning_values"]  # Stub
        return ["m9_summary"]

    def run_tests_on_student(self, repo, module):
        code_to_test = self.get_code_to_test(repo, module)
        testing_code = self.get_testing_code()
        return testing_code.run_tests(code_to_test)

    def get_code_to_test(self, repo, module):
        sys.path.insert(0, repo.repo_source_folder)
        f = importlib.import_module(
            f"{repo.repo_name_for_importing}.{module}")
        sys.path.pop(0)
        return f

    def get_testing_code(self, repo, module):
        sys.path.insert(0, repo.source_folder)
        f = importlib.import_module(repo.repo_relative + module)
        sys.path.pop(0)
        return f

    def run_tests(self, module):
        return 0

    def has_all_prerequistes(self):
        return True  # Stub
