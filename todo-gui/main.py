import customtkinter as ctk
import json
from datetime import datetime
from pathlib import Path
from typing import Any


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("To-Do")
        # self.geometry("400x500")
        self.resizable(False, False)
        ctk.set_appearance_mode("system")

        self.tasks = []
        self._task_id_counter = 0
        self.todo_list = Path("todo_list.json")

        self._setup_ui()

    def center_window(window, width=400, height=500):
        # Get screen dimensions
        screen_width: int = window.winfo_screenwidth()
        screen_height: int = window.winfo_screenheight()

        # Calculate x and y coordinates for the window to be centered
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        # Set the geometry
        window.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_ui(self):
        # Main frame
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(fill="x", padx=20, pady=20)

        # Entry field
        self.entry = ctk.CTkEntry(
            entry_frame, placeholder_text="New task...", text_color="black"
        )
        self.entry.pack()

        # Button
        self.add_btn = ctk.CTkButton(
            entry_frame, text="Add", width=80, command=self._add_task
        )
        self.add_btn.pack(side="right")

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
        self.entry.delete(0, "end")
        self._save_tasks()

    def _save_tasks(self):
        with open(self.todo_list, "a", encoding="utf-8") as f:
            self.tasks: Any = json.dump(
                self.tasks, f, ensure_ascii=False, indent=4
            )


if __name__ == "__main__":
    app = App()
    app.center_window()
    app.mainloop()
