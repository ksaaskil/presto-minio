from pyarrow import parquet as pq, fs

MINIO_ACCESS_KEY = "V42FCGRVMK24JJ8DHUYG"
MINIO_SECRET_KEY = "bKhWxVF3kQoLY9kFmt91l+tDrEoZjqnWXzY9Eza"


def read():
    minio = fs.S3FileSystem(
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        scheme="http",
        endpoint_override="localhost:9000",
    )

    file_info = minio.get_file_info(fs.FileSelector("parquet", recursive=True))

    print(f"Found files: {', '.join([info.path for info in file_info])}")

    PARQUET_FILE = "parquet/test.parquet"
    table = pq.read_table(PARQUET_FILE, filesystem=minio)

    df = table.to_pandas()

    print("Read Pandas DataFrame:")
    print(df)


if __name__ == "__main__":
    read()
