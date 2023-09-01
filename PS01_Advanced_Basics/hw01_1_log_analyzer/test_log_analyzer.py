import io
from log_analyzer import Config, LogDir
import os
import tempfile
from pathlib import Path


def test_config():
    file = io.BytesIO(b"")

    got_config = Config.from_file(file)

    assert got_config == Config()


def test_get_last_log_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        wd = Path(tmpdir)
        (wd / "nginx-access-ui.log-20170630.gz").touch()
        (wd / "nginx-access-ui.log-20070630.gz").touch()

        got_last_file = LogDir(tmpdir).get_last_log_file()
            
        assert got_last_file == os.path.join(tmpdir, "nginx-access-ui.log-20170630.gz")


def test_get_last_log_file_ignores_wrong_filenames():
    ...


def test_get_last_log_file_from_empty_dir():
    ...


def test_get_last_log_file_different_extensions():
    ...
