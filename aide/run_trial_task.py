import importlib.metadata
import os
import subprocess
from pathlib import Path

import git

import aide

# Check version of a specific package
package_name = "pip"
version = importlib.metadata.version(package_name)


def main():

    repo_url = "https://github.com/pybamm-team/PyBaMM.git"
    tag_name = "25.1.1"

    # task_file = "rebound_basic_task.md"
    task_file = "pybamm_soh_task.md"
    data_dir = "./example_tasks/pybamm_soh/"
    root_task_dir = Path("./example_tasks/")
    task_file = root_task_dir.joinpath(task_file).resolve()
    repo_dir = Path(data_dir).joinpath("repo/")
    repo_working_dir = repo_dir.joinpath("examples/")

    # Read task description
    with open(task_file) as f:
        task_desc_str = f.read()

    paper_file = Path("./pybamm_soh/paper.md")
    paper_file = root_task_dir.joinpath(paper_file).resolve()

    # Read content of journal publication
    with open(paper_file) as f:
        paper_content = f.read()

    if not repo_dir.exists():

        repo_dir.mkdir(parents=True, exist_ok=True)

        # Pull in repo from Github
        repo = git.Repo.clone_from(repo_url, repo_dir)
        repo.remote().fetch()
        repo.git.checkout(f"v{tag_name}")

    try:
        installed_version = importlib.metadata.version("pybamm")
        if installed_version == tag_name:
            print(f"✅ PyBaMM version is correct: {installed_version}")
        else:
            print(
                f"⚠️ PyBaMM version mismatch: Installed={installed_version}, Expected={tag_name}"
            )
            raise ImportError

    except importlib.metadata.PackageNotFoundError:
        print(f"❌ PyBaMM is not installed.")
        raise

    exp = aide.Experiment(
        data_dir=None,  # replace this with your own directory
        repo_dir=repo_dir.resolve(),
        repo_working_dir=repo_working_dir.resolve(),
        goal=task_desc_str,  # replace with your own goal description
        paper_content=paper_content,
        eval="An LLM agent will be used to provide an evaluation score between 0.0 and 1.0 to assess how realistic the results provided are. Higher is assumed to be better.",  # replace with your own evaluation metric
    )

    best_solution = exp.run(steps=20)

    print(f"Best solution has validation metric: {best_solution.valid_metric}")
    print(f"Best solution code: {best_solution.code}")


if __name__ == "__main__":
    main()
