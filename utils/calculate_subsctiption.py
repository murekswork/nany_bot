import datetime


def calculate_subscription_end(free_days: int) -> datetime:
    today = datetime.datetime.today()
    end_date = today + datetime.timedelta(days=free_days)
    return end_date
