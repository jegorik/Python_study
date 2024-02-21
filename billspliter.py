import random


class BillSplitter:
    """
    A class to split a bill among friends, with an option to choose a lucky friend.

    Attributes:
    - friends_list (dict): A dictionary to store friends and their share of the bill.
    """

    def __init__(self):
        self.friends_list = {}

    def create_list(self):
        """
        Creates a list of friends joining the bill-splitting.

        Returns:
        - bool: True if friends are joining, False if no one is joining.
        """
        number_of_friends = self.validate_input('Enter the number of friends joining (including you):\n', int)
        if number_of_friends > 0:
            print('Enter the name of every friend (including you), each on a new line:')
            for _ in range(number_of_friends):
                name = input()
                self.friends_list[name] = 0
            return True
        else:
            print('No one is joining for the party')
            return False

    def split_bill(self):
        """
        Splits the bill among friends, with an option to choose a lucky friend.
        """
        total_bill = self.validate_input('Enter the total bill value:\n', float)
        lucky = self.choose_lucky()
        friends = len(self.friends_list)
        if lucky:
            self.friends_list.pop(lucky)
            self.friends_list = {key: self.calculate_split(total_bill, friends - 1) for key in self.friends_list}
            self.friends_list.update({lucky: 0})
        else:
            self.friends_list = {key: self.calculate_split(total_bill, friends) for key in self.friends_list}

    @staticmethod
    def calculate_split(total_bill, friends):
        """
        Calculates the split amount per friend.

        Args:
        - total_bill (float): Total bill value.
        - friends (int): Number of friends.

        Returns:
        - float: Split amount per friend.
        """
        return round(total_bill / friends, 2)

    def get_friends_list(self):
        """
        Returns the list of friends and their share of the bill.

        Returns:
        - dict: List of friends and their share of the bill.
        """
        return self.friends_list

    @staticmethod
    def validate_input(prompt, data_type):
        """
        Validates user input based on data type.

        Args:
        - prompt (str): Input prompt message.
        - data_type (type): Data type to validate.

        Returns:
        - value: Validated user input.
        """
        while True:
            try:
                value = data_type(input(prompt))
                if value < 0:
                    raise ValueError("Please enter a non-negative value")
                return value
            except ValueError as e:
                print(f"Error: {e}")

    def choose_lucky(self):
        """
        Allows the user to choose a lucky friend.

        Returns:
        - str: Name of the lucky friend.
        """
        while True:
            user_input = input('Do you want to use the "Who is lucky?" feature? Write Yes/No: \n').capitalize()
            if 'Yes' in user_input:
                lucky = random.choice(list(self.friends_list.keys()))
                print(f'{lucky} is the lucky one!')
                return lucky
            elif 'No' in user_input:
                print('No one is going to be lucky')
                return None
            else:
                print('Please enter Yes or No')


def main():
    bill_splitter = BillSplitter()
    if bill_splitter.create_list():
        bill_splitter.split_bill()
        print(bill_splitter.get_friends_list())


if __name__ == "__main__":
    main()
