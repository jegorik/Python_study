import random


class Game:
    # Class variable to keep track of whether the running is running or not
    running = False

    def __init__(self):
        print(f"Game name: {type(self).__name__}")

    def start_game(self):
        # Abstract method, should be implemented by subclass
        raise NotImplementedError("Subclass must implement this abstract method")

    def new_game(self):
        # Abstract method, should be implemented by subclass
        raise NotImplementedError("Subclass must implement this abstract method")


def choose_markers():
    # Prompt the players to choose their markers (X or O)
    while True:
        player1_marker = input('Player 1, choose X or O: ').upper()
        if player1_marker == 'X':
            player2_marker = 'O'
            break
        elif player1_marker == 'O':
            player2_marker = 'X'
            break
        else:
            print('Invalid current_marker choice, please choose X or O')
    print(f"Player 1 is {player1_marker}")
    return player1_marker, player2_marker


class TicTacToe(Game):
    board = []
    players = []
    current_marker = ''

    def get_board(self):
        return self.board

    # Initialize the game board with empty cells
    def create_board(self):
        self.board = [' '] * 10
        self.board[0] = '#'

    def show_board(self):
        # Display the current state of the game board
        k = 1
        for x in range(0, 3):
            print(f"{self.board[x + k]} | {self.board[x + k + 1]} | {self.board[x + k + 2]}")
            if x < 2:
                print('--| - |--')
            k += 2

    def read_user_input(self):
        # Get valid input from the user (a number from 1-9)
        acceptable_values = range(1, 10)
        while True:
            user_input = input('Please enter a number in the range of [1-9]: ')
            if not user_input.isdigit():
                print('That is not a digit!')
            elif int(user_input) not in acceptable_values:
                print('Number is not in [1-9] range!')
            elif self.board[int(user_input)] != ' ':
                print('This cell already has a marker!')
            else:
                return int(user_input)

    def update_board(self, cell_number, current_marker):
        # Update the game board with the current player's marker
        self.board[cell_number] = str(current_marker)

    def read_board_cell(self, cell_number):
        # Return the value of a cell on the game board
        return self.board[cell_number]

    def win_check(self):
        # Check if the current player has won the game
        k = 1
        y = 3
        z = 3
        for x in range(0, 3):
            if (
                    self.board[x + k] == self.current_marker
                    and self.board[x + k + 1] == self.current_marker
                    and self.board[x + k + 2] == self.current_marker
            ):
                return True
            elif (
                    self.board[x + 1] == self.current_marker
                    and self.board[k + y] == self.current_marker
                    and self.board[z + y + k] == self.current_marker
            ):
                return True
            if x == 1:
                if (
                        self.board[x] == self.current_marker
                        and self.board[z + z - 1] == self.current_marker
                        and self.board[x + k + z + y] == self.current_marker
                ):
                    return True
            if x == 2:
                if (
                        self.board[x + 1] == self.current_marker
                        and self.board[z + z - 1] == self.current_marker
                        and self.board[k + x] == self.current_marker
                ):
                    return True
            k += 2
            y -= 1
        return False

    @staticmethod
    def first_turn():
        # This method is a utility function that randomly selects the first player
        return random.randint(0, 1)

    def change_player(self):
        # This method changes the current player to the opposite marker
        return 'O' if self.current_marker == 'X' else 'X'

    def board_have_place(self):
        # Checks if there are any empty spaces left on the board and returns True if there aren't any
        return ' ' not in self.board

    def new_game(self):
        # This method is called when a new game is started. It performs the following tasks:
        # 1. It creates a new game board.
        # 2. It allows the players to choose their markers.
        # 3. It randomly selects the first player and assigns the current marker accordingly.
        # 4. It shows the initial game board.
        # 5. It starts the game process.
        self.create_board()
        self.players = choose_markers()
        self.current_marker = self.players[self.first_turn()]
        print(f"{self.current_marker} goes first")
        self.show_board()
        self.game_process()

    @staticmethod
    def start_game():
        # This method prompts the user to start the game. It accepts the user input and returns True if the input is 'Y', False otherwise.
        user_exit_input = ''
        while user_exit_input not in ['Y', 'N']:
            user_exit_input = input('Start game? (Y or N) ').upper()
            if user_exit_input not in ['Y', 'N']:
                print('Sorry invalid input, please choose Y or N')
        return user_exit_input == 'Y'

    def game_process(self):
        # This method represents the main game loop. It performs the following tasks:
        # 1. It displays the current player's turn.
        # 2. It prompts the user to choose a cell to mark on the board.
        # 3. It updates the board with the current player's marker.
        # 4. It shows the updated game board.
        # 5. It checks if the current player has won or if there is a tie. If so, it displays the result and prompts the user to start a new game.
        # 6. If the user chooses to start a new game, it calls the new_game() method. Otherwise, it breaks out of the game loop.
        # 7. If the game is not over, it switches to the next player's turn.
        while self.running:
            print(f"{self.current_marker} Turn")
            cell_number = self.read_user_input()
            self.update_board(cell_number, self.current_marker)
            self.show_board()
            if self.win_check() or self.board_have_place():
                if self.board_have_place():
                    print('TIE!')
                else:
                    print(f"{self.current_marker} WIN!")
                self.running = self.start_game()
                if self.running is not True:
                    break
                else:
                    self.new_game()
            else:
                self.current_marker = self.change_player()

# This code creates a new instance of the TicTacToe class and assigns it to the variable new_game_TicTacToe.
# It then sets the running attribute of the instance to the value returned by the start_game() method.
# If the running attribute is True, it calls the new_game() method to start the game.
new_game_TicTacToe = TicTacToe()
new_game_TicTacToe.running = new_game_TicTacToe.start_game()
if new_game_TicTacToe.running:
    new_game_TicTacToe.new_game()
