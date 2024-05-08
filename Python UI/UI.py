import tkinter as tk
import customtkinter
import requests
from bs4 import BeautifulSoup
import time

def check_substrings(input_string):
    substrings = [
        "epc[00 00 01 35 69 103 137 171 205 239 01 35 ]",
        "epc[226 00 66 014 129 176 100 23 04 164 160 135 ]",
        #apples
        "epc[226 00 66 014 129 112 100 23 04 164 160 131 ]",
        "epc[226 00 66 014 31 240 100 23 04 164 154 107 ]",
        #oranges
        "epc[226 00 66 014 227 48 100 23 04 164 166 159 ]",
        "epc[226 00 66 014 129 48 100 23 04 164 160 127 ]",
        #mangos
        "epc[226 00 66 014 31 176 100 23 04 164 154 103 ]",
        "epc[226 00 66 014 31 112 100 23 04 164 154 99 ]",
        #bananas
        "epc[226 00 66 013 189 240 100 23 04 164 148 75 ]",
        "epc[226 00 66 014 129 240 100 23 04 164 160 139 ]"
        #strawberries
    ]

    fruits = {
    "apples": 0,
    "oranges": 0,
    "mangos": 0,
    "bananas": 0,
    "strawberries": 0
    }
    for i in range(0, len(substrings)):
        if substrings[i] in input_string:
            if i < 2:
                fruits["apples"] += 1
            elif i < 4:
                fruits["oranges"] += 1
            elif i < 6:
                fruits["mangos"] += 1
            elif i < 8:
                fruits["bananas"] += 1
            elif i < 10:
                fruits["strawberries"] += 1

    total_fruits = sum(fruits.values())
    print(f"{total_fruits} fruit(s) found")
    label.config(text=f"{total_fruits} fruit(s) found")
    apples.config(text=f"{fruits['apples']} apples found")
    oranges.config(text=f"{fruits['oranges']} oranges found")
    mangos.config(text=f"{fruits['mangos']} mangos found")
    bananas.config(text=f"{fruits['bananas']} bananas found")
    strawberry.config(text=f"{fruits['strawberries']} strawberries found")

def button_callback():
    print("Button click", combobox_1.get())


def slider_callback(value):
    progressbar_1.set(value)


def update_gui():
    # Read HTML from the link
    response = requests.get('http://pcr.bounceme.net/test/RFID/sampletest.html')
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the relevant HTML data
    
    
    # Update the GUI label with the new data
    #label.config(text=soup.prettify())
    check_substrings(soup.prettify())
    # Schedule the next update after 5 seconds
    root.after(1000, update_gui)

# Create the main window
root = customtkinter.CTk()
root.geometry("400x580")
root.title("RFID Notification")
customtkinter.set_appearance_mode("dark") # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue") # Themes: "blue" (standard), "green", "dark-blue"

frame_1 = customtkinter.CTkFrame(master=root)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
progressbar_1.pack(pady=12, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback)
button_1.pack(pady=12, padx=10)

slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_callback, from_=0, to=1)
slider_1.pack(pady=12, padx=10)
slider_1.pack(pady=12, padx=10)

#root.configure(bg='gray')
# Create a label to display the HTML data
label = tk.Label(root, font=("Arial", 24), bg='#333333', fg='blue')
label.pack(pady=20)

apples = tk.Label(root, font=("Arial", 24), bg='#333333', fg='green')
apples.pack(pady=20)

oranges = tk.Label(root, font=("Arial", 24), bg='#333333', fg='orange')
oranges.pack(pady=20)

mangos = tk.Label(root, font=("Arial", 24), bg='#333333', fg='yellow')
mangos.pack(pady=20)

bananas = tk.Label(root, font=("Arial", 24), bg='#333333', fg='yellow')
bananas.pack(pady=20)

strawberry = tk.Label(root, font=("Arial", 24), bg='#333333', fg='red')
strawberry.pack(pady=20)

# Start the GUI update loop
update_gui()

# Run the main event loop
root.mainloop()
