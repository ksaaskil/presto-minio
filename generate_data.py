from os import write
from pathlib import Path

import numpy as np
import pandas as pd

MINIO_DATA = Path("minio").joinpath("data")

PARQUET_DATA = MINIO_DATA.joinpath("parquet")

CSV = Path(MINIO_DATA).joinpath("customer-data-text").joinpath("customer.csv")


def write_parquet(df):
    PARQUET_DATA.mkdir(exist_ok=True, parents=True)
    target_file = PARQUET_DATA.joinpath("test.parquet")

    print(f"Writing to: {target_file}")

    df.to_parquet(str(target_file))


def make_df():
    arr = np.random.randn(5000)
    arr[::10] = np.nan  # 10% nulls
    return pd.DataFrame({"column_{0}".format(i): arr for i in range(10)})


def read_df():
    df = pd.read_csv(CSV, header=None, names=["id", "fname", "lname"])
    return df


def main():
    df = read_df()
    write_parquet(df)


if __name__ == "__main__":
    main()
