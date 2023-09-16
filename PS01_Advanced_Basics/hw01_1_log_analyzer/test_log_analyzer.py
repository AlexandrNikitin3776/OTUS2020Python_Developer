import io
from log_analyzer import Config, LogDir, LogFile, get_ts_from_logfile
import tempfile
from pathlib import Path
import unittest


class TestConfig(unittest.TestCase):
    def test_config(self):
        test_cases = {
            "empty": {
                "file_content": b"",
                "want_config": Config(),
            },
            "report_size": {
                "file_content": b"report_size=500",
                "want_config": Config(report_size=500),
            },
            "report_dir": {
                "file_content": b'report_dir="/home/user/reports"',
                "want_config": Config(report_dir=Path("/home/user/reports")),
            },
        }
        for tc, tdata in test_cases.items():
            with self.subTest(msg=tc):
                file = io.BytesIO(tdata["file_content"])

                got_config = Config.from_file(file)

                self.assertEqual(got_config, tdata["want_config"])


class TestDateParsers(unittest.TestCase):
    def testpip_get_ts_from_logfile(self):
        test_cases = [
            {
                "filepath": Path("/home/user/data/nginx-access-ui.log-20070630.gz"),
                "want_ts": 1183161600,
            }
        ]
        for tc in test_cases:
            with self.subTest(msg=tc):
                got_ts = get_ts_from_logfile(tc["filepath"])

                self.assertEqual(got_ts, tc["want_ts"])


class TestLogDir(unittest.TestCase):
    def test_get_last_log_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            wd = Path(tmpdir)
            (wd / "nginx-access-ui.log-20170630.gz").touch()
            (wd / "nginx-access-ui.log-20070630.gz").touch()

            got_last_file = LogDir(Path(tmpdir)).get_last_log_file()

            assert got_last_file == LogFile(Path(tmpdir, "nginx-access-ui.log-20170630.gz"))

    def test_get_last_log_file_ignores_wrong_filenames(self):
        ...

    def test_get_last_log_file_from_empty_dir(self):
        ...

    def test_get_last_log_file_different_extensions(self):
        ...
