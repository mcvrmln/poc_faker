import duckdb


def main():
    results = duckdb.sql(
        "SELECT * FROM read_csv('data/output/cdf1b7e8-508d-49a6-9f14-0f8d37fd22a1.csv') LIMIT 100"
    ).fetchall()
    print(results)


if __name__ == "__main__":
    main()
