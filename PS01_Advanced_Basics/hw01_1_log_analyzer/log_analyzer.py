"""
log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
                    '$request_time';

"""

import argparse
from dataclasses import dataclass
from datetime import datetime
from typing import IO, Self, TypeAlias

FilePath: TypeAlias = str
LogDir: TypeAlias = str
ReportDir: TypeAlias = str
ReportSize: TypeAlias = str


@dataclass
class Config:
    """Parser config"""

    report_size: ReportSize = 1000
    report_dir: ReportDir = "./reports"
    log_dir: LogDir = "./log"
    report_template_path: str = "./templates/report.html"

    @classmethod
    def from_file(cls, fileobj: IO) -> Self:
        """Getting config from config file"""
        ...


@dataclass
class LogFile:
    """Log file info"""

    date: datetime
    path: str

    @classmethod
    def from_path(cls, path: str) -> Self:
        ...


@dataclass
class ReportFile:
    """ Report file info"""

    path: str

    @classmethod
    def from_logfile(cls, logfile: LogFile) -> Self:
        ...


def get_last_log_file(log_dir: LogDir) -> FilePath:
    ...


def is_report_processed(report_dir: ReportDir, log_file: FilePath) -> bool:
    ...


def render_report(report_data: list[ReportFile], template: FilePath) -> str:
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
