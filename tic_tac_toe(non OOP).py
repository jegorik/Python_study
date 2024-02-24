import random

board = []
players = []
marker = ''


def create_board():
    """
    Creates a new game board.

    Returns:
        list: The game board.
    """
    board = [' '] * 10
    board[0] = '#'
    return board


def show_board():
    """
    Displays the current game board.
    """
    k = 1
    for x in range(0, 3):
        print(board[x + k] + ' | ' + board[x + k + 1] + ' | ' + board[x + k + 2])
        if x < 2:
            print('--| - |--')
        k += 2


def read_user_input():
    """
    Reads and validates user input for the next move.

    Returns:
        int: The validated user input.
    """
    user_input = 0
    check_user_input = True
    acceptable_values = range(1, 10)
    while check_user_input:
        user_input = input('Please enter number in range of [1-9]: ')
        if not user_input.isdigit():
            print('That is not a digit!')
        elif int(user_input) not in acceptable_values:
            print('Number is not in [1-9] range!')
        elif read_board_cell(int(user_input)) != ' ':
            print('This cell already has a marker!')
        else:
            check_user_input = False
    return int(user_input)


def start_game():
    """
    Asks the user if they want to start a new game.

    Returns:
        bool: True if the user wants to start a new game, False otherwise.
    """
    user_exit_input = ''
    while user_exit_input not in ['Y', 'N']:
        user_exit_input = input('Start game? (Y or N) ')
        if user_exit_input not in ['Y', 'N']:
            print('Sorry invalid input, please choose Y or N')
    if user_exit_input == 'Y':
        return True
    else:
        return False


def update_board(cell_number, marker):
    """
    Updates the game board with the player's marker.

    Args:
        cell_number (int): The cell number where the marker should be placed.
        marker (str): The player's marker ('X' or 'O').

    Returns:
        None
    """
    board[cell_number] = str(marker)


def read_board_cell(cell_number):
    """
    Reads the value of a cell on the game board.

    Args:
        cell_number (int): The cell number to read.

    Returns:
        str: The value of the cell.
    """
    return board[cell_number]


def choose_marker():
    """
    Asks the players to choose their markers.

    Returns:
        tuple: A tuple containing the markers chosen by player 1 and player 2.
    """
    marker = ''
    while marker != 'X' and marker != 'O':
        marker = input('Player 1, choose X or O: ')
    player1 = marker
    if player1 == 'X':
        player2 = 'O'
    else:
        player2 = 'X'
    print('Player 1 is', player1)
    return player1, player2


def win_check(board, mark):
    """
    Checks if a player has won the game.

    Args:
        board (list): The game board.
        mark (str): The player's marker ('X' or 'O').

    Returns:
        bool: True if the player has won, False otherwise.
    """
    k = 1
    y = 3
    z = 3
    result = False
    for x in range(0, 3):
        if board[x + k] == mark and board[x + k + 1] == mark and board[x + k + 2] == mark:
            result = True
        elif board[x + 1] == mark and board[k + y] == mark and board[z + y + k] == mark:
            result = True
        if x == 1:
            if board[x] == mark and board[z + z - 1] == mark and board[x + k + z + y] == mark:
                result = True
        if x == 2:
            if board[x + 1] == mark and board[z + z - 1] == mark and board[k + x] == mark:
                result = True
        k += 2
        y -= 1
    return result


def first_turn():
    """
    Randomly determines which player goes first.

    Returns:
        int: The index of the player who goes first (0 or 1).
    """
    return random.randint(0, 1)


def change_player(marker):
    """
    Changes the current player's marker.

    Args:
        marker (str): The current player's marker ('X' or 'O').

    Returns:
        str: The new player's marker.
    """
    if marker == 'X':
        return 'O'
    else:
        return 'X'


def board_have_place(board):
    """
    Checks if there are any empty cells left on the game board.

    Args:
        board (list): The game board.

    Returns:
        bool: True if there are empty cells, False otherwise.
    """
    if ' ' in board:
        return False
    else:
        return True


def new_game():
    """
    Starts a new game by resetting the board, choosing markers, and determining the first player.
    """
    global board, players, marker
    board = create_board()
    players = choose_marker()
    marker = players[first_turn()]
    print(marker, 'goes first')


board = create_board()
players = ()
marker = ''

game = start_game()
if game:
    new_game()

while game:
    print(marker, ' Turn')
    cell_number = read_user_input()
    update_board(cell_number, marker)
    show_board()
    if win_check(board, marker) or board_have_place(board):
        if board_have_place(board):
            print('TIE!')
        else:
            print(marker, 'WIN!')
        game = start_game()
        if game is not True:
            break
        else:
            new_game()
            show_board()
    else:
        marker = change_player(marker)
