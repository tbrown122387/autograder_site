from typing import List


setup_sh = """#!/usr/bin/env bash
apt-get install -y libxml2-dev libcurl4-openssl-dev libssl-dev
apt-get install -y r-base
{install_packages}
"""

install_one_package = """
Rscript -e "install.packages({package_name})\""""

grade_one_submission = """library(gradeR)
calcGradesForGradescope('{assignment_name}', 'run_tests.R')
"""

run_autograder = """#!/usr/bin/env bash
cp /autograder/submission/{assignment_name} /autograder/source/{assignment_name}
cd /autograder/source
Rscript grade_one_submission.R
"""

run_tests = """library(testthat)
{test_templates}
"""

test_template = """
test_that('{label} ({visibility})' {{
    expect_true({code})
}})"""


def make_setup_sh(package_names: List[str]):
    """setup.sh"""
    if package_names:
        install_packages = "".join(install_one_package.format(
            package_name=package_name) for package_name in package_names)
    else:
        install_packages = ""

    return setup_sh.format(install_packages=install_packages)


def make_grade_one_submission(assignment_name: str):
    """grade_one_submission.R"""
    return grade_one_submission.format(assignment_name=assignment_name)


def make_run_autograder(assignment_name: str):
    """make_autograder"""
    return run_autograder.format(assignment_name=assignment_name)


def make_run_tests(labels: List[str], visibilities: List[str], codes: List[str]):
    """run_tests.R"""
    return run_tests.format(test_templates=make_test_snippet(labels=labels, visibilities=visibilities, codes=codes))


def make_test_snippet(labels: List[str], visibilities: List[str], codes: List[str]):
    return "".join(test_template.format(label=label, visibility=visibility, code=code) for label, visibility, code in zip(labels, visibilities, codes))


if __name__ == "__main__":
    labels = [
        "Q1",
        "Q2",
        "Q3"
    ]

    visibilities = [
        "visible",
        "after_duedate",
        "visible",
    ]

    codes = [
        "length(x) == 3",
        "sum(x) == 10",
        ""
    ]

    package_names = ['MASS', 'survival']
    print(make_setup_sh(package_names))

    assignment_name = "assignment01.R"
    print(make_run_autograder(assignment_name))

    print(make_grade_one_submission(assignment_name))

    print(make_run_tests(labels, visibilities, codes))
