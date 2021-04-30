import pyupbit

access = "2EN4KQ4xxbH4wHmYt5pHLVCP2dZmsgxzwg5qxd1W"          # 본인 값으로 변경
secret = "GDIl2jiQxd6bYaPBo37BNZGGi6vBYr9MLTxpm7f4"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회

# 백테스팅

