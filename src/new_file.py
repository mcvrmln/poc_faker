""" functions for a new file """

from datetime import date, datetime, timedelta
from typing import Any

from faker import Faker


NUMBER_OF_ROWS = 10
FILE_NAME = "./data/input/testfile.txt"


def make_fixed_lenght_field(input: Any, length: int) -> str:
    if type(input) == str:
        output = input[:length].strip().ljust(length, " ")
    elif type(input) == int:
        output = str(input)[:length].strip().rjust(length, "0")
    elif type(input) == date:
        output = input.strftime("%Y%m%d")
    else:
        output = "NotImplemented"[:length].ljust(length, "-")

    return output


def make_header_record() -> str:

    fake = Faker("nl_NL")
    recordtype = "1"
    process_date = make_fixed_lenght_field(
        fake.date_between(date.today() - timedelta(days=14), date.today()), 8
    )
    dataset = make_fixed_lenght_field("FORESTWELL", 15)
    random_number = make_fixed_lenght_field(fake.random_number(), 20)

    return recordtype + process_date + dataset + random_number


def make_detail_record() -> str:
    fake = Faker("nl_NL")
    record_type = "2"
    customer_id = make_fixed_lenght_field(
        fake.random_number(digits=10, fix_len=True), 20
    )
    customer_name = make_fixed_lenght_field(fake.name(), 50)
    customer_email = make_fixed_lenght_field(fake.email(), 80)
    customer_city = make_fixed_lenght_field(fake.city(), 50)
    customer_country = make_fixed_lenght_field(fake.country(), 40)
    registration_date = make_fixed_lenght_field(
        fake.date_between(date(2012, 1, 1), date.today()), 8
    )

    return (
        record_type
        + customer_id
        + customer_name
        + customer_email
        + customer_city
        + customer_country
        + registration_date
    )


def make_footer_record() -> str:
    fake = Faker("nl_NL")
    record_type = "9"
    number_rows = make_fixed_lenght_field(NUMBER_OF_ROWS + 2, 10)
    random_number = make_fixed_lenght_field(fake.random_number(), 20)
    company = make_fixed_lenght_field(fake.company(), 25)
    close_sign = "."

    return record_type + number_rows + random_number + company + close_sign


def generate_file() -> None:
    """generates a file with 1 header, x detail records and 1 footer"""

    with open(FILE_NAME, "w") as file:
        file.write(make_header_record() + "\n")
        for _ in range(NUMBER_OF_ROWS):
            file.write(make_detail_record() + "\n")
        file.write(make_footer_record() + "\n")
    print(f"Job done: made {NUMBER_OF_ROWS} of detailrecords.")


if __name__ == "__main__":
    generate_file()
