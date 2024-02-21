import datetime


class ChatBot:
    """
    A simple chatbot program that interacts with the user by guessing their age, counting numbers, and testing programming knowledge.
    """

    def __init__(self):
        """
        Initializes the ChatBot with a default name and birthdate.
        """
        self.name = 'Aid'
        self.birthdate = datetime.date.today().year
        self.greet()

    def greet(self):
        """
        Greets the user and asks for their name.
        """
        print(f'Hello! My name is {self.name}.')
        print(f'I was created in {self.birthdate}.')
        user_name = input('Please, remind me your name.\n')
        print(f'What a great name you have, {user_name}!')

    def guess_user_age(self):
        """
        Guesses the user's age based on remainders of dividing by 3, 5, and 7.
        """
        print('Let me guess your age.')
        print('Enter remainders of dividing your age by 3, 5, and 7.')
        user_age = self.calculate_user_age()
        print(f"Your age is {user_age}; that's a good time to start programming!")

    def calculate_user_age(self):
        """
        Calculates the user's age based on remainders provided by the user.
        """
        reminders = [3, 5, 7]
        multipliers = [70, 21, 15]
        user_inputs = self.validate_user_input(reminders)
        user_age = sum(value * multiplier for value, multiplier in zip(user_inputs, multipliers)) % 105
        return user_age

    @staticmethod
    def count_numbers():
        """
        Counts numbers up to a user-specified number.
        """
        number = input('Now I will prove to you that I can count to any number you want.\n')
        try:
            number = int(number)
            for i in range(number + 1):
                print(f'{i} !')
            print('Completed, have a nice day!')
        except ValueError:
            print('Please enter a valid number.')

    @staticmethod
    def validate_user_input(reminders):
        """
        Validates user input for remainders.
        """
        user_inputs = []
        for reminder in reminders:
            while True:
                value = input(f'Reminder {reminder}: ')
                if value.isdigit():
                    user_inputs.append(int(value))
                    break
                else:
                    print('Please, enter a number.')
        return user_inputs

    def test(self):
        """
        Tests the user's programming knowledge with a multiple-choice question.
        """
        question_options = {
            "question": "Why do we use methods?",
            "options": {
                1: "To repeat a statement multiple times.",
                2: "To decompose a program into several small subroutines.",
                3: "To determine the execution time of a program.",
                4: "To interrupt the execution of a program."
            }
        }
        print("Let's test your programming knowledge.")
        print(question_options["question"])
        for option, text in question_options["options"].items():
            print(f"{option}. {text}")
        while True:
            user_input = self.get_user_input()
            if user_input.isdigit():
                answer = int(user_input)
                correct_answer = 2
                if answer == correct_answer:
                    print('Congratulations, have a nice day!')
                    break
                else:
                    print('Please, try again.')
            else:
                print('Please, enter a number.')

    def get_user_input(self):
        """
        Gets user input.
        """
        return input()


# Instantiate the ChatBot and interact with the user
chat_bot = ChatBot()
chat_bot.guess_user_age()
chat_bot.count_numbers()
chat_bot.test()
