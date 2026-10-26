import customtkinter as ctk
import src.stoich.equation_parser as ep


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Stoichiometry Calculator")
        self.geometry("800x600")
        self.resizable(True, True)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter a chemical equation")
        self.entry.pack(padx=20, pady=20, fill="x")

        self.button = ctk.CTkButton(
            self, text="Balance Equation", command=self.balance_equation
        )
        self.button.pack(padx=20, pady=20)

        self.result = ctk.CTkLabel(self, text="", wraplength=600)
        self.result.pack(padx=20, pady=20)

    def balance_equation(self) -> str:
        equation = self.entry.get()
        # Implementation for balancing equation would go here
        try:
            prod_react_list = ep.parse_equation(equation)
            balanced_dict = ep.balance_equation(prod_react_list)
            equation = ep.format_reaction(balanced_dict)
            print(equation)
            self.result.configure(text=equation)
        except ValueError as e:
            # Handle the error (e.g., show a message box)
            print(e)


def run():
    App().mainloop()
