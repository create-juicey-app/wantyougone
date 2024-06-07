import tkinter as tk
import customtkinter
import subprocess
import queue
import threading
import random

class CustomConsole(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Want You Gone GUI")
        self.geometry("800x600")
        self.configure(bg="#704910")

        self.fps = 60
        self.delay = int(1000 / self.fps)

        self.output_text = customtkinter.CTkLabel(
            master=self, justify="left", text="", width=100, height=30,
            text_color="#e9b15d", font=("Console", 28)
        )
        self.output_text.place(x=10, y=10)

        self.frame = customtkinter.CTkFrame(
            master=self, width=155, height=40, border_color="#704910"
        )
        self.frame.place(relx=0.7, rely=0.02, anchor='nw')

        self.matrix = customtkinter.CTkLabel(
            master=self.frame, anchor="ne", justify="left", text="101001110100",
            width=100, height=30, text_color="#e9b15d", font=("Console", 12)
        )
        self.matrix.place(relx=0.5, rely=0.5, anchor='center')

        self.update_matrix()
        self.process = None
        self.output_queue = queue.Queue()

        threading.Thread(target=self.start_console).start()

    def start_console(self):
        self.process = subprocess.Popen(
            ['python', './wantYouGone.py'], stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, universal_newlines=True
        )

        self.read_process_output()

    def read_process_output(self):
        if self.process is not None:
            if self.process.poll() is not None:
                self.process = None
                return

            try:
                char = self.process.stdout.read(1)
                if char:
                    self.output_queue.put(char)
            except Exception as e:
                print("Error reading subprocess output:", e)

            while not self.output_queue.empty():
                char = self.output_queue.get()
                if char == '\x0c':
                    self.output_text.configure(text="")
                else:
                    current_text = self.output_text.cget("text")
                    self.output_text.configure(text=current_text + char)

            self.after(10, self.read_process_output)
        else:
            self.after(100, self.read_process_output)


if __name__ == "__main__":
    app = CustomConsole()
    app.mainloop()
