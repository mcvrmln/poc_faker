"""
Main script
"""

from faker import Faker


def main():
    """It all starts here"""

    fake = Faker("nl_NL")
    for _ in range(100):
        print(fake.first_name(), fake.last_name(), fake.email())


if __name__ == "__main__":
    main()
