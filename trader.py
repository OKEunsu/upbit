# trader.py
import config
from upbit_api import api
from strategy import get_trading_signal
from logger import setup_logger

logger = setup_logger()

class Trader:
    def __init__(self):
        self.ticker = config.TICKER
        self.budget = config.TRADE_BUDGET
        # 코인 심볼만 추출 (예: "KRW-BTC" -> "BTC")
        self.coin_symbol = self.ticker.split('-')[1]

    def run(self):
        logger.info("="*40)
        logger.info("자동매매 로직 시작...")

        try:
            # 1. 매매 신호 가져오기
            signal = get_trading_signal(self.ticker)
            logger.info(f"현재 매매 신호: {signal}")

            # 2. 보유 자산 확인
            krw_balance = api.get_balance("KRW")
            coin_balance = api.get_balance(self.coin_symbol)
            
            logger.info(f"보유 잔고: {krw_balance:.2f} KRW, {coin_balance} {self.coin_symbol}")

            # 3. 신호에 따라 매매 실행
            if signal == "BUY":
                if krw_balance >= self.budget:
                    logger.info(f"{self.budget} KRW 만큼 {self.ticker} 시장가 매수를 시도합니다.")
                    api.buy_market_order(self.ticker, self.budget)
                else:
                    logger.warning(f"매수 예산 부족. (필요: {self.budget}, 보유: {krw_balance})")

            elif signal == "SELL":
                if coin_balance > 0:
                    logger.info(f"보유 중인 {coin_balance} {self.coin_symbol} 전량 시장가 매도를 시도합니다.")
                    api.sell_market_order(self.ticker, coin_balance)
                else:
                    logger.info("매도할 코인을 보유하고 있지 않습니다.")
            
            else: # HOLD
                logger.info("관망 상태를 유지합니다.")

        except Exception as e:
            logger.error(f"매매 로직 실행 중 에러 발생: {e}")
        
        logger.info("자동매매 로직 종료.")
        logger.info("="*40 + "\n")
