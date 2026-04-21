import typer
from rich import print
import json
from pathlib import Path


app = typer.Typer()
todo_list = Path("todo_list.json")


MSG_DICT: dict[int, str] = {
    0: "[[bold green]SUCCESS[/bold green]]",
    1: "[[bold blue]INFO[/bold blue]]",
    2: "[[bold red]ERROR[/bold red]]",
}

HELP_TEXT: str = """
Use 'add' to create your task-list and add a first task.
Use 'ls' to list all your tasks.
Use 'delete <number>' to delete your tasks or 'delete 0' to delete all.
"""

# TODO: Docstrings


def load_tasks() -> list[str]:
    if todo_list.exists():
        with open(todo_list, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks: list[str]):
    with open(todo_list, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


@app.command()
def add(task: str = typer.Argument(..., help="Text of new task")):
    tasks: list[str] = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print(MSG_DICT.get(0), f"New task added: {task}.")


@app.command()
def ls():
    if todo_list.exists():
        with open(todo_list, "r", encoding="utf-8") as f:
            for i in f:
                print(i)
    else:
        print(
            MSG_DICT.get(2),
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
