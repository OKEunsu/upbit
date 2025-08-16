# main.py
import time
import schedule
from trader import Trader
from logger import setup_logger

def job():
    """스케줄러가 실행할 작업"""
    trader_instance = Trader()
    trader_instance.run()

def main():
    """프로그램 메인 실행 함수"""
    setup_logger()
    logger = setup_logger()
    
    logger.info("="*50)
    logger.info("🚀 업비트 자동매매 프로그램을 시작합니다.")
    logger.info(f"거래 코인: {config.TICKER}")
    logger.info(f"매매 주기: {config.TRADE_INTERVAL_SECONDS}초")
    logger.info("="*50)

    # # --- 즉시 1회 실행 (테스트용) ---
    # job() 
    
    # --- 스케줄링 실행 ---
    schedule.every(config.TRADE_INTERVAL_SECONDS).seconds.do(job)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("프로그램을 종료합니다.")
            break
        except Exception as e:
            logger.error(f"메인 루프에서 예상치 못한 에러 발생: {e}")
            time.sleep(config.TRADE_INTERVAL_SECONDS) # 에러 발생 시 잠시 대기 후 재시도

if __name__ == "__main__":
    main()
