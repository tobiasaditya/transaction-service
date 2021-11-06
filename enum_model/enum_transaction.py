from enum import Enum

class trxMethodEnum(str,Enum):
    def __str__(self):
        return str(self.value)
    GOPAY = "GOPAY"
    OVO = "OVO"
    BCA = "BCA"
    CIMB_NIAGA = "CIMB NIAGA"
    CASH = "CASH"

class trxTypeEnum(str,Enum):
    def __str__(self):
        return str(self.value)
    PURCHASE = "PURCHASE"
    INCOME = "INCOME"