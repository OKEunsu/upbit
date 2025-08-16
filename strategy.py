# strategy.py
from upbit_api import api
from logger import setup_logger

logger = setup_logger()

def get_trading_signal(ticker):
    """
    간단한 이동평균선(MA) 교차 전략
    - 5일 이동평균선이 20일 이동평균선을 상향 돌파(골든 크로스)하면 'BUY'
    - 5일 이동평균선이 20일 이동평균선을 하향 돌파(데드 크로스)하면 'SELL'
    - 그 외에는 'HOLD'
    """
    try:
        df = api.get_ohlcv(ticker, interval='day', count=21)
        if df is None:
            logger.warning(f"{ticker} 데이터 조회 실패로 매매 신호를 생성할 수 없습니다.")
            return "HOLD"

        # 이동평균선 계산
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma20'] = df['close'].rolling(window=20).mean()

        # 최근 두 데이터(어제, 오늘) 가져오기
        yesterday = df.iloc[-2]
        today = df.iloc[-1]

        logger.debug(f"[{ticker}] Today(MA5: {today['ma5']:.2f}, MA20: {today['ma20']:.2f})")
        logger.debug(f"[{ticker}] Yesterday(MA5: {yesterday['ma5']:.2f}, MA20: {yesterday['ma20']:.2f})")

        # 골든 크로스 확인
        if yesterday['ma5'] < yesterday['ma20'] and today['ma5'] > today['ma20']:
            logger.info(f"[{ticker}] 골든 크로스 발생! 매수 신호.")
            return "BUY"
        # 데드 크로스 확인
        elif yesterday['ma5'] > yesterday['ma20'] and today['ma5'] < today['ma20']:
            logger.info(f"[{ticker}] 데드 크로스 발생! 매도 신호.")
            return "SELL"
        else:
            return "HOLD"

    except Exception as e:
        logger.error(f"매매 신호 생성 중 에러 발생: {e}")
        return "HOLD"
