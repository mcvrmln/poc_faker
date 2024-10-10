""" Functions to extract the data """

from typing import Any
from faker import Faker
from datetime import date, datetime
import pydantic


INPUT_FILE = "./data/input/testfile.txt"


class InvalidRegistrationDateError(Exception):
    """Custom error that is raised when the registration date is invalid"""

    def __init__(self, value: date, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class Forestwell(pydantic.BaseModel):
    """Just a random name."""

    record_type: int
    customer_id: int
    customer_name: str
    customer_email: str
    customer_city: str
    customer_country: str
    registration_date: date

    @pydantic.field_validator("registration_date", mode="before")
    @classmethod
    def parse_registration_date(cls, value):
        return datetime.strptime(value, "%Y%m%d").date()

    @pydantic.field_validator("registration_date", mode="after")
    @classmethod
    def validate_registration_date(cls, value):
        if (value > date.today()) or (value < date(2014, 1, 1)):
            raise InvalidRegistrationDateError(
                value=value,
                message="Invalid registration date, must be between 1-1-2014 and today.",
            )
        return value


def read_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def main() -> None:
    dataset = None

    for line in read_file(INPUT_FILE):
        if line[0:1] == "1":
            header = {
                "record_type": line[0:1].strip(),
                "proces_date": line[1:9].strip(),
                "dataset": line[9:24].strip(),
                "random_number": line[24:44].strip(),
            }
            print(header)
        elif line[0:1] == "2":
            data = {
                "record_type": line[0:1].strip(),
                "customer_id": line[1:21].strip(),
                "customer_name": line[21:71].strip(),
                "customer_email": line[71:151].strip(),
                "customer_city": line[151:201].strip(),
                "customer_country": line[201:241].strip(),
                "registration_date": line[241:249].strip(),
            }
            try:
                data_forestwell = Forestwell(**data)
                # print(data_forestwell)
            except InvalidRegistrationDateError as e:
                # After an error: do this and continue with the next line
                print(e.message)
                print(line)
        elif line[0:1] == "9":
            footer = {
                "record_type": line[0:1].strip(),
                "number_rows": line[1:11].strip(),
                "random_number": line[11:31].strip(),
                "company": line[31:56].strip(),
                "close_sign": line[56:57].strip(),
            }
            print(footer)


if __name__ == "__main__":
    main()
