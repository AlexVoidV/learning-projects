from click.testing import Result
from typer.testing import CliRunner
from main import app
from pathlib import Path  # noqa: F401
from rich import print  # noqa: F401
import json  # noqa: F401
import pytest  # noqa: F401


runner = CliRunner()
TEST_TASK = "test task"
TEST_TASK_2 = "test task two"


# @pytest.fixture(autouse=True)
# def use_temp_file(tmp_path, monkeypatch):
#     temp_file = tmp_path / "todo_list.json"
#     monkeypatch.__setattr__("app.todo_list", temp_file)
#     yield temp_file


def test_add():
    result: Result = runner.invoke(app, ["add", TEST_TASK])
    assert result.exit_code == 0
    assert "SUCCESS" in result.output


def test_ls():
    result: Result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    assert f"1. {TEST_TASK}" in result.output


def test_delete():
    runner.invoke(app, ["add", TEST_TASK_2])

    result: Result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0
    assert "SUCCESS" in result.output
