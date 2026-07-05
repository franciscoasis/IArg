import threading
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from iarg.agent import Agent


class IArgGUI:
    def __init__(self):
        self.agent = Agent()

        self.root = tk.Tk()
        self.root.title("IArg")
        self.root.geometry("980x680")
        self.root.minsize(760, 520)

        style = ttk.Style(self.root)
        style.configure("IArg.TFrame", padding=12)

        self.status_var = tk.StringVar(value="Listo")

        self._build_layout()

    def _build_layout(self):
        frame = ttk.Frame(self.root, style="IArg.TFrame")
        frame.pack(fill="both", expand=True)

        header = ttk.Label(
            frame,
            text="IArg | Chat Local",
            font=("DejaVu Sans", 16, "bold"),
        )
        header.pack(anchor="w", pady=(0, 8))

        self.output = ScrolledText(
            frame,
            wrap="word",
            state="disabled",
            font=("DejaVu Sans Mono", 11),
        )
        self.output.pack(fill="both", expand=True)

        self.entry = tk.Text(
            frame,
            height=4,
            wrap="word",
            font=("DejaVu Sans", 11),
        )
        self.entry.pack(fill="x", pady=(10, 8))
        self.entry.bind("<Control-Return>", self._on_send_hotkey)

        controls = ttk.Frame(frame)
        controls.pack(fill="x")

        hint = ttk.Label(
            controls,
            text="Ctrl+Enter para enviar | /clear, /memory-stats, /memory-config, /memory-compact",
        )
        hint.pack(side="left")

        self.send_button = ttk.Button(
            controls,
            text="Enviar",
            command=self._on_send,
        )
        self.send_button.pack(side="right")

        self.status = ttk.Label(
            frame,
            textvariable=self.status_var,
            anchor="w",
        )
        self.status.pack(fill="x", pady=(8, 0))

        welcome = (
            "IArg listo. Escribí tu prompt y presioná Ctrl+Enter o Enviar.\n"
            "Tip: para editar desde GUI usá '/edit ruta::instruccion'."
        )
        self._append("sistema", welcome)

    def _set_busy(self, busy: bool):
        self.send_button.configure(state="disabled" if busy else "normal")
        self.entry.configure(state="disabled" if busy else "normal")
        self.status_var.set("Procesando..." if busy else "Listo")

    def _on_send_hotkey(self, _event):
        self._on_send()
        return "break"

    def _on_send(self):
        prompt = self.entry.get("1.0", "end").strip()

        if not prompt:
            return

        if prompt.startswith("/edit ") and "::" not in prompt:
            path = prompt.removeprefix("/edit ").strip()
            instruction = simpledialog.askstring(
                "Instrucción de edición",
                "¿Qué querés cambiar?",
                parent=self.root,
            )

            if not instruction:
                self.status_var.set("Edición cancelada")
                return

            prompt = f"/edit {path}::{instruction}"

        self.entry.delete("1.0", "end")
        self._append("vos", prompt)
        self._set_busy(True)

        thread = threading.Thread(
            target=self._run_agent,
            args=(prompt,),
            daemon=True,
        )
        thread.start()

    def _run_agent(self, prompt: str):
        try:
            answer = self.agent.run(prompt)
            self.root.after(0, lambda: self._handle_answer(answer))
        except Exception as exc:
            self.root.after(0, lambda: self._handle_error(exc))

    def _handle_answer(self, answer):
        self._append("iarg", str(answer))
        self._set_busy(False)

    def _handle_error(self, exc: Exception):
        self._append("error", f"{type(exc).__name__}: {exc}")
        self._set_busy(False)

    def _append(self, role: str, text: str):
        self.output.configure(state="normal")
        self.output.insert("end", f"[{role}]\n{text}\n\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def run(self):
        self.root.mainloop()


def launch_gui():
    app = IArgGUI()
    app.run()
