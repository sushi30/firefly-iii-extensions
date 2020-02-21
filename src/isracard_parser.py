import xlrd


class IsraCardParser(Parser):
    def __init__(self, file_):
        super().__init__()
        self.file = file_
        self.domestic_rows = []
        self.international_rows = []
        self.wb = None

    def parse(self):
        self.wb = xlrd.open_workbook(file_contents=self.file.read())
        self.it = iter(self.wb.sheet_by_index(0).get_rows())
        while True:
            try:
                row = next(self.it)
            except StopIteration:
                break
            if len(row) < 2:
                continue
            if "עסקאות בארץ" in row[0].value:
                row = next(self.it)
                self.categories = [col.value for col in row]
                self.parse_domestic_rows()
            if "עסקאות בחו˝ל" in row[0].value:
                row = next(self.it)
                self.categories = [col.value for col in row]
                self.parse_international_rows()

        self.parse_domestic_transactions()
        self.parse_international_transactions()
        return self

    def parse_domestic_transactions(self):
        columns_dictionary = {
            "תאריך רכישה": "date",
            "שם בית עסק": "business",
            "סכום עסקה": "value",
            "מטבע מקור": "original_currency",
            "סכום חיוב": "payment",
            "מטבע לחיוב": "payment_currency",
            "מספר שובר": "confirmation_no",
            "פירוט נוסף": "comments",
        }
        for row in self.domestic_rows:
            kwargs = {columns_dictionary.get(k, k): v for k, v in row.items()}
            self.transactions.append(Transaction(**kwargs))

    def parse_international_transactions(self):
        columns_dictionary = {
            "תאריך רכישה": "date",
            "שם בית עסק": "business",
            "סכום חיוב": "value",
            "סכום מקורי": "original_value",
            "מטבע מקור": "original_currency",
            "מטבע לחיוב": "value_currency",
            "תאריך חיוב": "payment_date",
        }
        for row in self.international_rows:
            kwargs = {columns_dictionary.get(k, k): v for k, v in row.items()}
            if kwargs["business"] != "TOTAL FOR DATE":
                self.transactions.append(Transaction(**kwargs))

    def parse_domestic_rows(self):
        while True:
            try:
                row = next(self.it)
            except StopIteration:
                break
            str_values = [str(cell.value) for cell in row]
            cells_with_content = len([cell for cell in str_values if len(cell) > 0])
            if cells_with_content < 6:
                break
            self.domestic_rows.append(
                {col_name: col.value for (col_name, col) in zip(self.categories, row)}
            )

    def parse_international_rows(self):
        while True:
            try:
                row = next(self.it)
            except StopIteration:
                break
            str_values = [str(cell.value) for cell in row]
            cells_with_content = len([cell for cell in str_values if len(cell) > 0])
            if cells_with_content < 4:
                break
            self.international_rows.append(
                {col_name: col.value for (col_name, col) in zip(self.categories, row)}
            )
