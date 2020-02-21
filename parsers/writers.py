import csv


def write_csv(transactions):
    with open("names.csv", "w", newline="", encoding="utf8") as csvfile:
        writer = csv.DictWriter(
            csvfile, delimiter="\t", fieldnames=list(transactions[0].keys())
        )
        writer.writeheader()
        writer.writerows(transactions)
