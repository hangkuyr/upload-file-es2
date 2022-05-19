from datetime import datetime

def GetCurrentUTCTimestamp():
    return datetime.utcnow().timestamp()

def TimestampToDatetime(t):
    return datetime.fromtimestamp(t)

def DatetimeToStr(d):
    return f'{d:%Y-%m-%d %H:%M:%S%z}'

def TimestampToStr(t):
    d = TimestampToDatetime(t)
    return DatetimeToStr(d)