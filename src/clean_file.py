import gzip


def read_lines(file):
    with gzip.open(file, mode="rt") as f:
        for line in f:
            yield (line)


def clean_line(line, clean_indexes):
    replacement = " "  # single space!
    res = "".join(
        line[idx] if idx not in clean_indexes else replacement
        for idx in range(len(line))
    )
    return res


def main():
    with gzip.open("./data/output/file.txt.gz", "wt") as output:
        for line in read_lines("./data/input/file.txt.gz"):
            if line[0:1] == "1":
                # code to generate a list
                cleaned_line = line
            elif line[0:1] == "4":
                cleaned_line = clean_line(
                    line, [9, 10, 11, 15, 16, 17, 18, 19, 20, 25, 26, 27]
                )
            else:
                cleaned_line = line
            output.write(cleaned_line)

    with gzip.open("./data/output/file.txt.gz", "rt") as test:
        for record in test:
            print(record)


if __name__ == "__main__":
    main()
