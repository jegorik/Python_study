class FinancialCalculator:
    def __init__(self):
        self.prices = {
            'bubblegum': 2,
            'toffee': 0.2,
            'ice_cream': 5,
            'milk_chocolate': 4,
            'doughnut': 2.5,
            'pancake': 3.2
        }
        self.profit_by_product = {
            'bubblegum': 202,
            'toffee': 118,
            'ice_cream': 2250,
            'milk_chocolate': 1680,
            'doughnut': 1075,
            'pancake': 80
        }
        self.staff_expenses = {}
        self.other_expenses = {}

    def make_user_request(self, request):
        """
        Makes a user request and prints the corresponding data.

        Args:
            request (str): The user request.

        Returns:
            None
        """
        request = request.lower()
        requested_data = {
            'prices': {'data': self.prices, 'header': 'Prices:'},
            'profit': {'data': self.profit_by_product, 'header': 'Earned amount:',
                       'footer': f'Income: ${self.get_profit_by_product()}'},
            'staff expenses': {'data': self.staff_expenses, 'header': 'Staff expenses:',
                               'footer': self.get_staff_expenses()},
            'other expenses': {'data': self.other_expenses, 'header': 'Other expenses:',
                               'footer': self.get_other_expenses()},
            'net income': {'footer': self.get_net_income()}
        }

        data_info = requested_data.get(request)
        if data_info is None:
            raise KeyError(f"Request '{request}' not found in data dictionary")
        header = data_info.get('header')
        footer = data_info.get('footer')
        data = data_info.get('data')

        self.print_user_request(data, header, footer)

    def get_net_income(self):
        """
        Calculates and returns the net income.

        Returns:
            str: The net income.
        """
        total = self.get_profit_by_product() - self.get_staff_expenses() - self.get_other_expenses()
        return f'Net income: ${total}'

    def get_profit_by_product(self):
        """
        Calculates and returns the total profit by product.

        Returns:
            int: The total profit by product.
        """
        return sum(self.profit_by_product.values())

    def set_staff_expenses(self, value):
        """
        Sets the staff expenses.

        Args:
            value (int): The value of staff expenses.

        Returns:
            None
        """
        self.staff_expenses.update({'staff_expenses': value})

    def set_other_expenses(self, value):
        """
        Sets the other expenses.

        Args:
            value (int): The value of other expenses.

        Returns:
            None
        """
        self.other_expenses.update({'other_expenses': value})

    def get_staff_expenses(self):
        """
        Calculates and returns the total staff expenses.

        Returns:
            int: The total staff expenses.
        """
        return sum(self.staff_expenses.values())

    def get_other_expenses(self):
        """
        Calculates and returns the total other expenses.

        Returns:
            int: The total other expenses.
        """
        return sum(self.other_expenses.values())

    def print_user_request(self, data, header, footer):
        """
        Prints the user request data.

        Args:
            data (dict): The data to be printed.
            header (str): The header text.
            footer (str): The footer text.

        Returns:
            None
        """
        if data and header:
            print(header)
            for key, value in data.items():
                print(f'{key}: ${value}')
        if footer:
            print('\n' + footer)

    @classmethod
    def validate_user_input(cls, prompt):
        """
        Validates user input and returns an integer value.

        Args:
            prompt (str): The input prompt.

        Returns:
            int: The validated user input.
        """
        while True:
            user_input = input(prompt)
            if user_input.isdigit():
                return int(user_input)
            else:
                print('Please enter a number')


financial_calculator = FinancialCalculator()
financial_calculator.make_user_request('profit')
financial_calculator.set_staff_expenses(financial_calculator.validate_user_input('Staff expenses: \n'))
financial_calculator.set_other_expenses(financial_calculator.validate_user_input('Other expenses: \n'))
financial_calculator.make_user_request('net income')
