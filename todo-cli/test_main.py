from click.testing import Result
from typer.testing import CliRunner
from main import app
from pathlib import Path  # noqa: F401
from rich import print  # noqa: F401
import json  # noqa: F401
import pytest  # noqa: F401


runner = CliRunner()
TEST_TASK = "test task"


def test_add():
    result: Result = runner.invoke(app, ["add", TEST_TASK])
    assert result.exit_code == 0
    assert "SUCCESS" in result.output


def test_ls():
    result: Result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    assert TEST_TASK in result.output
