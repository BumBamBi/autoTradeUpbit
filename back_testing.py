import pyupbit
import numpy as np

# 7일간의 BTC OHLCV를 불러옴
# OHLCV = Open High Low Close Volume (시가 고가 저가 종가 거래량)
df = pyupbit.get_ohlcv("KRW-BTC", count=7)


# 변동성 돌파 전략 -> 매수가를 구하기 위한 코드
# 매수가 = 전날의 고가 저가 변동폭의 k배
# 전날 변동폭의 k배 구하기
df['range'] = (df['high'] - df['low']) * 0.5

# 매수가 = 시가 + 전날 변동폭*k배
df['target'] = df['open'] + df['range'].shift(1)

# 수익률 계산
fee = 0 # 수수료 업비트는 0.05%임

# np.where 은 3항연산자(? : )와 동일
# 고가 > 타겟 ? 종가(매도가)/타켓 : 1
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)

# 누적 수익률
df['hpr'] = df['ror'].cumprod()

# 낙폭(Draw Down) 계산
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# 가장 큰 낙폭(Max DrawDown) 계산
print("MDD(%): ", df['dd'].max())

# 엑셀로 출력
df.to_excel("dd.xlsx")