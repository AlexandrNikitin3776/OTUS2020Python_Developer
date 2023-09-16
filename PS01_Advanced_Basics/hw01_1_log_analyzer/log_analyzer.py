"""
log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
                    '$request_time';

"""

import argparse
from dataclasses import dataclass
from datetime import datetime
from typing import BinaryIO, Self
from pathlib import Path
import re
import tomllib
from zoneinfo import ZoneInfo


LOGFILE_REGEX = re.compile(r"nginx-access-ui.log-(\d+).gz")
DEFAULT_TIMEZONE = ZoneInfo("UTC")


def get_ts_from_logfile(path: Path) -> int:
    m = LOGFILE_REGEX.search(path.name)
    if not m:
        raise ValueError(f"Wrong log file: {path.name!r}")
    dt = datetime.strptime(m.group(1), "%Y%m%d")
    dt = dt.replace(tzinfo=DEFAULT_TIMEZONE)
    return int(dt.timestamp())


@dataclass
class Config:
    report_size: int = 1000
    report_dir: Path = Path("./reports")
    log_dir: Path = Path("./log")
    report_template_path: Path = Path("./templates/report.html")

    @classmethod
    def from_file(cls, fileobj: BinaryIO) -> Self:
        """Getting config from config file"""
        data = tomllib.load(fileobj)
        return cls(**data)

    def __post_init__(self):
        if not isinstance(self.report_dir, Path):
            self.report_dir = Path(self.report_dir)
        if not isinstance(self.log_dir, Path):
            self.log_dir = Path(self.log_dir)
        if not isinstance(self.report_template_path, Path):
            self.report_template_path = Path(self.report_template_path)


@dataclass
class LogFile:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.ts = get_ts_from_logfile(path)

    def __lt__(self, other: "LogFile"):
        return self.ts < other.ts


class LogDir:
    def __init__(self, path: Path) -> None:
        self.path = path

    def get_last_log_file(self) -> LogFile:
        files = self.path.glob("nginx-access-ui.log-*.gz")
        log_files = map(LogFile, files)
        return max(log_files)


class ReportDir:
    def __init__(self, path: Path) -> None:
        self.path = path

    def construct_report_path(self, ts: int) -> Path:
        ...

    def is_report_processed(self, path: Path) -> bool:
        ...


@dataclass
class ReportFile:
    report_path: Path


@dataclass
class Report:
    ...


def render_report(report_data: list[Report], template: Path) -> str:
    ...


def main():
    parser = argparse.ArgumentParser(
        prog="Log analyzer",
        description="Parse last nginx log from logs dir to reports dir",
    )
    parser.add_argument("-c", "--config", default="./config.toml", help="Config file path in toml format")
    args = parser.parse_args()

    with open(args.config, "rb") as config_toml:
        config = Config.from_file(config_toml)

    log_dir = LogDir(config.log_dir)
    last_log_file = log_dir.get_last_log_file()

    report_dir = ReportDir(config.report_dir)
    report_path = report_dir.construct_report_path(last_log_file.ts)
    if report_dir.is_report_processed(report_path):
        return

    report = "None"
    with open(report_path, "w") as report_file:
        report_file.write(report)
