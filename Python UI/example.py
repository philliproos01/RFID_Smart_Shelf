import tkinter
import customtkinter
import requests 
from bs4 import BeautifulSoup 

r = requests.get('http://pcr.bounceme.net/test/RFID/Notification.html') 
  
# check status code for response received 
# success code - 200 
print(r) 
  
# Parsing the HTML 
soup = BeautifulSoup(r.content, 'html.parser') 
print(soup.prettify()) 

customtkinter.set_appearance_mode("dark") # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue") # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry ("400x580")
app.title("SmartShelf GUI")


def button_callback():
    print("Button click", combobox_1.get())


def slider_callback(value):
    progressbar_1.set(value)


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

Label_1 = customtkinter.CTkLabel(master=frame_1, text=soup.prettify(), justify=tkinter.LEFT)
Label_1.pack(pady=12, padx=10)

progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
progressbar_1.pack(pady=12, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback)
button_1.pack(pady=12, padx=10)

slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_callback, from_=0, to=1)
slider_1.pack(pady=12, padx=10)
slider_1.pack(pady=12, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="CTkEntry")
entry_1.pack(pady=12, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, values=["Option 1", "Option 2", "Option 42 long long Long..."])
optionmenu_1.pack(pady=12, padx=10)
optionmenu_1.set("CTkOptionMenu")

combobox_1 = customtkinter.CTkComboBox(frame_1, values=["Option 1", "Option 2", "Option 42 long long Long..."])
combobox_1.pack(pady=12, padx=10)
optionmenu_1.set("CTkComboBox")

checkbox_1 = customtkinter.CTkCheckBox(master=frame_1)
checkbox_1.pack(pady=12, padx=10)

radiobutton_var = tkinter.IntVar(value=1)

radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=1)
radiobutton_1.pack(pady=12, padx=10)

radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=2)
radiobutton_2.pack(pady=12, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1)
switch_1.pack(pady=12, padx=10)

app.mainloop()