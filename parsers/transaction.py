from datetime import datetime


class Transaction:
    def __init__(self, date, business, value, **kwargs):
        self.date = date
        self.business = business
        self.value = value
        self.other = kwargs
        self.normalize()

    def normalize(self):
        try:
            self.date = datetime.fromisoformat(self.date)
        except ValueError:
            try:
                self.date = datetime.strptime(self.date, "%d/%m/%Y")
            except:
                try:
                    self.date = datetime.strptime(self.date, "%d-%m-%Y")
                except:
                    print(self.to_dict())
                    raise

        self.value = float(self.value)

    def to_dict(self):
        return self.__dict__
