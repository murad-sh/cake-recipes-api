import tkinter as tk
from source.lib.api.api_client import CakeAPI
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from tkinter import messagebox
import requests
import io
import ttkbootstrap as ttk

# initial image
url = "https://i.etsystatic.com/9461176/r/il/b61cd7/3252469986/il_1140xN.3252469986_fh7t.jpg"


class GUIApplication:
    def __init__(self, key):
        self.cake_api = CakeAPI(key)
        self.root = ttk.Window()
        self.style = ttk.Style('minty')
        self.root.title("Cake Recipes App")
        self.root.geometry("1000x700")

        # main label frame
        self.label_frame = tk.Frame(self.root)
        self.label = tk.Label(self.label_frame, text="Cake Recipes", font=("Ariel", 30))
        self.label.pack(pady=20, side="left")
        self.label_frame.pack()

        # cakes list frame
        self.cakes_list_frame = tk.Frame(self.root)
        self.scrollbar = tk.Scrollbar(self.cakes_list_frame, orient="vertical")
        self.cakes_box = tk.Listbox(self.cakes_list_frame, width=80, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.cakes_box.yview)
        self.cakes_list_frame.pack(padx=30, pady=10)
        self.cakes_box.pack(pady=15, padx=10, side="left")
        self.scrollbar.pack(side='right', fill="y")
        self.cakes = []

        # button frame
        self.button_frame = tk.Frame(self.root)
        self.button = tk.Button(self.button_frame, text="Get recipe", font=("Ariel", 16),
                                command=lambda: self.get_recipe())
        self.button.pack(side="left")
        self.button_frame.pack()

        # recipe frame
        self.recipe_frame = tk.Frame(self.root)
        self.recipe_output = ScrolledText(self.recipe_frame, wrap="word")
        self.recipe_output.pack(side="left", pady=15)

        # image label
        self.url = ""
        self.init_image = self.get_image_by_url(url)
        self.image_label = tk.Label(self.recipe_frame, image=self.init_image)
        self.image_label.pack(pady=15, padx=10, side="left")
        self.recipe_frame.pack()

        self.get_cakes()

        self.root.mainloop()

    def get_cakes(self):
        self.cakes = self.cake_api.get_cakes_list()
        for cake in self.cakes:
            self.cakes_box.insert(tk.END, f"{cake.get_id()}. {cake.get_title()} , Difficulty: {cake.get_difficulty()}")

    def get_recipe(self):
        if self.cakes_box.get(tk.ACTIVE) == "":
            messagebox.showwarning("No Cake Selected", "Please choose a cake first.")
            return
        else:
            self.recipe_output.delete('1.0', tk.END)
            selected_item = self.cakes_box.get(tk.ACTIVE)
            id = selected_item.split(".")[0].strip()
            self.update_photo(id)
            recipe = self.cake_api.get_recipe_by_id(id)
            recipe_text = f"Recipe Title: {recipe.get_title()}\n"
            recipe_text += f"Portion: {recipe.get_portion()}\n"
            recipe_text += f"Time: {recipe.get_time()}\n"
            recipe_text += f"Description: {recipe.get_description()}\n\n"

            recipe_text += "Ingredients:\n"
            for ingredient in recipe.get_ingredients():
                recipe_text += f"- {ingredient}\n"

            recipe_text += "\nMethod:\n"
            for step in recipe.get_method():
                for key, value in step.items():
                    recipe_text += f"{key}: {value}\n"

            self.recipe_output.configure(state='normal')
            self.recipe_output.delete('1.0', tk.END)
            self.recipe_output.insert(tk.END, recipe_text)
            self.recipe_output.configure(state='disabled')

    def get_image_by_id(self, id):
        for cake in self.cakes:
            if cake.get_id() == id:
                return cake.get_image()

    @staticmethod
    def get_image_by_url(image_url):
        width = 200
        height = 200
        response = requests.get(image_url, stream=True)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((width, height))
        photo = ImageTk.PhotoImage(image)
        return photo

    def update_photo(self, id):
        global url
        url = self.get_image_by_id(id)
        image = self.get_image_by_url(url)
        self.image_label.configure(image=image)
        self.image_label.image = image


if __name__ == "__main__":
    API_KEY = "YOUR API KEY"
    app = GUIApplication(API_KEY)
