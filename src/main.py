"""
Main script
"""

import yaml
from faker import Faker
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


def generate_data(rows: int) -> pd.DataFrame:
    """
    Generates a dataframe with first_name, last_name, email, random_value

    """

    fake = Faker("nl_NL")
    data = {
        "first_name": [fake.first_name() for _ in range(rows)],
        "last_name": [fake.last_name() for _ in range(rows)],
        "email": [fake.email() for _ in range(rows)],
        "random_value": [fake.paragraph(nb_sentences=5) for _ in range(rows)],
    }
    return pd.DataFrame(data=data)


import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import datetime


def create_connection(
    user: str, password: str, account: str, warehouse: str, role: str
):
    """Creates a Snowflake connection"""

    return snowflake.connector.connect(
        user=user, password=password, account=account, warehouse=warehouse, role=role
    )


def save_dataframe(connection, dataframe, table, database, schema):
    """
    Save a dataframe directly into Snowflake

    More information: https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api#write_pandas
    """

    return write_pandas(
        conn=connection,
        df=dataframe,
        table_name=table,
        database=database,
        schema=schema,
        quote_identifiers=False,
        use_logical_type=True,
    )


def main():
    """It all starts here"""

    with open("./config/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    df = generate_data(10000)
    conn = create_connection(
        config["user"],
        config["password"],
        config["account"],
        config["warehouse"],
        config["role"],
    )
    result = save_dataframe(conn, df, "hattam", "volfase", "waredax")
    print(result)


if __name__ == "__main__":
    main()
