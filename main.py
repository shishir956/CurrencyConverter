from customtkinter import *
from PIL import Image
import requests
import json

try:
    API_KEY = '4946fa0e0e9a4745a1af6b3ca286f588'

    params = {
        "api_key": API_KEY,
        "base": 'USD',
    }

    response = requests.get("https://exchange-rates.abstractapi.com/v1/live", params=params)
    response.raise_for_status()
    data = response.json()

except:
    file = open('data_file.json')
    data = json.load(file)
    file.close()

text = ""
for values in data["exchange_rates"]:
    text = text+f"{values} : {data['exchange_rates'][values]}"+"\n"

options = [currency for currency in data["exchange_rates"]]

options.append("USD")
data["exchange_rates"]["USD"] = 1.0000

screen = CTk()
screen.configure(padx=10, pady=10)
screen.resizable(False, False)
screen.title("Currency Converter")
screen.geometry('400x300')
set_appearance_mode("dark")


def toggle_light():
    set_appearance_mode("light")
    change_theme.configure(command=toggle_dark, text="☀️")
    from_menu.configure(dropdown_hover_color="grey", dropdown_text_color="black")
    to_menu.configure(dropdown_hover_color="grey", dropdown_text_color="black")


def toggle_dark():
    set_appearance_mode("dark")
    change_theme.configure(command=toggle_light, text="🌒")
    from_menu.configure(dropdown_hover_color="black", dropdown_text_color="white")
    to_menu.configure(dropdown_hover_color="black", dropdown_text_color="white")


img1 = Image.open("exchange-dollar-fill (4).png")
img2 = Image.open("exchange-dollar-fill (5).png")

logo = CTkImage(light_image=img1, dark_image=img2, size=(50, 50))
logo_label1 = CTkLabel(screen, text="", image=logo)
logo_label1.place(x=170, y=30)

logo_label2 = CTkLabel(screen, text="Currency Converter", font=("Georgia", 20, "bold"))
logo_label2.place(x=100, y=80)

change_theme = CTkSwitch(screen, text="🌒", command=toggle_light, progress_color="#6495ED", switch_width=50)
change_theme.place(x=300, y=0)


clicked1 = StringVar()
clicked1.set("Currency")
from_label = CTkLabel(screen, text="From", width=100, font=("Georgia", 16, "bold"))
to_label = CTkLabel(screen, text="To", width=100, font=("Georgia", 16, "bold"))

from_label.place(x=30, y=120)
to_label.place(x=250, y=120)


currency1 = "USD"
currency2 = "USD"


clicked1 = StringVar(value="USD")
from_menu = CTkOptionMenu(screen, variable=clicked1, values=options, dropdown_hover_color="grey", width=100, font=("Algerian", 15, "bold"))
from_menu.place(x=30, y=150)


clicked2 = StringVar(value="USD")
to_menu = CTkOptionMenu(screen, variable=clicked2, values=options, dropdown_hover_color="grey", width=100, font=("Algerian", 15, "bold"))
to_menu.place(x=250, y=150)


to_convert = CTkEntry(screen, placeholder_text="Enter value")
to_convert.place(x=10, y=200)
to_convert.focus()

converted = CTkEntry(screen, placeholder_text="0", state='disabled')
converted.place(x=230, y=200)

# to_frame = CTkFrame(screen,width=130, height=30,fg_color="white")
# to_frame.place(x=230,y=200)


def ip():
    global currency1
    global currency2
    currency2 = to_menu.get()
    currency1 = from_menu.get()

    try:
        conversion_factor = data["exchange_rates"][currency2] / data["exchange_rates"][currency1]

        before = to_convert.get()
        before = before.split(".")
        if "." in before:
            before = float(before[0])+float(before[1])/(10**len(before[1]))

        else:
            before = int(before[0])

        after = before * conversion_factor
        # print(after)
        converted.configure(state="normal")
        converted.delete(0, END)
        converted.insert(0, f"{after}")
        converted.configure(state="disabled")

    except:
        top_level = CTkToplevel(screen)
        top_level.geometry('150x90')
        label = CTkLabel(top_level, text="Error\nPlease Make Valid Entries")
        label.pack()
        top_level.state('withdrawn')


def live_rate():
    top_level = CTkToplevel()
    top_level.state("zoomed")
    # top_level.geometry('1000x1000')
    frame = CTkFrame(top_level)
    frame.pack()
    labelx = CTkLabel(frame, anchor=NE, text=f"Base: USD\n\n\n\n{text}")
    labelx.pack()


button1 = CTkButton(screen, text="Convert", font=("Georgia", 16, "bold"), command=ip)
button1.place(x=120, y=250)

button2 = CTkButton(screen, text="Live Rates", command=live_rate, width=8)
button2.place(x=0, y=0)


screen.mainloop()
input()