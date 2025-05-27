import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme


class RichLogger:
    """
    Rich 彩色日志系统
    功能：
    - 控制台彩色输出（Rich）
    - 按日期时间命名的日志文件
    - 自动按天轮转日志
    - 同时输出到文件和终端
    """

    def __init__(
            self,
            name: str = "APP",
            log_dir: str = "logs",
            console_level: str = "INFO",
            file_level: str = "DEBUG",
            time_format: str = "%Y-%m-%d_%H-%M-%S"
    ):
        """
        初始化日志系统

        Args:
            name: 日志名称（会体现在日志中）
            log_dir: 日志目录
            console_level: 控制台日志级别
            file_level: 文件日志级别
            time_format: 日志文件名时间格式
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.time_format = time_format
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 确保日志目录存在
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 初始化控制台和文件处理器
        self._setup_console_handler(console_level)
        self._setup_file_handler(file_level)

    def _setup_console_handler(self, level: str):
        """配置 Rich 控制台输出"""
        console = Console(theme=Theme({
            "logging.level.debug": "dim blue",
            "logging.level.info": "bold green",
            "logging.level.warning": "bold yellow",
            "logging.level.error": "bold red",
            "logging.level.critical": "bold white on red"
        }))

        rich_handler = RichHandler(
            level=getattr(logging, level),
            console=console,
            markup=True,
            show_time=False
        )
        rich_handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(rich_handler)

    def _setup_file_handler(self, level: str):
        """配置按时间命名的文件日志"""
        timestamp = datetime.now().strftime(self.time_format)
        log_file = self.log_dir / f"{self.name}_{timestamp}.log"

        file_handler = TimedRotatingFileHandler(
            log_file,
            when="midnight",
            backupCount=7,
            encoding="utf-8"
        )
        file_handler.setLevel(getattr(logging, level))
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """获取配置好的日志器"""
        return self.logger




