import tkinter as tk

from game.solo.bomberman_solo import BombermanSolo


def _get_online_players():
    return 1


class BombermanMenu(tk.Tk):

    """ Create the window for the menu of the game """

    def __init__(self):
        super().__init__()
        self.title('Bomberman')
        self.minsize(600, 500)
        self.resizable(False, False)
        self._create_widgets()

    def _create_widgets(self):

        """ Create a background and button for launching the game (Solo or Multiplayer) """

        self.background = tk.PhotoImage(file="sprites/entities/menu/background_menu.png")
        background_label = tk.Label(self, image=self.background)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.solo_button = tk.PhotoImage(file="sprites/entities/menu/solo_button.png")
        solo_button = tk.Button(self, image=self.solo_button, bd=0, highlightthickness=0, command=self._open_solo_game)
        solo_button.pack(pady=120, anchor="center")

        self.multiplayer_button = tk.PhotoImage(file="sprites/entities/menu/multiplayer_button.png")
        multiplayer_button = tk.Button(self, image=self.multiplayer_button, bd=0, highlightthickness=0)
        multiplayer_button.pack(anchor="center")

        show_online_players = tk.Label(self, text="Online players: " + str(_get_online_players()) + "/4",
                                       bg="green", font=("Arial", 16))
        show_online_players.pack(pady=20, anchor="center")

        show_movement = tk.Label(self, text="Move with Z, Q, S, D and Space for spawn a bomb", bg="gray", font=("Arial", 13))
        show_movement.pack()

        show_rules = tk.Label(self, text="Kill all enemies or players with bombs!", bg="gray", font=("Arial", 13))
        show_rules.pack()

        show_version = tk.Label(self, text="Version 1.0", font=("Arial", 13), highlightcolor="black")
        show_version.pack(side=tk.BOTTOM, padx=50)

    def _open_solo_game(self):

        """ Open the game in solo mode """

        self.quit()
        bomberman = BombermanSolo()
        bomberman.open_game()

    def quit(self):
        """ Close the window """

        # self.destroy()

    def open_game(self):
        """ Open the window """

        self.mainloop()
