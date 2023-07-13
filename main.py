import json
import time
import tkinter as tk
from PIL import Image, ImageTk


def add_money(button='+'):
    global add_money_flag, add_money_frame, coins_label_amount, my_games_frame, my_games_flag
    if not add_money_flag and button == '+':
        add_money_frame.place(in_=win, anchor="center", relx=.5, rely=.5)
        add_money_flag = True
        games_main_frame.forget()
        my_games_frame.forget()
        user_data["money"] += 10
        coins_amount = int(coins_label_amount["text"]) + 10
        coins_label_amount.configure(text=coins_amount)
        with open("user_data.json", "w") as f:
            json.dump(user_data, f)
    elif button == "OK":
        add_money_frame.place_forget()
        add_money_flag = False
        if my_games_flag:
            my_games_frame.pack(expand=True, fill="both")
        else:
            games_main_frame.pack(expand=True, fill="both")


def create_price_btn(price, text, game_index_, game_name_frame_, is_owned=False):
    global buy_buttons_list, my_games_btn_list
    button = tk.Button(game_name_frame_, text=text, background="#0e1d36", foreground="gray",
                       font=("Helvetica", 17),
                       wraplength=270)

    button.configure(command=lambda: buy_game(price, game_index_, is_owned))
    if is_owned:
        my_games_btn_list.append(button)
    else:
        buy_buttons_list.append(button)
    button.pack(side="bottom")


def buy_game(price, game_index_, my_games_page=False):
    global user_data, money_info_label
    with open("user_data.json") as user_file_:
        user_data = json.load(user_file_)
    buying_game: int = games_list[game_index_]["id"]
    if user_data["money"] >= price and buying_game not in user_data["games"] and buying_game not in user_data[
        "deleted_games"]:
        user_games: list = user_data["games"]
        user_data["money"] -= price
        user_games.append(games_list[game_index_]["id"])
        coins_amount = int(coins_label_amount["text"]) - price
        coins_label_amount.configure(text=coins_amount)
        buy_buttons_list[game_index_].configure(text="Удалить")
        money_info_label.configure(text="Игра успешно куплена", background="#117804")
        money_info_label.place(in_=games_main_frame, relx=0.5, rely=0.90, anchor="n",)
        # money_info_label.pack(pady=35, ipadx=10, ipady=10)
        win.after(2000, lambda: money_info_label.place_forget())

    elif buying_game in user_data["deleted_games"]:
        user_data["deleted_games"].remove(game_index_)
        user_data["games"].append(game_index_)
        buy_buttons_list[game_index_].configure(text="Удалить")
        load_my_games("installed")
    elif buying_game in user_data["games"]:
        user_data["games"].remove(game_index_)
        user_data["deleted_games"].append(game_index_)
        buy_buttons_list[game_index_].configure(text="Добавить")
    elif user_data["money"] < price:
        money_info_label.configure(text="Недостаточно средств", background="#c20d04")
        money_info_label.place(in_=games_main_frame, relx=0.5, rely=0.90, anchor="n",)
        win.after(2000, lambda: money_info_label.place_forget())
        return

    with open("user_data.json", 'w') as file:
        json.dump(user_data, file)

    if my_games_page:
        load_my_games("installed")
        load_my_games("deleted")


def switch_page(button, frames, is_owned=False):
    global page_count, current_games_frame, current_my_games_frame
    if button == '+':
        if page_count + 1 >= len(frames):
            return
        page_count += 1
    elif button == '-':
        if page_count - 1 < 0:
            return
        page_count -= 1

    if is_owned:
        current_my_games_frame.forget()
        current_my_games_frame = frames[page_count]
        current_my_games_frame.pack(expand=True)

        return
    current_games_frame.forget()
    current_games_frame = frames[page_count]
    current_games_frame.pack(expand=True)


def my_games():
    global my_games_flag
    if not my_games_flag:
        games_main_frame.forget()
        my_games_frame.pack(expand=True, fill="both")
        switch_page_button.configure(text="Все игры")
        my_games_flag = True
        load_my_games("installed")
        load_my_games("deleted")
    else:
        my_games_frame.forget()
        games_main_frame.pack(expand=True, fill="both")
        switch_page_button.configure(text="Мои игры")
        my_games_flag = False


def switch_my_games(button):
    if button == "installed":
        deleted_games_frame.forget()
        installed_games_frame.pack(expand=True, fill="both")
        my_games_title.configure(text="Установленные игры:")
    else:
        deleted_games_frame.pack(expand=True, fill="both")
        installed_games_frame.forget()
        my_games_title.configure(text="Удалённые игры:")


def show_game(game_frame_, image_, game_name_, game_price_, game_index_, is_owned=False):
    image_label = tk.Label(game_frame_, image=image_, background="#0e1d36")
    image_label.pack()
    image_label.image = image_
    game_name_frame = tk.Frame(game_frame_, background="#0e1d36")
    buy_button_text: str = "Купить"
    if (is_owned or game_index in user_data["games"]) and game_index_ not in user_data["deleted_games"]:
        buy_button_text = "Удалить"
    elif game_price_ == 0 or game_index_ in user_data["deleted_games"]:
        buy_button_text = "Добавить"
    tk.Label(game_name_frame, text=f"{game_name_}", background="#0e1d36", foreground="gray",
             font=("Helvetica", 17), wraplength=270).pack()
    tk.Label(game_name_frame, text=f"{game_price_}$", background="#0e1d36", foreground="white",
             font=("Helvetica", 17), wraplength=270).pack()
    create_price_btn(game_price_, buy_button_text, games_list[game_index_]["id"], game_name_frame, is_owned)
    game_name_frame.pack(fill="both", padx=10, expand=True)
    game_frame_.pack(side="left", padx=30, fill="both", expand=True)


with open("games.json", 'r', encoding="utf-8") as games_file:
    games_list = json.load(games_file)

with open("user_data.json") as user_file:
    user_data = json.load(user_file)

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

coins_label_amount = tk.Label(top_bar, text=user_data["money"], background="#0e1d36", font=20, foreground="yellow")

coins_label_amount.pack(side=tk.LEFT)
tk.Label(top_bar, text="$", background="#0e1d36", font=20, foreground="yellow").pack(side="left")

coins_amount_add = tk.Button(top_bar, text="+", background="#1a3259", font=("Helvetica", 17), foreground="gray",
                             command=lambda: add_money())
coins_amount_add.pack(side="left", ipadx=10, padx=10)
tk.Label(top_bar, background="#0e1d36").pack(side="left", padx=20)
tk.Label(top_bar, text="В вашей библиотеке ", background="#0e1d36", font=40, foreground="gray").pack(side="left")
games_amount = tk.Label(top_bar, text="0", background="#0e1d36", font=40, foreground="gray")
games_amount.pack(side="left")

tk.Label(top_bar, text=" игр", background="#0e1d36", font=40, foreground="gray").pack(side="left")

my_games_flag = False
switch_page_button = tk.Button(top_bar, text="Мои игры", background="#1a3259", font=40, foreground="gray",
                               command=lambda: my_games())
switch_page_button.pack(side="right", padx=40)
top_bar.pack(fill="x")

# ADD MONEY

add_money_image = tk.PhotoImage(file="images/add_money.png").subsample(2)
add_money_flag = False
add_money_frame = tk.Frame(win)
add_money_label = tk.Label(add_money_frame, image=add_money_image)
add_money_label.pack()
tk.Label(add_money_frame, text="Но так уж и быть! Дам тебе 10$", font=("Helvetica", 20)).pack()
close_money_btn = tk.Button(add_money_frame, text="OK", font=20, background="black", foreground="gray",
                            command=lambda: add_money('OK'))
close_money_btn.pack(ipadx=10, ipady=10, pady=10)

# Games menu

games_main_frame = tk.Frame(win, background="#02070f")

tk.Button(games_main_frame, text="<", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page('-', games_frames)).place(
    anchor="center", relheight=0.5, relx=0.02, rely=0.5)
games_main_frame.pack(expand=True, fill="both")
tk.Button(games_main_frame, text=">", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page('+', games_frames)).place(
    anchor="center", relheight=0.5, relx=0.98, rely=0.5)

games_frames = []

buy_buttons_list = []

for i in range(len(games_list)):
    if i % 3 == 0:
        games_frames.append(tk.Frame(games_main_frame, background="#02070f"))
    games_list[i]["frame"] = len(games_frames)
    game_frame = tk.Frame(games_frames[-1], height=350, width=300, background="#0e1d36")
    image = ImageTk.PhotoImage(Image.open(games_list[i]["image"]).resize((300, 300)))
    game_name = games_list[i]["name"]
    game_price = games_list[i]["price"]
    game_index = games_list[i]["id"]
    show_game(game_frame, image, game_name, game_price, game_index)

current_games_frame: tk.Frame = games_frames[0]
current_games_frame.pack(expand=True)

money_info_label = tk.Label(games_main_frame, text="Недостаточно средств.", font=("Helvetica", 20), foreground="white")

page_count = 0

# MY Games

my_games_frame = tk.Frame(win, background="#02070f")
my_games_btn_frame = tk.Frame(my_games_frame, background="#02070f")
my_games_btn_frame.pack(fill="x", pady=30)
tk.Button(my_games_btn_frame, text="Установленные игры", background="#1a3259", font=40, foreground="gray",
          command=lambda: (switch_my_games("installed"), load_my_games("installed"))).pack(side="left", padx=25)
tk.Button(my_games_btn_frame, text="Удалённые игры", background="#1a3259", font=40, foreground="gray",
          command=lambda: (switch_my_games("deleted"), load_my_games("deleted"))).pack(side="left")
my_games_title = tk.Label(my_games_frame, text="Установленные игры:", foreground="white", font=("Helvetica", 20),
                          background="#02070f", anchor="w")
my_games_title.pack(padx=25, fill="x")
installed_games_frame = tk.Frame(my_games_frame, background="#02070f")
installed_games_frame.pack(expand=True, fill="both")
tk.Button(installed_games_frame, text="<", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page('-', installed_games_frames, True)).place(
    anchor="center", relheight=0.5, relx=0.02, rely=0.5)
tk.Button(installed_games_frame, text=">", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page('+', installed_games_frames, True)).place(
    anchor="center", relheight=0.5, relx=0.98, rely=0.5)
installed_games_frames = []

deleted_games_frame = tk.Frame(my_games_frame, background="#02070f")
tk.Button(deleted_games_frame, text="<", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page('-', deleted_games_frames, True)).place(
    anchor="center", relheight=0.5, relx=0.02, rely=0.5)
tk.Button(deleted_games_frame, text=">", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page('+', deleted_games_frames, True)).place(
    anchor="center", relheight=0.5, relx=0.98, rely=0.5)
deleted_games_frames = []

my_games_btn_list = []

# deleted_games_frame.pack()
current_my_games_frame = None


def load_my_games(game_type):
    """
    :param game_type: "installed" or "deleted"
    """
    global page_count, current_my_games_frame
    page_count = 0
    my_games_btn_list.clear()
    with open("user_data.json") as file:
        user_data_ = json.load(file)
    installed_games_index = user_data_["games"]
    deleted_games_index = user_data_["deleted_games"]
    if game_type == "installed":
        [fr.destroy() for fr in installed_games_frames]
        installed_games_frames.clear()
        games_list_ = [el for el in games_list if el["id"] in installed_games_index]
        games_frames_ = installed_games_frames
        page_frame = installed_games_frame
        if not installed_games_index:
            return
    else:
        [fr.destroy() for fr in deleted_games_frames]
        deleted_games_frames.clear()
        games_list_ = [el for el in games_list if el["id"] in deleted_games_index]
        games_frames_ = deleted_games_frames
        page_frame = deleted_games_frame
        if not deleted_games_index:
            return
    for index in range(len(games_list_)):
        if index % 3 == 0:
            games_frames_.append(tk.Frame(page_frame, background="#02070f"))

        game_frame_ = tk.Frame(games_frames_[-1], height=350, width=300, background="#0e1d36")
        image_ = ImageTk.PhotoImage(Image.open(games_list_[index]["image"]).resize((300, 300)))
        game_name_ = games_list_[index]["name"]
        game_price_ = games_list_[index]["price"]
        game_index_ = games_list_[index]["id"]
        show_game(game_frame_, image_, game_name_, game_price_, game_index_, True)
    current_my_games_frame = games_frames_[0]
    current_my_games_frame.pack(expand=True)


# for i in range(len(games_list)):
#     if i % 3 == 0:
#         games_frames.append(tk.Frame(games_main_frame, background="#02070f"))
#     games_list[i]["frame"] = len(games_frames)
#     game_frame = tk.Frame(games_frames[-1], height=350, width=300, background="#0e1d36")
#     image = ImageTk.PhotoImage(Image.open(games_list[i]["image"]).resize((300, 300)))
#     game_name = games_list[i]["name"]
#     game_price = games_list[i]["price"]
#     game_index = games_list[i]["id"]
#     show_game(game_frame, image, game_name, game_price, game_index)
#
# current_games_frame: tk.Frame = games_frames[0]
# current_games_frame.pack(expand=True)
#
# page_count = 0


win.mainloop()
