import tkinter as tk
import customtkinter
import requests
from bs4 import BeautifulSoup
import time
#response = requests.get('http://pcr.bounceme.net/test/RFID/Notification.html')
response = requests.get('http://pcr.bounceme.net/test/RFID/sampletest.html')
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.prettify())
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

    for fruit, count in fruits.items():
        print(f"{count} {fruit} found")



"""
    substrings_found = 0
    for substring in substrings:
        if substring not in input_string:
            print(f"Substring not found: {substring}")
        else:
            print(f"Substring {substring} found")
            substrings_found += 1
    print(f"{substrings_found} substring(s) found")"""


#input_string = "This is a sample string that may or may not contain the specified substrings.epc[226 00 66 014 129 176 100 23 04 164 160 135 ]"
check_substrings(soup.prettify())
