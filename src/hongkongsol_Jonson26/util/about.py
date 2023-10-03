import tkinter as tk
import webbrowser
from threading import Thread

class About:
    def __init__(self):
        root = tk.Tk()
        root.title("About Hongkong Solitaire")
        ##root.geometry("800x800")

        labels = [tk.Label(root, text="                       Hongkong Solitaire                       "),
                  tk.Label(root, text="               Shenzhen Solitaire Clone in Python               "),
                  tk.Label(root, text="               All Assets (c) 2023 Filip Jamroga                "),
                  tk.Label(root, text="    All Code (c) 2023 Filip Jamroga, unless stated otherwise    "),
                  tk.Label(root, text="              spritesheet.py (c) 2019 Eric Matthes              "),
                  tk.Label(root, text="SHENZHEN SOLITAIRE is (c) 2016 Zachtronics. All rights reserved."),
                  tk.Label(root, text="================================================================")]
        for l in labels:
            l.pack()

        donatebutton = tk.Button(root, text="Donate!", command= lambda: self._link("https://www.paypal.com/donate/?hosted_button_id=5A6RVS9TKS6YY"))
        donatebutton.pack()

        root.update()
        root.mainloop()

    def _link(self, url):
        Thread(target= lambda: webbrowser.open_new_tab(url)).start()

if __name__ == "__main__":
    About()
