import time
import pyupbit
import datetime

access = "2EN4KQ4xxbH4wHmYt5pHLVCP2dZmsgxzwg5qxd1W"
secret = "GDIl2jiQxd6bYaPBo37BNZGGi6vBYr9MLTxpm7f4"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")  # 9:00
        end_time = start_time + datetime.timedelta(days=1)  # 익일 9:00

        # 09:00:00 ~ 08:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            # 매수가를 정하기 (2일 기준)
            target_price = get_target_price("KRW-BTC", 0.5)
            # 15일간의 평균 값을 확인 -> 상승장인지 하락장인지 확인 가능
            ma15 = get_ma15("KRW-BTC")
            # 현재가
            current_price = get_current_price("KRW-BTC")
            # 타겟 목표가 현재가 보다 낮고(가격 상승), 이동 평균선 이상이면 거래.
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw * 0.9995) # 0.05%는 수수료
        else:
            # 장마감일 10초 전부터는 전량 매도
            btc = get_balance("BTC")
            # 5000원 이상
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)