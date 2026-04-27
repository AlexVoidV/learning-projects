import customtkinter as ctk
import json
from datetime import datetime
from pathlib import Path
from typing import Any


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("To-Do")
        self.resizable(False, False)
        ctk.set_appearance_mode("system")

        self.tasks: list[Any] = []
        self.task_widgets: list[Any] = []
        self._task_id_counter = 1
        self.todo_list = Path("todo_list.json")

        self._setup_ui()
        self._load_tasks()
        self.center_window()
        self.iconbitmap("icon/check-check.ico")

    def center_window(window, width=400, height=500):
        # Get screen dimensions
        screen_width: int = window.winfo_screenwidth()
        screen_height: int = window.winfo_screenheight()

        # Calculate x and y coordinates for the window to be centered
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        # Set the geometry
        window.geometry(f"{width}x{height}+{x}+{y}")

    def limit_entry(self, *args):
        if len(self.entry_var.get()) > self.limit:
            # self.after(0) postpones the change by 1 tick of the loop → recursion ends
            self.after(
                0,
                lambda: self.entry_var.set(self.entry_var.get()[: self.limit]),
            )

    def _setup_ui(self):
        # Main frame
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(
            fill="x",
            padx=20,
            pady=(15, 5),
        )
        self.entry_var = ctk.StringVar()
        self.limit = 28

        # Entry field
        self.entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="New task...",
            text_color="black",
            font=("Roboto", 14, "italic"),
            textvariable=self.entry_var,
        )
        self.entry.pack(
            fill="x",
            padx=(10, 10),
            pady=(14, 14),
            side="left",
            expand=True,
        )
        self.entry.bind(
            "<Return>",
            lambda e: self._add_task(),
        )

        self.entry_var.trace_add("write", self.limit_entry)

        # Button
        self.add_btn = ctk.CTkButton(
            entry_frame,
            text="Add",
            width=80,
            command=self._add_task,
            font=("Roboto", 14),
        )
        self.add_btn.pack(side="right", padx=10)

        # Scroll frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
        )
        self.scrollable_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10,
        )

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _add_task(self):
        # Define text
        text: str = self.entry.get().strip()
        if not text:
            return

        # Task model
        task: dict[str, Any | bool | str] = {
            "id": self._task_id_counter,
            "text": text,
            "completed": False,
            "created_at": datetime.now().isoformat(),
        }

        self._task_id_counter += 1
        self.tasks.append(task)
        self._render_tasks(task)
        self.entry.delete(0, "end")
        self._save_tasks()

    def _render_tasks(self, task):
        # Frame for Checkbox
        frame = ctk.CTkFrame(
            self.scrollable_frame,
        )
        frame.pack(
            fill="x",
            pady=4,
        )

        # Checkbox for To-Do list of tasks
        tdbox = ctk.CTkCheckBox(
            frame,
            text=task["text"],
            command=lambda t=task: self._toggle_task(t),
        )
        tdbox.pack(
            side="left",
            padx=8,
            pady=5,
        )

        # Delete button
        del_btn = ctk.CTkButton(
            frame,
            width=30,
            fg_color="#336fb0",
            hover_color="#245487",
            text="Delete",
            command=lambda t=task, f=frame: self._delete_task(t, f),
        )
        del_btn.pack(
            side="right",
            padx=8,
            pady=5,
        )

        self.task_widgets.append(
            {
                "data": task,
                "frame": frame,
                "checkbox": tdbox,
            }
        )
        if task["completed"]:
            tdbox.select()

    def _toggle_task(self, task):
        task["completed"] = not task["completed"]
        self._save_tasks()

    def _delete_task(self, task, frame):
        frame.destroy()
        self.tasks.remove(task)
        self.task_widgets: list[Any] = [
            w for w in self.task_widgets if w["data"] != task
        ]
        self._save_tasks()

    def _save_tasks(self):
        with open(self.todo_list, "w", encoding="utf-8") as f:
            json.dump(
                self.tasks,
                f,
                ensure_ascii=False,
                indent=4,
            )

    def _load_tasks(self):
        if self.todo_list.exists():
            with open(self.todo_list, "r", encoding="utf-8") as f:
                self.tasks: Any = json.load(f)
            for task in self.tasks:
                self._render_tasks(task)
                if task["id"] >= self._task_id_counter:
                    self._task_id_counter: int = task["id"] + 1

    def on_close(self):
        self._save_tasks()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
