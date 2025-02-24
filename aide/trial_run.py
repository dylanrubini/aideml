from pathlib import Path

import aide


def main():

    task_file = "rebound_basic_task.md"
    root_task_dir = Path("./example_tasks/")
    task_file = root_task_dir.joinpath(task_file).resolve()

    with open(task_file) as f:
        task_desc_str = f.read()

    exp = aide.Experiment(
        data_dir=None,  # replace this with your own directory
        goal=task_desc_str,  # replace with your own goal description
        eval="LLM_score",  # replace with your own evaluation metric
    )

    best_solution = exp.run(steps=10)

    print(f"Best solution has validation metric: {best_solution.valid_metric}")
    print(f"Best solution code: {best_solution.code}")


if __name__ == "__main__":
    main()
