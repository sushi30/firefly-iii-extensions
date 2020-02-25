import csv
import itertools


def write_csv(path, transactions):
    columns = list(set(itertools.chain(*[t.keys() for t in transactions])))
    with open(path, "w", newline="", encoding="utf8") as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=",", fieldnames=columns)
        writer.writeheader()
        writer.writerows(transactions)
