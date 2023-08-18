"""
log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
                    '$request_time';

"""

from dataclasses import dataclass
from datetime import datetime
from typing import IO, Self, TypeAlias

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "REPORT_TEMPLATE": "./templates/report.html",
}

FilePath: TypeAlias = str
LogDir: TypeAlias = str
ReportDir: TypeAlias = str
ReportSize: TypeAlias = str


@dataclass
class Config:
    """Parser config"""

    report_size: ReportSize
    report_dir: ReportDir
    log_dir: LogDir

    @classmethod
    def from_file(cls, fileobj: IO) -> Self:
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


def get_config() -> Config:
    """Getting config from config file"""
 
    ...


def get_last_log_filenane(log_dir: LogDir) -> FilePath:
    ...


def is_report_processed(report_dir: ReportDir, log_file: FilePath) -> bool:
    ...


def render_report(report_data: list[ReportFile], template: FilePath) -> str:
    ...


def main():
    config = get_config()

    last_log_file = get_last_log_file(config.log_dir)
    if is_report_processed(config.report_dir, last_log_file):
        return

    report = render_report(report_data, config.render_template)
    report_filename = construct_report_filename(config.report_dir, last_log_filename)
    with open(report_filename, "w") as report_file:
        report_file.write(report)


if __name__ == "__main__":
    main()
