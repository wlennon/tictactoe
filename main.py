import tkinter as tk
import tkinter.font as font
from tkinter import ttk, messagebox as mb
from windows import set_dpi_awareness
from functools import partial

set_dpi_awareness()

class TicTacToe(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("TicTacToe")
        self.resizable(False, False)

        #Frames
        game_space = ttk.Frame(self)
        draws_frame = ttk.Frame(game_space)
        scoreboard = ttk.Frame(draws_frame, borderwidth=4, relief='raised')
        game_board = ttk.Frame(game_space)

        #Varaibles
        self.player_one = tk.StringVar(value='')
        self.player_one_wins = tk.StringVar(value='0')
        self.player_two = tk.StringVar(value='')
        self.player_two_wins = tk.StringVar(value='0')
        self.draws = tk.StringVar(value='0')

        self.button_values = [None for _ in range(9)]
        i = 0
        for i in range(9):
            self.button_values[i] = tk.StringVar(value=' ')


        self.turn = tk.IntVar(value=1)
        self.turn_indicator = tk.StringVar(value='')

        self.clicked_matrix = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

        #Labels
        score_label = ttk.Label(scoreboard, text='SCOREBOARD')
        players_label = ttk.Label(scoreboard, text='Players')
        wins_label = ttk.Label(scoreboard, text='Wins')
        draws_label = ttk.Label(draws_frame, text='Draws:', font=(None, 13))
        player_one_wins_label = ttk.Label(scoreboard, textvariable=self.player_one_wins)
        player_two_wins_label = ttk.Label(scoreboard, textvariable=self.player_two_wins)
        draws_value_label = ttk.Label(draws_frame, textvariable=self.draws, font=(None, 13))

        turn_indicator_label = ttk.Label(game_space, textvariable=self.turn_indicator, font=(None, 12))

        #Buttons
        self.buttons = [None for _ in range(9)]
        i = 0
        for i in range(9):
            function_with_args = partial(self.buttonFunc, i)
            self.buttons[i] = ttk.Button(game_board, width=3, textvariable=self.button_values[i], style='W.TButton', command=function_with_args, state='disabled')

        update_names_button = ttk.Button(draws_frame, text='Update Names', command=self.updateNames)
        clear_score_button = ttk.Button(draws_frame, text='Clear Score', command=self.clearScore)
        
        #Entry Fields
        self.player_one_input = ttk.Entry(scoreboard, width=15, textvariable=self.player_one)
        self.player_one_input.focus()
        self.player_two_input = ttk.Entry(scoreboard, width=15, textvariable=self.player_two)

        #Separators
        scoreboard_separator1 = ttk.Separator(scoreboard, orient='horizontal')
        
        #Layout
        game_space.grid()
        draws_frame.grid(column=0, row=0, rowspan=2)
        scoreboard.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
        turn_indicator_label.grid(column=1, row=0, pady=(10,0))
        game_board.grid(column=1, row=1, padx=5, pady=5)

        score_label.grid(column=0, row=0, columnspan=2)
        players_label.grid(column=0, row=1, padx=1)
        wins_label.grid(column=1, row=1, padx=10)
        scoreboard_separator1.grid(column=0, row=2, columnspan=2, sticky='EW')
        self.player_one_input.grid(column=0, row=3)
        player_one_wins_label.grid(column=1, row=3)
        self.player_two_input.grid(column=0, row=4)
        player_two_wins_label.grid(column=1, row=4)
        

        draws_label.grid(column=0, row=1)
        draws_value_label.grid(column=1, row=1, sticky='EW')
        update_names_button.grid(column=0, row=2, padx=(5,2))
        clear_score_button.grid(column=1, row=2)


        i = 0
        x = 0
        y = 0
        for i in range(9):
            self.buttons[i].grid(column=y, row=x)
            if (y+1)%3 == 0 and i != 0:
                y = 0
                x = x + 1
            else:
                y = y + 1

    def checkTurn(self):
        if self.turn.get() == 2:
            self.turn_indicator.set(value=self.player_one.get() + "'s Move: X")
            self.turn.set(value=1)
        else:
            self.turn_indicator.set(value=self.player_two.get() + "'s Move: O")
            self.turn.set(value=2)

    def clearBoard(self):
        self.clicked_matrix = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        for value in self.button_values:
            value.set(value=' ')

    def checkWin(self):
        patterns = {
            0:[0,1,2],
            1:[3,4,5],
            2:[6,7,8],
            3:[0,3,6],
            4:[1,4,7],
            5:[2,5,8],
            6:[0,4,8],
            7:[2,4,6]
        }

        i = 0
        answer = 'yes'

        for i in range(8):
            temp = self.clicked_matrix[patterns[i][0]] + self.clicked_matrix[patterns[i][1]] + self.clicked_matrix[patterns[i][2]]
            if temp[0] == temp[1] == temp[2] and ' ' not in temp:
                if self.turn.get() == 1:
                    answer = mb.askquestion(title=None, message=self.player_one.get() + ' Wins! Play again?')
                else:
                    answer = mb.askquestion(title=None, message=self.player_two.get() + ' Wins! Play again?')
                
                if answer == 'no':
                    self.destroy()
                else:
                    self.clearBoard()

                    if self.turn.get() == 1:
                        score = int(self.player_one_wins.get())
                        self.player_one_wins.set(f"{score+1}")
                    else:
                        score = int(self.player_two_wins.get())
                        self.player_two_wins.set(f"{score+1}")
                    
                    self.checkWin()
            
        if ' ' not in self.clicked_matrix and answer != 'no':
            answer = mb.askquestion(title=None, message='Draw! Play again?')

            if answer == 'no':
                self.destroy()
            else:
                self.clearBoard()
                
                score = int(self.draws.get())
                self.draws.set(f"{score+1}")

    def buttonFunc(self, button):
        i = 0
        for i in range(9):
            if button == i and self.clicked_matrix[i] == ' ':
                if self.turn.get() == 1:
                    self.button_values[i].set(value='X')
                else:
                    self.button_values[i].set(value='O')

                self.clicked_matrix[i] = self.button_values[i].get()
                self.checkWin()
                self.checkTurn()

    def updateNames(self):
        if self.player_one.get() == '' or self.player_two.get() == '':
            mb.showerror(title=None, message='Must fill in both player names!')
        else:
            self.turn_indicator.set(value=self.player_one.get() + "'s Move: X")
            self.player_one_input['state'] = 'disabled'
            self.player_two_input['state'] = 'disabled'
            for button in self.buttons:
                button['state'] = 'normal'

    def clearScore(self):
        self.player_one_wins.set('0')
        self.player_two_wins.set('0')
        self.draws.set('0')
        self.clearBoard()
        self.player_one_input['state'] = 'normal'
        self.player_two_input['state'] = 'normal'
        self.turn.set(1)
        self.turn_indicator.set('')

if __name__=="__main__":
    root = TicTacToe()
    root.columnconfigure(0, weight=1)

    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('W.TButton', font=(None, 15))
    root.mainloop()