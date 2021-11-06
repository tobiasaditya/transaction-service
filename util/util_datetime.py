from datetime import datetime
import pytz

def datetime_jakarta():
    waktu_jakarta = datetime.now(pytz.timezone('Asia/Jakarta'))
    return waktu_jakarta