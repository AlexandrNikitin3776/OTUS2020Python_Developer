import io
from log_analyzer import Config
import tempfile


def test_config():
    file = io.StringIO("""[ini]""")
    
    got_config = Config.from_file(file)
    
    assert get_config == Config()


def test_get_last_log_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        with tempfile.NamedTemporaryFile(dir=tmpdir) as tmpfile:
            assert False
