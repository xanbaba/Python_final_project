import json
import tkinter as tk
from PIL import Image, ImageTk


# Functions

def get_user_data(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def uptade_user_data(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file)


def switch_my_games():
    global my_games_flag
    if my_games_flag:
        games_main_frame.pack(expand=True, fill="both")
        my_games_main_frame.pack_forget()
        switch_page_button.configure(text="Мои игры")
        my_games_flag = False
    else:
        games_main_frame.pack_forget()
        my_games_main_frame.pack(expand=True, fill="both")
        switch_page_button.configure(text="Все игры")
        my_games_flag = True


def get_games(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def add_money(action="open"):
    """
    :param action: "open" or "close"
    """
    global user_data, coins_label_amount, add_money_flag
    if action == "open" and not add_money_flag:
        add_money_frame.place(in_=win, anchor="center", relx=.5, rely=.5)
        # games_main_frame.pack_forget()
        add_money_frame.lift()

        user_data["money"] += 10
        uptade_user_data(user_data_filename, user_data)

        coins_label_amount.configure(text=user_data["money"])

        add_money_flag = True

    elif add_money_flag and action == "close":
        add_money_frame.place_forget()
        # games_main_frame.pack(expand=True, fill="both")
        add_money_flag = False


def buy_game(price, index, buttons_list):
    user_money = user_data["money"]
    if index in user_data["games"]:
        buttons_list[index].configure(text="Добавить")
        user_data["games"].remove(index)
        user_data["deleted_games"].append(index)
        games_amount.configure(text=int(games_amount["text"]) - 1)
    elif index in user_data["deleted_games"]:
        buttons_list[index].configure(text="Удалить")
        user_data["games"].append(index)
        user_data["deleted_games"].remove(index)
        games_amount.configure(text=int(games_amount["text"]) + 1)
    else:
        if user_money >= price:
            buttons_list[index].configure(text="Удалить")
            user_data["games"].append(index)
            user_data["money"] -= price
            coins_label_amount.configure(text=int(coins_label_amount["text"]) - price)
            games_amount.configure(text=int(games_amount["text"]) + 1)

            money_info_label.configure(text="Игра успешно куплена", background="#117804")

            money_info_label.place(in_=games_main_frame, relx=0.5, rely=0.90, anchor="n", )
            win.after(2000, lambda: money_info_label.place_forget())
        else:
            money_info_label.configure(text="Недостаточно средств", background="#c20d04")
            money_info_label.place(in_=games_main_frame, relx=0.5, rely=0.90, anchor="n", )
            win.after(2000, lambda: money_info_label.place_forget())

    uptade_user_data(user_data_filename, user_data)


def create_game_frames(games_list, main_frame, frames, buttons_list, is_owned=False, page_index=0,
                       load_type="installed"):
    """

    :param load_type: shows which owned frame load
    :param page_index: index of visible page
    :param is_owned: shows if player already bought the games in the frame
    :param buttons_list: list where to save buttons
    :param games_list: list of games which will be added
    :param main_frame: frame where all pages will be writen
    :param frames: list where to save added frames
    """

    for i in range(len(games_list)):
        if i % 3 == 0:
            frames.append(tk.Frame(main_frame, background="#02070f"))
        frame = tk.Frame(frames[-1], height=350, width=300, background="#0e1d36")
        image = ImageTk.PhotoImage(Image.open(games_list[i]["image"]).resize((300, 300)))
        name = games_list[i]["name"]
        price = games_list[i]["price"]
        index = games_list[i]["id"]

        show_game(frame, image, name, price, index, buttons_list, is_owned, load_type)

    try:
        frames[page_index].pack(expand=True)
    except IndexError:
        try:
            frames[page_index - 1].pack(expand=True)
        except IndexError:
            pass


def show_game(frame, image, name, price, index, buttons_list, is_owned=False, load_type="installed"):
    image_label = tk.Label(frame, image=image, background="#0e1d36")
    image_label.pack()
    image_label.image = image

    game_name_frame = tk.Frame(frame, background="#0e1d36")
    game_name_frame.pack(fill="both", padx=10, expand=True)

    tk.Label(game_name_frame, text=f"{name}", background="#0e1d36", foreground="gray",
             font=("Helvetica", 17), wraplength=270).pack()
    tk.Label(game_name_frame, text=f"{price}$", background="#0e1d36", foreground="white",
             font=("Helvetica", 17), wraplength=270).pack()
    button_title = "Купить"
    if index in user_data["games"]:
        button_title = "Удалить"
    elif index in user_data["deleted_games"] or price == 0:
        button_title = "Добавить"

    if is_owned:
        buttons_list[index] = tk.Button(game_name_frame, text=button_title, background="#0e1d36", foreground="gray",
                                        font=("Helvetica", 17),
                                        wraplength=270)

        if load_type == "installed":
            buttons_list[index].configure(command=lambda: (buy_game(price, index, buttons_list),
                                                           load_my_games(installed_games_frame, installed_games_frames,
                                                                         installed_buttons_list, load_type="installed",
                                                                         page_count=installed_games_count)))
        else:
            buttons_list[index].configure(command=lambda: (buy_game(price, index, buttons_list),
                                                           load_my_games(deleted_games_frame, deleted_games_frames,
                                                                         deleted_buttons_list, load_type="deleted",
                                                                         page_count=deleted_games_count)))
        buttons_list[index].pack(side="bottom")
    else:

        buttons_list.append(
            tk.Button(game_name_frame, command=lambda: buy_game(price, index, buttons_list), text=button_title,
                      background="#0e1d36", foreground="gray", font=("Helvetica", 17),
                      wraplength=270))
        buttons_list[-1].pack(side="bottom")

    frame.pack(side="left", padx=30, fill="both", expand=True)


def switch_page(frames, frames_type, button, count):
    """
    :param frames: list of frames
    :param frames_type: "all", "installed" or "deleted"
    :param button: '+' or '-'
    :param count: variable for detecting where is the switch now
    :return:
    """
    global all_games_count, installed_games_count, deleted_games_count

    if button == '+':
        if count + 1 >= len(frames):
            print(1)
            return
        frames[count].pack_forget()
        count += 1

    elif button == '-':
        print(count, frames_type, installed_games_count)
        if count - 1 < 0:
            print(2)
            return
        frames[count].pack_forget()
        count -= 1

    if frames_type == "all":
        all_games_count = count
    elif frames_type == "installed":
        installed_games_count = count
    else:
        deleted_games_count = count

    frames[count].pack(expand=True)


def load_my_games(main_frame, frames, buttons_list, load_type="installed", page_count=0):
    """
    :param page_count: index of visible page
    :param main_frame: frame where all pages will be writen
    :param frames: list where to save added frames
    :param buttons_list: list where to save buttons
    :param load_type: "deleted" or "installed"
    """

    global installed_games_count, deleted_games_count
    [frame.destroy() for frame in frames]
    frames.clear()
    if load_type == "installed":
        games_indexes = user_data["games"]
        deleted_games_frame.pack_forget()
        installed_games_count = 0
    else:
        games_indexes = user_data["deleted_games"]
        installed_games_frame.pack_forget()
        deleted_games_count = 0

    games_list = []
    for index in games_indexes:
        games_list.append(games_data[index])

    create_game_frames(games_list, main_frame, frames, buttons_list, True, page_count, load_type)
    main_frame.pack(expand=True, fill="both")


win = tk.Tk()
win.state("zoomed")
win.title("Steam 2.0")

win.geometry("{}x{}".format(win.winfo_screenwidth(), win.winfo_screenheight()))
win['background'] = "#02070f"

user_data_filename = "user_data.json"
user_data = get_user_data(user_data_filename)

games_data_filename = "games.json"
games_data = get_games(games_data_filename)

# TOP BAR

top_bar = tk.Frame(win, height=70, background="#0e1d36")

coins_image = tk.PhotoImage(file="images/coins.png").subsample(10)

coins_label_image = tk.Label(top_bar, image=coins_image, background="#0e1d36")
coins_label_image.pack(side="left", ipadx=20)

coins_label_amount = tk.Label(top_bar, text=user_data["money"], background="#0e1d36", font=20, foreground="yellow")
coins_label_amount.pack(side=tk.LEFT)
tk.Label(top_bar, text="$", background="#0e1d36", font=20, foreground="yellow").pack(side="left")

coins_amount_add = tk.Button(top_bar, text="+", background="#1a3259", font=("Helvetica", 17),
                             command=lambda: add_money(), foreground="gray")
coins_amount_add.pack(side="left", ipadx=10, padx=10)

tk.Label(top_bar, text="В вашей библиотеке ", background="#0e1d36", font=40, foreground="gray").pack(side="left")
games_amount = tk.Label(top_bar, text=f"{len(user_data['games'])}", background="#0e1d36", font=40, foreground="gray")
games_amount.pack(side="left")
tk.Label(top_bar, text=" игр", background="#0e1d36", font=40, foreground="gray").pack(side="left")

switch_page_button = tk.Button(top_bar, text="Мои игры", background="#1a3259", font=40, foreground="gray",
                               command=switch_my_games)
switch_page_button.pack(side="right", padx=40)

top_bar.pack(fill="x")

# ADD MONEY

add_money_flag = False

add_money_image = tk.PhotoImage(file="images/add_money.png").subsample(2)
add_money_frame = tk.Frame(win)

add_money_label = tk.Label(add_money_frame, image=add_money_image)
add_money_label.pack()

tk.Label(add_money_frame, text="Но так уж и быть! Дам тебе 10$", font=("Helvetica", 20)).pack()

close_money_btn = tk.Button(add_money_frame, text="OK", font=20, background="black", foreground="gray",
                            command=lambda: add_money("close"))
close_money_btn.pack(ipadx=10, ipady=10, pady=10)

# add_money_frame.place(in_=win, anchor="center", relx=.5, rely=.5)


# GAMES MENU

games_main_frame = tk.Frame(win, background="#02070f")
games_main_frame.pack(expand=True, fill="both")

tk.Button(games_main_frame, text="<", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page(games_frames, "all", '-', all_games_count)).place(
    anchor="center", relheight=0.5, relx=0.02, rely=0.5)
tk.Button(games_main_frame, text=">", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page(games_frames, "all", '+', all_games_count)).place(
    anchor="center", relheight=0.5, relx=0.98, rely=0.5)

games_frames = list()

all_games_count = 0

all_buttons_list = list()

create_game_frames(games_data, games_main_frame, games_frames, all_buttons_list)

money_info_label = tk.Label(games_main_frame, text="Недостаточно средств.", font=("Helvetica", 20), foreground="white")

# MY GAMES MENU

my_games_main_frame = tk.Frame(win, background="#02070f")
# my_games_main_frame.pack(expand=True, fill="both")

my_games_flag = False

my_games_btn_frame = tk.Frame(my_games_main_frame, background="#02070f")
my_games_btn_frame.pack(fill="x", pady=30)

tk.Button(my_games_btn_frame, text="Установленные игры", background="#1a3259", font=40, foreground="gray",
          command=lambda: load_my_games(installed_games_frame, installed_games_frames, installed_buttons_list)).pack(
    side="left", padx=25)
tk.Button(my_games_btn_frame, text="Удалённые игры", background="#1a3259", font=40, foreground="gray",
          command=lambda: load_my_games(deleted_games_frame, deleted_games_frames, deleted_buttons_list,
                                        load_type="deleted")) \
    .pack(side="left", padx=25)

my_games_title = tk.Label(my_games_main_frame, text="Установленные игры:", foreground="white", font=("Helvetica", 20),
                          background="#02070f", anchor="w")
my_games_title.pack(padx=25, fill="x")

installed_games_frame = tk.Frame(my_games_main_frame, background="#02070f")
installed_games_frame.pack(expand=True, fill="both")

tk.Button(installed_games_frame, text="<", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page(installed_games_frames, "installed", '-', installed_games_count)).place(
    anchor="center", relheight=0.5, relx=0.02, rely=0.5)
tk.Button(installed_games_frame, text=">", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page(installed_games_frames, "installed", '+', installed_games_count)).place(
    anchor="center", relheight=0.5, relx=0.98, rely=0.5)

installed_games_frames = []
installed_buttons_list = {}
installed_games_count = 0

deleted_games_frame = tk.Frame(my_games_main_frame, background="#02070f")

tk.Button(deleted_games_frame, text="<", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page(deleted_games_frames, "deleted", '-', deleted_games_count)).place(
    anchor="center", relheight=0.5, relx=0.02, rely=0.5)
tk.Button(deleted_games_frame, text=">", background="#1a3259", font=40, foreground="gray",
          command=lambda: switch_page(deleted_games_frames, "deleted", '+', deleted_games_count)).place(
    anchor="center", relheight=0.5, relx=0.98, rely=0.5)

deleted_games_frames = []
deleted_buttons_list = {}
deleted_games_count = 0

load_my_games(installed_games_frame, installed_games_frames, installed_buttons_list)

win.mainloop()
