import io
from log_analyzer import Config, get_last_log_file
import os
import tempfile


def touch(dir: str, filename: str) -> str:
    filepath = os.path.join(tmpdir, filename)
    with open(filepath, "w"):
        pass
    return filepath


def test_touch():
    filename = "test_file.txt"
    with tempfile.TemporaryDirectory() as tmpdir:
        got_filepath = touch(tmpdir, filename)

        assert os.path.isfile(got_filepath)
        assert got_filepath == os.path.join(tmpdir, filename)


def test_config():
    file = io.StringIO("")

    got_config = Config.from_file(file)

    assert got_config == Config()


def test_get_last_log_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        touch(tmpdir, "nginx-access-ui.log-20170630.gz")
        touch(tmpdir, "nginx-access-ui.log-20070630.gz")

        got_last_file = get_last_log_file(tmpdir)
            
        assert got_last_file == os.path.join(tmpdir, "nginx-access-ui.log-20170630.gz")


def test_get_last_log_file_ignores_wrong_filenames():
    ...


def test_get_last_log_file_from_empty_dir():
    ...


def test_get_last_log_file_different_extensions():
    ...
