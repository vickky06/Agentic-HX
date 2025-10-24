import inspect
import datetime
from colorama import Fore, Style
from src.infrastructure.configs.config_init import ConfigInit
import builtins

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

def debug(*args): logger.log("DEBUG", *args)
def info(*args): logger.log("INFO", *args)
def warn(*args): logger.log("WARN", *args)
def error(*args): logger.log("ERROR", *args)


def test_logs(env):
        if env != "DEV":
            return
        print("**************************************************")
        print("Testing logs...")
        print("**************************************************")
        debug("Debug message")
        info("Info message")
        warn("Some warning")
        error("Boom!")
        print("Hello")
test_logs(logger.env)


