import asyncio
import inspect
import datetime
from colorama import Fore, Style
from src.infrastructure.configs.config_init import ConfigInit
import builtins

from src.infrastructure.database.factory.db_factory import test_db_in_mem, test_db_pgsql

real_print = builtins.print
LOG_COLORS = {
    "DEBUG": Fore.CYAN,
    "INFO": Fore.GREEN,
    "WARN": Fore.YELLOW,
    "ERROR": Fore.RED,
}

class Logger:
    def __init__(self):
        cfg = ConfigInit()
        self.level = cfg.model_dump().get("app_log_level", "DEBUG").upper()
        self.env = cfg.model_dump().get("env", "dev").upper()

    def _should_log(self, level):
        order = ["DEBUG", "INFO", "WARN", "ERROR"]
        return order.index(level) >= order.index(self.level)

    def log(self, level, *args):
        if not self._should_log(level):
            return
        
        frame = inspect.stack()[2]
        file = frame.filename.split("/")[-1]
        line = frame.lineno
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color = LOG_COLORS[level]

        real_print(f"{color}[{timestamp}] {level} {file}:{line} -> {' '.join(map(str,args))}{Style.RESET_ALL}")

        

# Global logger
logger = Logger()
    

def print(*args, level=None, **kwargs):
    if level is None:
        level = "DEBUG"
    logger.log(level.upper(), *args)

def log_debug(*args): logger.log("DEBUG", *args)
def log_info(*args): logger.log("INFO", *args)
def log_warn(*args): logger.log("WARN", *args)
def log_error(*args): logger.log("ERROR", *args)


def test_logs(env):
        if env != "DEV":
            return
        print("**************************************************")
        print("Testing logs...")
        print("**************************************************")
        log_debug("Debug message")
        log_info("Info message")
        log_warn("Some warning")
        log_error("Boom!")
        print("Hello")
test_logs(logger.env)
print("testing faCtory")
asyncio.run(test_db_in_mem())
asyncio.run(test_db_pgsql())

