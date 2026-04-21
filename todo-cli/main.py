import typer
from rich import print
import json
from pathlib import Path
from time import sleep
from rich.live import Live
from rich.text import Text
# import sys
# from rich.console import Console


app = typer.Typer()
todo_list = Path("todo_list.json")


MSG_DICT: dict[int, str] = {
    0: "[[bold green]SUCCESS[/bold green]]",
    1: "[[bold blue]INFO[/bold blue]]",
    2: "[[bold red]ERROR[/bold red]]",
}

HELP_TEXT: str = """
Use 'add <task name>' to create your task-list and add a first task.
Use 'ls' to list all your tasks.
Use 'delete <number>' to delete your task or 'delete 0' to delete all.
"""

WELCOME_TEXT = """
Welcome to To-Do CLI App!
"""

# TODO: Docstrings

## First attempt to animate text
# def typing_print(text):
#     for char in text:
#         sys.stdout.write(char)
#         sys.stdout.flush()
#         sleep(0.05)


def welcome():
    typing_text = Text()

    with Live(typing_text, refresh_per_second=20):
        for char in WELCOME_TEXT:
            typing_text.append(char, style="bold cyan")
            sleep(0.05)


def load_tasks() -> list[str]:
    if todo_list.exists():
        with open(todo_list, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks: list[str]) -> None:
    with open(todo_list, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


@app.command()
def add(task: str = typer.Argument(..., help="Text of new task")) -> None:
    tasks: list[str] = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print(MSG_DICT.get(0), f"New task added: {task}")


@app.command()
def ls() -> None:
    try:
        tasks: list[str] = load_tasks()

        if not tasks:
            print(
                MSG_DICT.get(2),
                "[bold red]File not found or empty![/bold red]",
                "Use 'add' command to create file and new task.",
            )
            return

        print(MSG_DICT.get(1), "Your tasks:")
        for i, t in enumerate(tasks, 1):
            print(f"{i}. {t}")

    except json.JSONDecodeError:
        print(MSG_DICT.get(2), "The file is empty!")


@app.command()
def delete(
    task_num: int = typer.Argument(
        ..., help="The number of task for deleting (from 1)"
    ),
) -> None:
    tasks: list[str] = load_tasks()
    idx: int = task_num - 1

    if idx == -1:
        tasks.clear()
        save_tasks(tasks)
    elif idx < len(tasks):
        removed_task = tasks.pop(idx)
        save_tasks(tasks)
        print(MSG_DICT.get(0), f"The task was removed: {removed_task}")
    else:
        print(
            MSG_DICT.get(2),
            f"The task with the number {task_num} is not exist",
        )
        raise typer.Exit(code=1)


@app.command()
def help() -> None:
    welcome()
    print(HELP_TEXT)


if __name__ == "__main__":
    app()
