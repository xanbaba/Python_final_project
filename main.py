import json
import tkinter as tk
from PIL import Image, ImageTk


def add_money():
    global add_money_flag, add_money_frame
    if not add_money_flag:
        add_money_frame.place(in_=win, anchor="c", relx=.5, rely=.5)
        add_money_flag = True
        games_main_frame.forget()
    else:
        add_money_frame.place_forget()
        add_money_flag = False
        games_main_frame.pack(expand=True, fill="both")


def swith_page(button):
    global page_count, current_games_frame, games_frames
    if button == '+':
        if page_count + 1 >= len(games_frames):
            return
        page_count += 1
    elif button == '-':
        if page_count - 1 < 0:
            return
        page_count -= 1
    current_games_frame.forget()
    current_games_frame = games_frames[page_count]
    current_games_frame.pack(expand=True)


win = tk.Tk()
win.state("zoomed")
win.title("Steam 2.0")

win.geometry("{}x{}".format(win.winfo_screenwidth(), win.winfo_screenheight()))
win['background'] = "#02070f"

# Top Bar

top_bar = tk.Frame(win, height=70, background="#0e1d36")

coins_image = tk.PhotoImage(file="images/coins.png").subsample(10)
coins_label_image = tk.Label(top_bar, image=coins_image, background="#0e1d36")
coins_label_image.pack(side="left", ipadx=20)

coins_label_amount = tk.Label(top_bar, text="100", background="#0e1d36", font=20, foreground="yellow")

coins_label_amount.pack(side=tk.LEFT)
tk.Label(top_bar, text="$", background="#0e1d36", font=20, foreground="yellow").pack(side="left")

coins_amount_add = tk.Button(top_bar, text="+", background="#1a3259", font=40, foreground="gray",
                             command=lambda: add_money())
coins_amount_add.pack(side="left", ipadx=10, padx=10)
tk.Label(top_bar, background="#0e1d36").pack(side="left", padx=20)
tk.Label(top_bar, text="В вашей библиотеке ", background="#0e1d36", font=40, foreground="gray").pack(side="left")
games_amount = tk.Label(top_bar, text="0", background="#0e1d36", font=40, foreground="gray")
games_amount.pack(side="left")
tk.Label(top_bar, text=" игр", background="#0e1d36", font=40, foreground="gray").pack(side="left")

tk.Button(top_bar, text="Мои игры", background="#1a3259", font=40, foreground="gray").pack(side="right", padx=40)

top_bar.pack(fill="x")

# ADD MONEY

add_money_image = tk.PhotoImage(file="images/add_money.png").subsample(2)
add_money_flag = False
add_money_frame = tk.Frame(win)
add_money_label = tk.Label(add_money_frame, image=add_money_image)
add_money_label.pack()
tk.Label(add_money_frame, text="Но так уж и быть! Дам тебе 10$", font=("Helvetica", 20)).pack()
close_money_btn = tk.Button(add_money_frame, text="OK", font=20, background="black", foreground="gray",
                            command=lambda: add_money())
close_money_btn.pack(ipadx=10, ipady=10, pady=10)

# Games menu

games_main_frame = tk.Frame(win, background="#02070f")

with open("games.json", 'r', encoding="utf-8") as games_file:
    games_list = json.load(games_file)

games_frames = []

for i in range(len(games_list)):
    if i % 3 == 0:
        games_frames.append(tk.Frame(games_main_frame, background="#02070f"))
    games_list[i]["frame"] = len(games_frames)
    game_frame = tk.Frame(games_frames[-1], height=350, width=300)
    image = ImageTk.PhotoImage(Image.open(games_list[i]["image"]).resize((300, 300)))
    image_label = tk.Label(game_frame, text=i, image=image)
    image_label.pack()
    image_label.image = image
    game_frame.pack(side="left", padx=30)

current_games_frame: tk.Frame = games_frames[0]
current_games_frame.pack(expand=True)

page_count = 0
tk.Button(win, text="<", background="#1a3259", font=40, foreground="gray", command=lambda: swith_page('-')).place(
    anchor="center", relheight=0.5, relx=0.02, rely=0.5)
games_main_frame.pack(expand=True, fill="both")
tk.Button(win, text=">", background="#1a3259", font=40, foreground="gray", command=lambda: swith_page('+')).place(
    anchor="center", relheight=0.5, relx=0.98, rely=0.5)

win.mainloop()
