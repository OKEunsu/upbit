# upbit_api.py
import pyupbit
import config
from logger import setup_logger

logger = setup_logger()

class UpbitAPI:
    def __init__(self, access_key, secret_key):
        if not access_key or access_key == "YOUR_ACCESS_KEY" or \
           not secret_key or secret_key == "YOUR_SECRET_KEY":
            logger.warning("API 키가 설정되지 않았습니다. 실제 거래 관련 기능은 제한됩니다.")
            self.upbit = None
        else:
            try:
                self.upbit = pyupbit.Upbit(access_key, secret_key)
                logger.info("Upbit API 클라이언트가 성공적으로 초기화되었습니다.")
            except Exception as e:
                logger.error(f"Upbit API 클라이언트 초기화 실패: {e}")
                self.upbit = None

    def get_balance(self, currency="KRW"):
        """지정된 화폐의 잔고를 조회합니다."""
        if not self.upbit:
            return 0
        try:
            return self.upbit.get_balance(currency)
        except Exception as e:
            logger.error(f"{currency} 잔고 조회 실패: {e}")
            return 0

    def get_current_price(self, ticker):
        """현재가를 조회합니다."""
        try:
            return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
        except Exception as e:
            logger.error(f"{ticker} 현재가 조회 실패: {e}")
            return None

    def get_ohlcv(self, ticker, interval='day', count=20):
        """과거 시세 데이터를 가져옵니다. (open, high, low, close, volume)"""
        try:
            return pyupbit.get_ohlcv(ticker, interval=interval, count=count)
        except Exception as e:
            logger.error(f"{ticker} OHLCV 데이터 조회 실패: {e}")
            return None

    def buy_market_order(self, ticker, budget):
        """시장가 매수를 실행합니다."""
        if not self.upbit:
            logger.warning(f"API 키 미설정으로 {ticker} 시장가 매수를 실행할 수 없습니다.")
            return None
        try:
            result = self.upbit.buy_market_order(ticker, budget)
            logger.info(f"시장가 매수 주문 성공: {result}")
            return result
        except Exception as e:
            logger.error(f"{ticker} 시장가 매수 주문 실패: {e}")
            return None

    def sell_market_order(self, ticker, volume):
        """시장가 매도를 실행합니다."""
        if not self.upbit:
            logger.warning(f"API 키 미설정으로 {ticker} 시장가 매도를 실행할 수 없습니다.")
            return None
        try:
            result = self.upbit.sell_market_order(ticker, volume)
            logger.info(f"시장가 매도 주문 성공: {result}")
            return result
        except Exception as e:
            logger.error(f"{ticker} 시장가 매도 주문 실패: {e}")
            return None

# 싱글턴처럼 사용할 API 인스턴스 생성
api = UpbitAPI(config.UPBIT_ACCESS_KEY, config.UPBIT_SECRET_KEY)
