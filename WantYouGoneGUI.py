import tkinter as tk
import customtkinter
import subprocess
import queue
import threading

class CustomConsole(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Want You Gone GUI")
        self.geometry("800x600")
        self.configure(bg="#FF7F00")

        self.output_text = customtkinter.CTkLabel(master=self, justify="left", text="", width=100, height=30, text_color="#e9b15d", font=("Console", 28))
        self.output_text.place(x=10, y=10)
        
        self.frame = customtkinter.CTkFrame(master=self, width=155, height=40, border_color="#704910")
        self.frame.place(relx=0.7, rely=0.02, anchor='nw')
        
        self.process = None
        self.output_queue = queue.Queue()
        self.read_thread = threading.Thread(target=self.start_console)
        self.read_thread.start()

    def start_console(self):
        try:
            self.process = subprocess.Popen(['python', './WantYouGone.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in iter(self.process.stdout.readline, ''):
                self.output_queue.put(line)
        except Exception as e:
            print("Error starting subprocess:", e)
        finally:
            if self.process is not None:
                self.process.stdout.close()
                self.process.wait()
                self.process = None

    def read_process_output(self):
        while not self.output_queue.empty():
            line = self.output_queue.get()
            if line == '\x0c':
                self.output_text.configure(text="")
            else:
                current_text = self.output_text.cget("text")
                self.output_text.configure(text=current_text + line)

        if self.read_thread.is_alive():
            self.after(10, self.read_process_output)

if __name__ == "__main__":
    app = CustomConsole()
    app.mainloop()
