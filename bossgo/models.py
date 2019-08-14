from datetime import datetime,timedelta

class ProxyModle(object):
    def __init__(self,data):
        self.ip = data['ip']
        self.port = data['port']
        self.expired_str = data['expire_time']
        self.blacked = False

        date_str, time_str = self.expired_str.split(" ")
        year, month, day = date_str.split("-")
        hour, minute, second = time_str.split(":")
        self.expired_time = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))

        self.proxy = "https://{}:{}".format(self.ip, self.port)

    @property
    def is_expiring(self):
        now = datetime.now()
        if (self.expired_time-now) < timedelta(seconds=5):
            return True
        else:
            return False