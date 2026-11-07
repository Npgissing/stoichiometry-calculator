import customtkinter as ctk
import src.stoich.equation_parser as ep
from pathlib import Path
from PIL import Image
from time import sleep

# Create a default image
default_image_path = Path.cwd() / "assets" / "images" / "default.png"
size = (1, 1)
default_image = Image.new("RGBA", size, (0, 0, 0, 0))
default_image.save(default_image_path)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._set_appearance_mode("System")
        self.title("Stoichiometry Calculator")
        self.geometry("464x638")
        self.resizable(False, False)
        self.equation_dict = {}
        self.equation_amounts = []
        self.equation_type = None

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter a chemical equation")
        self.entry.pack(padx=20, pady=10, fill="x")

        self.balance_equation_button = ctk.CTkButton(self, text="Balance Equation", command=self.balance_equation)
        self.balance_equation_button.pack(padx=20, pady=10)

    def reset(self):
        pass

    def balance_equation(self):
        equation = self.entry.get()
        # Implementation for balancing equation would go here
        try:
            prod_react_list = ep.parse_equation(equation)
            balanced_dict = ep.balance_equation(prod_react_list)
            self.equation_dict = balanced_dict
            equation = ep.format_reaction(balanced_dict)
            self.equation_type = ep.determine_equation_type(equation)
            print(equation)

            equation_path_light = Path.cwd() / "assets" / "images" / "equation_light.png"
            equation_path_dark = Path.cwd() / "assets" / "images" / "equation_dark.png"

            ep.generate_equation_image(ep.format_equation_latex(equation))

            equation_light = open_image(equation_path_light)
            equation_dark = open_image(equation_path_dark)

            horizontal, vertical = equation_light.size
            refitted = (horizontal / vertical * 30, 30)

            self.equation_image = ctk.CTkImage(
                light_image=equation_light,
                dark_image=equation_dark,
                size=refitted,
            )
            self.equation_image_label = ctk.CTkLabel(self, image=self.equation_image, text="")
            self.equation_image_label.pack(padx=20, pady=10)

            self.equation_amounts_frame = EntryAmounts(self, self.equation_dict)
            self.equation_amounts_frame.pack(padx=20, pady=10, fill="x")

            self.calculate_button = ctk.CTkButton(self, text="Calculate", command=self.calculate)
            self.calculate_button.pack(padx=20, pady=10)
        except ValueError as e:
            # Handle the error (e.g., show a message box)
            print(e)

    def calculate(self):
        for i, entry in enumerate(self.equation_amounts_frame.entries):
            try:
                amount = ep.parse_amount(list(self.equation_dict.keys())[i], entry.get())
                self.equation_amounts.append(amount)
            except ValueError as e:
                # Handle the error (e.g., show a message box)
                print(e)
        final_results = ep.calculate_equation(self.equation_dict, self.equation_amounts, self.equation_type)
        self.results_frame = ResultsFrame(self, final_results)
        print("Calculated")


class EntryAmounts(ctk.CTkFrame):
    def __init__(self, master, equation_dict):
        super().__init__(master)
        self.entries = []
        self.equation_dict = equation_dict
        for i in range(len(self.equation_dict)):
            self.grid_columnconfigure(i, weight=1)
            entry = ctk.CTkEntry(self, placeholder_text=list(self.equation_dict.keys())[i].formula)
            entry.grid(row=0, column=i, padx=10, pady=10)
            self.entries.append(entry)
        self.pack(padx=20, pady=10, fill="x")


class ResultsFrame(ctk.CTkFrame):
    def __init__(self, master, final_results):
        super().__init__(master)
        self.final_results = final_results
        ep.generate_prod_react_image(self.final_results)
        for i in range(2 * len(self.final_results)):
            self.grid_columnconfigure(i, weight=1)
            if i % 2 == 0:
                light = open_image(
                    Path.cwd() / "assets" / "images" / f"{list(self.final_results.keys())[i // 2].name}_light.png"
                )
                dark = open_image(
                    Path.cwd() / "assets" / "images" / f"{list(self.final_results.keys())[i // 2].name}_dark.png"
                )
            label = ctk.CTkLabel(
                self,
                text=(f"{list(self.final_results.values())[i // 2]}" if i % 2 == 1 else ""),
                image=(
                    ctk.CTkImage(
                        light_image=light,
                        dark_image=dark,
                        size=(light.size[0] / light.size[1] * 15, 15),
                    )
                    if i % 2 == 0
                    else None
                ),
            )
            label.grid(row=0, column=i, padx=10, pady=10)
        self.pack(padx=20, pady=10, fill="x")


def open_image(image_path: Path) -> Image.Image:
    try:
        with Image.open(image_path) as img:
            return img.copy()
    except FileNotFoundError:
        return Image.open(Path.cwd() / "assets" / "images" / "default.png")


def run():
    App().mainloop()
    for file in Path.cwd().glob("assets/images/*.png"):
        if file.name != "default.png":
            file.unlink()
