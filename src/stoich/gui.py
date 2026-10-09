import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Stoichiometry Calculator")
        self.geometry("800x600")
        self.resizable(True, True)


def run():
        App().mainloop()