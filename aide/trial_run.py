import aide


def main():
    exp = aide.Experiment(
        data_dir="example_tasks/bitcoin_price",  # replace this with your own directory
        goal="Build a time series forecasting model for bitcoin close price.",  # replace with your own goal description
        eval="RMSLE",  # replace with your own evaluation metric
    )

    best_solution = exp.run(steps=10)

    print(f"Best solution has validation metric: {best_solution.valid_metric}")
    print(f"Best solution code: {best_solution.code}")


if __name__ == "__main__":
    main()
