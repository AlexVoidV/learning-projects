import typer  # noqa: F401
from rich import print  # noqa: F401
import json  # noqa: F401
from pathlib import Path  # noqa: F401


app = typer.Typer()
todo_list = Path("todo_list.txt")


def cr_file(task: str = ""):
    with open("todo_list.txt", "x"):
        pass


@app.command()
def add(task: str):
    if todo_list.exists():
        with open("todo_list.txt", "a") as f:
            f.write(task)
    else:
        cr_file(task)


@app.command()
def show():
    if todo_list.exists():
        with open("todo_list.txt", "r") as f:
            for i in f:
                print(i)


@app.command()
def delete():
    pass


if __name__ == "__main__":
    app()
