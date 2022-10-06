from datetime import datetime


class DateValidator:
    def validate(self, date):
        if self.check_format_dmy(date):
            return self.check_format_dmy(date)
        if self.check_format_dmY(date):
            return self.check_format_dmY(date)
        if self.check_format_Ydm(date):
            return self.check_format_Ydm(date)
        if self.check_format_ydm(date):
            return self.check_format_ydm(date)
        return False

    @staticmethod
    def check_format_dmy(date: str):
        try:
            date = datetime.strptime(date, "%d.%m.%y")
            return date
        except ValueError:
            return False

    @staticmethod
    def check_format_dmY(date: str):
        try:
            corrected_date = datetime.strptime(date, "%d.%m.%Y")
            return corrected_date
        except ValueError:
            return False

    @staticmethod
    def check_format_ydm(date: str):
        try:
            corrected_date = datetime.strptime(date, "%y.%d.%m")
            return corrected_date
        except ValueError:
            return False

    @staticmethod
    def check_format_Ydm(date: str):
        try:
            corrected_date = datetime.strptime(date, "%Y.%d.%m")
            return corrected_date
        except ValueError:
            return False
