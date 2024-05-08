import tkinter as tk
import customtkinter
import requests
from bs4 import BeautifulSoup
import time



def button_callback():
    print("Button click", combobox_1.get())


def slider_callback(value):
    progressbar_1.set(value)


def update_gui():
    # Read HTML from the link
    response = requests.get('http://pcr.bounceme.net/test/RFID/Notification.html')
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the relevant HTML data
    
    
    # Update the GUI label with the new data
    label.config(text=soup.prettify())
    
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

# Start the GUI update loop
update_gui()

# Run the main event loop
root.mainloop()