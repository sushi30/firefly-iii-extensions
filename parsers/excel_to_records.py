import xlrd


def parse_rows(rows, it, categories):
    while True:
        try:
            row = next(it)
        except StopIteration:
            break
        rows.append({col_name: col.value for (col_name, col) in zip(categories, row)})


def leumicard_excel_to_records(file):
    rows = []
    wb = xlrd.open_workbook(file_contents=file.read())
    for i in range(wb.nsheets):
        it = iter(wb.sheet_by_index(i).get_rows())
        while True:
            try:
                row = next(it)
            except StopIteration:
                break
            if "כל המשתמשים" in row[0].value:
                continue
            if "כל הכרטיסים" in row[0].value:
                continue
            if "תאריך עסקה" in row[0].value:
                categories = [col.value for col in row]
                parse_rows(rows, it, categories)
    return rows
