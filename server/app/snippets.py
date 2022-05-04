from typing import List, Optional

setup_sh = """#!/usr/bin/env bash
apt-get install -y libxml2-dev libcurl4-openssl-dev libssl-dev
apt-get install -y r-base
{install_packages}
"""

install_one_package = """
Rscript -e "install.packages('{package_name}')\""""

grade_one_submission = """library(gradeR)
{r_markdown_snippet}
calcGradesForGradescope('{assignment_name}', 'run_tests.R')
"""

r_markdown = """knitr::purl('{assignment_name}')"""

run_autograder = """#!/usr/bin/env bash
cp /autograder/submission/{assignment_name} /autograder/source/{assignment_name}
cd /autograder/source
Rscript grade_one_submission.R
"""

run_tests = """library(testthat)
{setup_code}
{test_templates}
"""

test_template = """
test_that('{label} ({visibility})', {{
    expect_true({code})
}})"""


def make_setup_sh(package_names: Optional[List[str]]):
    """setup.sh"""
    install_packages = "Rscript -e \"install.packages('gradeR')\""
    if package_names:
        install_packages += "".join(install_one_package.format(
            package_name=package_name.strip()) for package_name in package_names)

    return setup_sh.format(install_packages=install_packages)


def make_grade_one_submission(assignment_name: str, is_r_markdown: bool):
    """grade_one_submission.R"""
    r_markdown_snippet = r_markdown.format(assignment_name=assignment_name) if is_r_markdown else ""
    return grade_one_submission.format(assignment_name=f"{assignment_name.split('.')[0]}.R", r_markdown_snippet=r_markdown_snippet)


def make_run_autograder(assignment_name: str):
    """make_autograder"""
    return run_autograder.format(assignment_name=assignment_name)


def make_run_tests(setup_code: str, labels: List[str], visibilities: List[str], codes: List[str]):
    """run_tests.R"""
    return run_tests.format(setup_code=setup_code, test_templates=make_test_snippet(labels=labels, visibilities=visibilities, codes=codes))


def make_test_snippet(labels: List[str], visibilities: List[str], codes: List[str]):
    return "".join(
        test_template.format(label=label, visibility=visibility, code=code) for label, visibility,
        code in zip(labels, visibilities, codes))
