class Product:
    """
    Represents a coffee product with its ingredients.

    Attributes:
        name (str): The name of the product.
        ingredients (dict): A dictionary containing the ingredients and their quantities.
    """

    def __init__(self, name, water, milk, coffee_beans, cups, money):
        """
        Initializes a Product instance.

        Args:
            name (str): The name of the product.
            water (int): The amount of water required (in ml).
            milk (int): The amount of milk required (in ml).
            coffee_beans (int): The amount of coffee beans required (in grams).
            cups (int): The number of cups required.
            money (int): The price of the product.
        """
        self.name = name
        self.ingredients = {
            'water': water,
            'milk': milk,
            'coffee beans': coffee_beans,
            'cups': cups,
            'money': money
        }

    def __str__(self):
        """Returns a string representation of the product."""
        return f"{self.name.capitalize()} - Ingredients: {self.ingredients}"


class CoffeeMachine:
    """
    Represents a coffee machine that can manage coffee products and user interactions.

    Attributes:
        products (dict): A dictionary of available coffee products.
        coffee_machine_stock (dict): A dictionary representing the current stock of ingredients.
        measurements (dict): A dictionary of measurement units for each ingredient.
        available_commands (dict): A dictionary of available commands for user interaction.
        states (dict): A dictionary of states for the coffee machine.
        current_state (str): The current state of the coffee machine.
    """

    def __init__(self):
        """Initializes the CoffeeMachine instance with products and stock."""
        self.products = {
            'espresso': Product('espresso', 250, 0, 16, 1, 4),
            'latte': Product('latte', 350, 75, 20, 1, 7),
            'cappuccino': Product('cappuccino', 200, 100, 12, 1, 6)
        }
        self.coffee_machine_stock = {
            'water': 400,
            'milk': 540,
            'coffee beans': 120,
            'cups': 9,
            'money': 550
        }

        self.measurements = {
            'water': 'ml',
            'milk': 'ml',
            'coffee beans': 'g',
            'cups': 'disposable'
        }
        self.available_commands = {
            'buy': self.buy,
            'fill': self.fill,
            'take': self.take,
            'exit': self.exit,
            'remaining': self.remaining
        }

        self.states = {
            'main_menu': self.main_menu,
            'buy_state': self.buy,
        }

        self.current_state = 'main_menu'
        self.state_handler(self.current_state)

    def state_handler(self, current_state=None):
        """
        Handles the current state of the coffee machine.

        Args:
            current_state (str, optional): The state to transition to. Defaults to None.
        """
        if current_state is None:
            self.states.get(self.current_state)()
        elif current_state in self.states:
            self.states.get(current_state)()
        else:
            print('Input right command.')

    def main_menu(self):
        """Displays the main menu and processes user input."""
        user_input = input(self.display_commands()).lower()
        result = self.check_user_input(user_input, self.available_commands)
        if callable(result):
            result()
        else:
            print(result)
            self.state_handler()

    def buy(self):
        """Handles the buying process of coffee products."""
        user_input = input(self.display_drinks().strip() + ', back - to main menu: \n')
        if user_input == 'back':
            return self.state_handler()
        try:
            user_input = int(user_input)
            product_name = self.check_user_input(user_input, {i + 1: name for i, name in enumerate(self.products)})
            if product_name != 'Wrong input!':
                self.make_calculations(self.products[product_name].ingredients)
                self.state_handler()
            else:
                print(product_name)
        except ValueError:
            print("Invalid input. Please enter a valid integer or 'back'.")
            self.state_handler('buy_state')

    def fill(self):
        """Fills the coffee machine with additional ingredients."""
        self.coffee_machine_stock['water'] += self.get_positive_integer('Write how many ml of water you want to add: ')
        self.coffee_machine_stock['milk'] += self.get_positive_integer('Write how many ml of milk you want to add: ')
        self.coffee_machine_stock['coffee beans'] += self.get_positive_integer('Write how many grams of coffee beans you want to add: ')
        self.coffee_machine_stock['cups'] += self.get_positive_integer('Write how many disposable cups you want to add: ')
        print()
        self.state_handler()

    def take(self):
        """Withdraws the money from the coffee machine."""
        print(f"I gave you {self.coffee_machine_stock['money']}$\n")
        self.coffee_machine_stock['money'] = 0
        self.state_handler()

    def display_commands(self):
        """Displays the available commands to the user."""
        prompt = 'Write action: ' + ' '.join(f'{method.__name__.capitalize()}' for key, method in self.available_commands.items()) + '\n'
        return prompt

    def display_drinks(self):
        """Displays the available drinks to the user."""
        prompt = 'What do you want to buy?: ' + ' '.join(f'{i + 1}: {name.capitalize()}' for i, name in enumerate(self.products)) + '\n'
        return prompt

    def check_user_input(self, user_input, dictionary):
        """
        Checks the user input against a dictionary.

        Args:
            user_input (str/int): The input from the user.
            dictionary (dict): The dictionary to check against.

        Returns:
            str: The corresponding value from the dictionary or 'Wrong input!'.
        """
        return dictionary.get(user_input, 'Wrong input!')

    def get_positive_integer(self, prompt):
        """
        Prompts the user for a positive integer input.

        Args:
            prompt (str): The prompt message to display.

        Returns:
            int: A positive integer input from the user.
        """
        while True:
            try:
                value = int(input(prompt))
                if value < 0:
                    print("Please enter a non-negative number.")
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def make_calculations(self, ingredients):
        """
        Checks if there are enough ingredients to make the coffee and updates the stock.

        Args:
            ingredients (dict): The ingredients required to make the coffee.
        """
        for item, value in ingredients.items():
            if item != 'money' and self.coffee_machine_stock[item] < value:
                print(f"Sorry, not enough {item}!\n")
                return
        for item, value in ingredients.items():
            if item != 'money':
                self.coffee_machine_stock[item] -= value
            else:
                self.coffee_machine_stock[item] += value
        print('I have enough resources, making you a coffee!\n')

    def remaining(self):
        """Displays the remaining ingredients in the coffee machine."""
        print('The coffee machine has:')
        for item, value in self.coffee_machine_stock.items():
            if item == 'money':
                print(f"{value}$ of money")
            else:
                print(f"{value} {self.measurements[item]} {item}")
        print()
        self.state_handler()

    def exit(self):
        """Exits the coffee machine program."""
        exit()


def main():
    """Main function to run the coffee machine."""
    coffee_machine = CoffeeMachine()

if __name__ == '__main__':
    main()