import customtkinter as ctk
import src.stoich.equation_parser as ep
from pathlib import Path
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._set_appearance_mode("system")
        self.title("Stoichiometry Calculator")
        self.geometry("800x600")
        self.resizable(True, True)

        equation_path_light = Path.cwd() / "assets" / "images" / "equation_light.png"
        equation_path_dark = Path.cwd() / "assets" / "images" / "equation_dark.png"

        self.equation_image = ctk.CTkImage(
            light_image=Image.open(equation_path_light),
            dark_image=Image.open(equation_path_dark),
            size=(300, 100),
        )
        self.equation_image_label = ctk.CTkLabel(
            self, image=self.equation_image, text=""
        )
        self.equation_image_label.pack(padx=20, pady=20)

        """self.entry = ctk.CTkEntry(self, placeholder_text="Enter a chemical equation")
        self.entry.pack(padx=20, pady=20, fill="x")

        self.button = ctk.CTkButton(
            self, text="Balance Equation", command=self.balance_equation
        )
        self.button.pack(padx=20, pady=20)

        self.result = ctk.CTkLabel(self, text="", wraplength=600)
        self.result.pack(padx=20, pady=20)

        """

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
