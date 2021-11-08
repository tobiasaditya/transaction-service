from datetime import datetime, timedelta
import pytz

def datetime_jakarta():
    waktu_jakarta = datetime.now()+timedelta(hours=7)
    return waktu_jakarta