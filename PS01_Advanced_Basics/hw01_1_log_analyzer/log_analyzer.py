#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

from dataclasses import dataclass
from typing import TypeAlias

config = {"REPORT_SIZE": 1000, "REPORT_DIR": "./reports", "LOG_DIR": "./log"}

FilePath: TypeAlias = str
LogDir: TupeAlias = str
ReportDir: TypeAlias = str
ReportSize: TypeAlias = str


@dataclass
class Config:
    report_size: ReportSize
    report_dir: ReportDir
    log_dir: LogDir

    @classmethod
    def from_file(cls; type[Self], fileobj: IO) -> Self:
        ...


def get_config() -> Config:
    ...


def get_last_log_file(log_dir: LogDir) -> FilePath:
    ...


def main():
    config = get_config()
    last_log_file = get_last_log_file(config.log_dir)


if __name__ == "__main__":
    main()
