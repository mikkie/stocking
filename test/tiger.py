import decimal
from decimal import Decimal
context=decimal.getcontext() # 获取decimal现在的上下文
context.rounding = decimal.ROUND_05UP

print(round(Decimal(2.9), 0))		# 2.6
print(format(Decimal(2.5), '.d'))	#'2.6'