"""
log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
                    '$request_time';

"""

import argparse
from dataclasses import dataclass
from datetime import datetime
from typing import IO, Self
from pathlib import Path


@dataclass
class Config:
    report_size: int = 1000
    report_dir: Path = Path("./reports")
    log_dir: Path = Path("./log")
    report_template_path: Path = Path("./templates/report.html")

    @classmethod
    def from_file(cls, fileobj: IO) -> Self:
        """Getting config from config file"""
        ...


@dataclass
class LogFile:
    log_date: datetime
    log_path: Path

    @classmethod
    def from_log_path(cls, log_path: Path) -> Self:
        ...


@dataclass
class ReportFile:
    report_path: Path


@dataclass
class Report:
    ...


def get_last_log_file(log_dir: Path) -> LogFile:
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

    with open(args.config) as config_toml:
        config = Config.from_file(config_toml)

    last_log_file = get_last_log_file(config.log_dir)
    if is_report_processed(config.report_dir, last_log_file):
        return

    report = render_report(report_data, config.render_template)
    report_filename = construct_report_filename(config.report_dir, last_log_filename)
    with open(report_filename, "w") as report_file:
        report_file.write(report)


if __name__ == "__main__":
    main()
