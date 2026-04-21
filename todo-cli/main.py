import typer
from rich import print
import json  # noqa: F401
from pathlib import Path


app = typer.Typer()
todo_list = Path("todo_list.txt")


MSG_DICT: dict[int, str] = {
    0: "[ERROR]",
    1: "[INFO]",
}

HELP_TEXT: str = """
Use 'add' to create your task-list and add a first task.
Use 'ls' to list all your tasks.
Use 'delete <number>' to delete your tasks or 'delete 0' to delete all.
"""


@app.command()
def add(task: str):
    with open(todo_list, "a", encoding="utf-8") as f:
        f.write(task)


@app.command()
def ls():
    if todo_list.exists():
        with open(todo_list, "r", encoding="utf-8") as f:
            for i in f:
                print(i)
    else:
        print(
            MSG_DICT.get(0),
            "[bold red]File not found![/bold red]",
            "Use 'add' command to create file and new task.",
        )


@app.command()
def delete(task_num: int):
    pass


@app.command()
def help():
    print(HELP_TEXT)


if __name__ == "__main__":
    app()
