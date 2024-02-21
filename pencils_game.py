import random


class PencilGame:
    """
    A class representing a game where players take turns removing pencils from a pile.

    Attributes:
        PLAYERS_NAMES (list): A list of player names.
        MAX_PENCILS (int): The maximum number of pencils allowed.

    Methods:
        create_pencils(): Prompt the user to enter the number of pencils to use and create the pencil pile.
        choose_player(): Prompt the user to choose the first player.
        print_table(): Print the current state of the pencil pile.
        start_game(): Start the pencil game by creating pencils, choosing the first player, printing the table, and starting the game process.
        player_turn(pencils_amount, current_player): Perform a player's turn in the game.
        human_turn(pencils_amount): Perform a human player's turn in the game.
        bot_turn(pencils_amount): Perform a bot player's turn in the game.
        game_process(): Run the game process until there are no more pencils left.
        switch_player(current_player): Change the current player to the other player.
        check_winner(): Check if there is a winner and print the winner's name.
    """

    PLAYERS_NAMES = ['John', 'Jack']
    MAX_PENCILS = 100

    def __init__(self):
        self.pencils = []
        self.current_player = ''

    def create_pencils(self):
        """
        Prompt the user to enter the number of pencils to use and create the pencil pile.
        """
        while True:
            try:
                pencils_amount = int(input('How many pencils would you like to use: \n'))
                if pencils_amount > 0:
                    self.pencils = ['|'] * pencils_amount
                    break
                else:
                    print('The number of pencils should be positive.')
            except ValueError:
                print('The number of pencils should be numeric')

    def choose_player(self):
        """
        Prompt the user to choose the first player.
        """
        while True:
            user_player_input = input(f'Who will be the first ({(", ".join(self.PLAYERS_NAMES))}): \n')
            if user_player_input in self.PLAYERS_NAMES:
                self.current_player = user_player_input
                break
            else:
                print(f'Choose between {(" and ".join(self.PLAYERS_NAMES))}')

    def print_table(self):
        """
        Print the current state of the pencil pile.
        """
        print("".join(self.pencils))

    def start_game(self):
        """
        Start the pencil game by creating pencils, choosing the first player, printing the table, and starting the game process.
        """
        self.create_pencils()
        self.choose_player()
        self.print_table()
        self.game_process()

    def player_turn(self, pencils_amount, current_player):
        """
        Perform a player's turn in the game.

        Args:
            pencils_amount (int): The current number of pencils.
            current_player (str): The current player's name.

        Returns:
            int: The number of pencils taken by the player.
        """
        print(f"{current_player}'s turn:")
        if current_player == self.PLAYERS_NAMES[0]:
            return self.human_turn(pencils_amount)
        else:
            return self.bot_turn(pencils_amount)

    def human_turn(self, pencils_amount):
        """
        Perform a human player's turn in the game.

        Args:
            pencils_amount (int): The current number of pencils.

        Returns:
            int: The number of pencils taken by the human player.
        """
        while True:
            try:
                player_action = int(input())
                if 1 <= player_action <= 3:
                    if player_action <= pencils_amount:
                        return player_action
                    else:
                        print('Too many pencils were taken')
                else:
                    print("Possible values: '1', '2' or '3'")
            except ValueError:
                print("Possible values: '1', '2' or '3'")

    def bot_turn(self, pencils_amount):
        """
        Perform a bot player's turn in the game.

        Args:
            pencils_amount (int): The current number of pencils.

        Returns:
            int: The number of pencils taken by the bot player.
        """
        if pencils_amount % 4 == 1:
            return random.randint(1, min(3, pencils_amount))
        else:
            return (pencils_amount - 1) % 4

    def game_process(self):
        """
        Run the game process until there are no more pencils left.
        """
        while len(self.pencils) > 0:
            action = self.player_turn(len(self.pencils), self.current_player)
            self.pencils = self.pencils[:-action]
            self.print_table()
            self.current_player = self.switch_player(self.current_player)
            self.check_winner()

    def switch_player(self, current_player):
        """
        Change the current player to the other player.

        Args:
            current_player (str): The current player's name.

        Returns:
            str: The name of the other player.
        """
        return self.PLAYERS_NAMES[0] if current_player == self.PLAYERS_NAMES[1] else self.PLAYERS_NAMES[1]

    def check_winner(self):
        """
        Check if there is a winner and print the winner's name.
        """
        if len(self.pencils) == 0:
            print(f'{self.current_player} Won!')


def main():
    """
    The main function that creates an instance of the PencilGame class and starts the game.
    """
    new_pencil_game = PencilGame()
    new_pencil_game.start_game()


if __name__ == '__main__':
    main()
