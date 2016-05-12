import os
import re

from mock import MagicMock

from ephemerol import ephemerol as cli
from ephemerol.SingleFileProcessor import SingleFileProcessor

good_message = re.compile("^Examining .*")


def test_main_accepts_filename(capsys):
    cli.main([os.path.join('ephemerol', 'test', 'SampleWebApp-master.zip')])
    out, err = capsys.readouterr()
    assert good_message.match(out) is not None


def test_file_passed_to_all_modules():
    mod1 = MockModule()
    mod1.handles = MagicMock(return_value=True)
    mod2 = MockModule()
    mod2.handles = MagicMock(return_value=True)

    proc = SingleFileProcessor([mod1, mod2])
    proc.process("foo")
    mod1.handles.assert_called_with("foo")
    mod2.handles.assert_called_with("foo")


class MockModule:
    def __init__(self):
        return

    @classmethod
    def handles(cls, file_name):
        return False

    @classmethod
    def do_handle(cls, file_name):
        return []