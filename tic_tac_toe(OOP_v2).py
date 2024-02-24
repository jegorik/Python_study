import numpy as np  # Importing the numpy library for array manipulations

# Define the TicTacToe class which includes methods to play the game
class TicTacToe:
    def __init__(self):
        # Initialize the game field with spaces representing empty cells
        self._field = np.full((3, 3), ' ')
        # Print the initial layout of the field
        self.print_field_layout()
        # Set the first player to X
        self._current_player = 'X'
        # Initialize the game over flag to False, game continues until a win or draw
        self._game_over = False

    def print_field_layout(self):
        # Print the current layout of the game field
        print(self.get_field_string())

    def check_player_input(self, _player_coordinates):
        # Validate the coordinates entered by the player
        # Check if they are within the 1-3 range and the cell is not already occupied
        if any(x > 3 or x < 1 for x in _player_coordinates):
            print('Coordinates should be from 1 to 3!')
            return False
        if self._field[_player_coordinates[0] - 1, _player_coordinates[1] - 1] == ' ':
            # Place the player's mark on the field if valid
            self._field[_player_coordinates[0] - 1, _player_coordinates[1] - 1] = self._current_player
            winner = self.check_winner()
            # Check for a win, draw, or change turns
            if winner:
                print(f'{self.get_field_string()}{self._current_player} wins')
                self._game_over = True
            elif ' ' not in self._field:
                print(f'{self.get_field_string()}Draw')
                self._game_over = True
            else:
                self._current_player = 'O' if self._current_player == 'X' else 'X'
                print(self.get_field_string())
            return True
        else:
            print('This cell is occupied! Choose another one!')
            return False

    def check_winner(self):
        # Check all possible win conditions (rows, columns, diagonals)
        for i in range(3):
            if (self._field[i] == self._current_player).all() or (self._field[:, i] == self._current_player).all():
                return True
        if (self._field.diagonal() == self._current_player).all() or (np.fliplr(self._field).diagonal() == self._current_player).all():
            return True
        return False

    def player_turn(self):
        # Handle player input during their turn
        while True:
            _player_input = input("Enter your move: ")
            try:
                _player_coordinates = [int(x) for x in _player_input.split()]
                if len(_player_coordinates) != 2 or not all(1 <= x <= 3 for x in _player_coordinates):
                    raise ValueError
                if self.check_player_input(_player_coordinates):
                    break
            except ValueError:
                print('You should enter two numbers from 1 to 3, separated by a space!')

    def get_field_string(self):
        # Convert the current field into a string for printing
        field_string = '---------\n'
        for row in self._field:
            field_string += f"| {' '.join(row)} |\n"
        field_string += '---------\n'
        return field_string

# The main function that starts the game
def main():
    new_game = TicTacToe()
    while not new_game._game_over:
        new_game.player_turn()

# Entry point of the script
if __name__ == "__main__":
    main()
