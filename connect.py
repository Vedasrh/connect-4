"""

A simple two player "Connect Four" game with a gameboard that has 6 rows and 7
columns (6x7). Uses a class Connectfour to simulate the game and then class
Gameinterface to create a GUI, a window where the game operates. At the bottom
of the window is shown the current player and the color of their pawn.
In the GUI there is also a dropdown menu with the name "Menu" which consists of
options: New Game, Instructions and Quit. New game starts the game from the
beginning, Instructions tells how to play the game and Quit ends the program.
"""

from tkinter import *
from tkinter import messagebox

class Connectfour:
    """
    Connectfour simulates the game of "Connect Four".
    """

    def __init__(self, rows=6, columns=7, player_1="X", player_2="O"):
        """
        Initializes the class with parameters (below) and with necessary
            variables.

        :param rows: Number of rows(default=6).
        :type rows: int
        :param columns: Number of columns(default=7).
        :type columns: int
        :param player_1: Marker used for player 1's pawns.
        :type player_1: str
        :param player_2: Marker used for player 2's pawns.
        :type player_2: str
        """

        self.size = {"r":rows, "c":columns}
        self.grid = []

        self.first_player = True
        self.players = {True: player_1, False: player_2}

        self.game_over = False

        # Makes the grid where pawns are placed.
        for square in range(0, self.size["c"]):
            self.grid.append([])


    def place_pawn(self, column):
        """
        Adds the players pawn in the chosen column. Returns false if game is
            over or column does not exist in the game board. Returns True if
            pawn was placed/added.

        :return: True if pawn was placed, regardless of gamestate. False if not.
            Also False if game is over.
        :rtype: bool
        :param column: The column where the pawn is placed.
        :type column: int
        """

        # Game is over.
        if self.game_over:
            return False

        # Column is not on the game board -> False.
        if column < 0 or column >= self.size["c"]:
            return False
        if len(self.grid[column]) >= self.size['r']:
            return False

        # Adds the players pawn in the chosen column.
        self.grid[column].append(self.players[self.first_player])

        # If game is ongoing, changes the player from 1 to 2 and vice versa.
        if self.check_gamestate() == "ongoing":
            self.first_player = not self.first_player
            return True
        else:
            # Game ends after the pawn is placed.
            self.game_over = self.check_gamestate()
            return True


    def check_gamestate(self):
        """
        Checks in what state the game is. It is either won by someone, a draw
            or still ongoing. One or the other player has 4 pawns in a row
            (vertical, horizontal, diagonal) -> return "win". All of the game
            board is filled but no one won -> return "draw". If either of the
            options before are not true -> return "ongoing".

        :return: The state the game is in. "win", "draw" or "ongoing".
        :rtype: str
        """

        # Number of pawns in the game board.
        pawns = 0


        for c_counter, column in enumerate(self.grid):

            # Adds every pawn in grid to pawns.
            pawns += len(self.grid[c_counter])


            for r_counter, row in enumerate(column):

                # Not in 4 last columns -> True, else -> False
                horizontal = (c_counter + 4 <= self.size["c"])

                # Column has at least 4 pawns -> True(when r_counter=0 meaning
                # first time around in loop)
                vertical = (r_counter + 4 <=
                                len(self.grid[c_counter]))

                # Determines if 4 pawns are in a row upwards or downwards
                # (vertical)
                if vertical:

                    # len() is one if only one type of pawn is in set.
                    if len(set(self.grid[c_counter]
                            [r_counter:r_counter + 4])) == 1:
                        return "win"

                # Determines if 4 pawns are in a row sideways (horizontal)
                if horizontal:

                    # True if all adjacent columns have something in them.
                    if len(self.grid[c_counter]) > r_counter \
                            and len(self.grid[c_counter + 1]) > r_counter \
                            and len(self.grid[c_counter + 2]) > r_counter \
                            and len(self.grid[c_counter + 3]) > r_counter:

                        pawn_set = set()

                        for number in range(0, 4):


                            pawn_set.add(self.grid[c_counter +
                                                number][r_counter])

                        # len(pawn_set) is 1 if only one type of pawn is in set.
                        if len(pawn_set) == 1:
                            return "win"

                # Determines if 4 pawns are in a row diagonally (upwards)
                if horizontal:

                    pawn_set_2 = set()

                    for number in range(0, 4):

                        # True if there is a required amount of pawns to make
                        # a diagonal row
                        if len(self.grid[c_counter + number]) > \
                                r_counter + number:

                            pawn_set_2.add(self.grid[c_counter +
                                number][r_counter + number])

                        else:
                            pawn_set_2.add("E")

                    # len(pawn_set_2) is 1 if only one type of pawn is in set.
                    if len(pawn_set_2) == 1:
                        return "win"

                # 4 squares diagonally (downwards)
                # r_counter -3 is used because the 4th row of pawns
                # results in r_counter being at least 3 (begins from 0).
                if horizontal and r_counter - 3 >= 0:

                    pawn_set_3 = set()

                    for number in range(0, 4):

                        if len(self.grid[c_counter + number]) > \
                                (r_counter - number):

                            pawn_set_3.add(self.grid[c_counter +
                                number][r_counter - number])

                        else:
                            pawn_set_3.add("E")

                    # len(pawn_set_3) is 1 if only one type of pawn is in set.
                    if len(pawn_set_3) == 1:
                        return "win"

        # Pawns fill the whole board without someone winning -> must be draw
        if pawns == (self.size["c"] * self.size["r"]):
            return "draw"

        # If game is not won or draw it is ongoing.
        return "ongoing"

class Gameinterface:
    """
    Class Gameinterface creates the GUI which is used for the game
        "Connect Four". It has a title, the game board, current player
        indicator and a menu that has the options "New Game", "Instructions"
        and "Quit".
    """

    # Size of one square in game board.
    element_size = 50
    # Width of grids lines.
    grid_border = 3
    # Grids line color
    grid_color = "black"
    # player 1's pawn color
    player_1_color = "yellow"
    # player 2's pawn color
    player_2_color = "cyan"
    # Indicator for games state.
    game_on = False

    def __init__(self):
        """
        Initializes the GUI.
        """

        self.__mainwindow = Tk()
        self.__mainwindow.title("Connect 4")



        # Creating the dropdown menu.
        main_menu = Menu(self.__mainwindow)
        self.__mainwindow.config(menu=main_menu)

        function_menu = Menu(main_menu)
        main_menu.add_cascade(label="Menu", menu=function_menu)
        function_menu.add_command(label="New Game", command=self.new_game)

        function_menu.add_command(label="Instructions",
                                  command=self.print_instructions)

        function_menu.add_separator()
        function_menu.add_command(label="Quit", command=self.quit)
        #

        title_label = Label(text="CONNECT FOUR", font=("times new roman", 32),
                            fg="green")

        # Creating the game board using Canvas.
        self.__game_board = Canvas(self.__mainwindow, width=500, height=300,
                                   bg="blue")
        self.__current_player = Label(self.__mainwindow, text="")


        title_label.grid(row=0, sticky=W+E)
        self.__game_board.grid(row=1)
        self.__current_player.grid(row=2, sticky=W+E)

        # Bind left_mouse button to placing a pawn.
        self.__game_board.bind('<Button-1>', self.place_pawn)

        self.new_game()


    def new_game(self):
        """
        Starts the game from the beginning by deleting all previous actions and
            creating the gameboard again. Also updates current player and is
            used when first time creating the board.
        """

        # Names of the players
        self.__player_1 = "Player 1"
        self.__player_2 = "Player 2"

        self.__game = Connectfour()

        # Clears the game board of everything.
        self.__game_board.delete(ALL)
        self.__game_board.config(width=(self.element_size) * self.__game.size['c'],
                           height=(self.element_size) * self.__game.size['r'])

        # Draws everything needed in game board and updates the current player.
        self.__mainwindow.update()
        self.draw_grid()
        self.draw_pawn()
        self.update_player()

        self.game_on = True
        self.__mainwindow.mainloop()


    def print_instructions(self):
        """
        Prints the games instructions(how to play) to a new window using
            Toplevel.
        """

        instruction_window = Toplevel(self.__mainwindow)
        instruction_window.title("INSTRUCTIONS")
        instruction_window.geometry("460x350")

        instruction_text = "Connect Four is a game where \n your goal is to have" \
                           " 4 of your \n pawns in a row either horizontally, \n" \
                           "vertically or diagonally. \n By achieving this you " \
                           "win. \n Two players take turns to drop \n their own " \
                           "pawns in while \n trying to win and stop the \n other " \
                           "player from winning."

        instructions = Label(instruction_window, text=instruction_text,
                             font=("times new roman", 25))

        instructions.pack()


    def place_pawn(self, event):
        """
        Places the pawn in the chosen column and updates current players.
            Also displays end message if the game ended after placing the pawn.
        """

        # Game is over -> return
        if not self.game_on:
            return
        if self.__game.game_over:
            return

        # Defining the column that was clicked.
        column = event.x // self.element_size

        # Column exists -> True.
        if (0 <= column < self.__game.size['c']):

            # Uses the drop method to place the pawn.
            self.drop(column)
            self.draw_pawn()
            self.update_player()

        # Game is over after placing pawn.
        if self.__game.game_over:

            # X and Y coordinates at the middle of the game board.
            x = self.__game_board.winfo_width() // 2
            y = self.__game_board.winfo_height() // 2

            # Game resulted in a draw.
            if self.__game.game_over == "draw":
                text_message = "IT'S A DRAW!"

            # Game is over and not a draw -> someone won.
            else:

                # Determining the winning player.
                if self.__game.first_player:
                    winner = self.__player_1
                else:
                    winner = self.__player_2

                # Victory message.
                text_message = winner + "WON!"

            # Creating the end message on the game board.
            self.__game_board.create_text(x, y, text=text_message,
                font=("times new roman", 32))


    def draw_grid(self):
        """
        Draws the grid needed in the game board.
        """

        # Determines the starting and ending x coordinate.
        x_0, x_1 = 0, self.__game_board.winfo_width()

        # Creates horizontal lines in the grid.
        for row in range(1, self.__game.size['r']):
            y = row * self.element_size
            self.__game_board.create_line(x_0, y, x_1, y, fill=self.grid_color)

        # Determines the starting and ending y coordinate.
        y_0, y_1 = 0, self.__game_board.winfo_height()

        # Creates vertical lines in the grid.
        for column in range(1, self.__game.size['c']):
            x = column * self.element_size
            self.__game_board.create_line(x, y_0, x, y_1, fill=self.grid_color)



    def draw_pawn(self):
        """
        Draws the placed pawn in the game board according to where it was
            placed and the player that placed it.
        """

        for column in range(0, self.__game.size["c"]):

            for row in range(0, self.__game.size["r"]):

                # There is nothing in the column at this row.
                if row >= len(self.__game.grid[column]):
                    continue

                # The starting and ending coordinates of the exact square where
                # the pawn is to be placed.
                x_0 = column * self.element_size
                y_0 = row * self.element_size
                x_1 = (column + 1) * self.element_size
                y_1 = (row + 1) * self.element_size

                # Determines the player that placed the pawn -> needed color.
                if self.__game.grid[column][row] == self.__game.players[True]:
                    color = self.player_1_color
                else:
                    color = self.player_2_color

                # Creates the circle/oval used as pawn in the game.
                self.__game_board.create_oval(x_0 + 2,
                    self.__game_board.winfo_height() - (y_0 + 2),
                    x_1 - 2,self.__game_board.winfo_height() - (y_1 - 2),
                    fill=color)


    def update_player(self):
        """
        Updates the current player, meaning the player that is in turn at the
            moment.
        """

        # True if current player=player 1.
        if self.__game.first_player:
            player = self.__player_1
            player_color = self.player_1_color
        else:
            player = self.__player_2
            player_color = self.player_2_color

        # Configurates the current player to the player indicator.
        self.__current_player.config(text=f"{player}'s "
                                          f"turn    Color: {player_color}")


    def drop(self, column):
        """
        Drops/places the pawn in the column using the place_pawn method in
            class Connectfour.

        :param column: The column where the pawn is to be placed/dropped.
        :type column: int
        """

        return self.__game.place_pawn(column)

    def quit(self):
        """
        Asks the user if they want to quit, yes -> end program, no ->
        continue program.
        """

        if messagebox.askyesno("Quit", "Do you want to Quit?"):
            self.__mainwindow.destroy()


def main():

    Gameinterface()

if __name__ == "__main__":
    main()