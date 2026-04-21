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
Use 'add <task name>' to create a to-do list and a new task.
Use 'ls' to see the task list.
Use 'delete' to delete a task, or 'delete' to delete all tasks.
"""

WELCOME_TEXT = """
Welcome to the To-Do CLI App!
"""


def welcome() -> None:
    """**It shows a welcome message with a print animation.**"""
    typing_text = Text()

    with Live(typing_text, refresh_per_second=20):
        for char in WELCOME_TEXT:
            typing_text.append(char, style="bold cyan")
            sleep(0.05)


def load_tasks() -> list[str]:
    """**Loads the task list.**

    Returns:
        list[str]: An empty or complete task list.
    """
    if todo_list.exists():
        with open(todo_list, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks: list[str]) -> None:
    """**Retrieves the task list and saves it.**

    Args:
        tasks (list[str]): Any list.
    """
    with open(todo_list, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


@app.command()
def add(
    task: str = typer.Argument(..., help="The text of the new task"),
) -> None:
    """**Gets one task and adds it to the list.
    Creates a 'todo_list.json' if it has not been created yet.**

    Args:
        task (str, optional): Any user input.
            Defaults to typer.Argument(..., help="The text of the new task").
    """
    tasks: list[str] = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print(MSG_DICT.get(0), f"New task added: {task}")


@app.command()
def ls() -> None:
    """**Loads the task list and shows it.**"""
    try:
        tasks: list[str] = load_tasks()

        if not tasks:
            print(
                MSG_DICT.get(2),
                "[bold red]The file is either not found or empty![/bold red]",
                "Use 'add' to create a file and add a task to it.",
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
        ..., help="The number of the task to delete (from 1)"
    ),
) -> None:
    """**Deletes either one task or all of them. It does not delete the '.json' itself.**

    Args:
        task_num (int, optional): Any user input from zero and above.
            Defaults to typer.Argument( ..., help="The number of the task to delete (from 1)" ).

    Raises:
        typer.Exit: It is called when it is impossible to find the necessary task by the index.
    """
    tasks: list[str] = load_tasks()
    idx: int = task_num - 1

    if idx == -1:
        tasks.clear()
        save_tasks(tasks)
        print(MSG_DICT.get(0), "All tasks have been deleted!")
    elif idx < len(tasks):
        removed_task = tasks.pop(idx)
        save_tasks(tasks)
        print(MSG_DICT.get(0), f"Task deleted: {removed_task}")
    else:
        print(
            MSG_DICT.get(2),
            f"There is no task with {task_num} number",
        )
        raise typer.Exit(code=1)


@app.command()
def help() -> None:
    """**Shows a welcome message and a list of all the commands.**"""
    welcome()
    print(HELP_TEXT)


if __name__ == "__main__":
    app()
