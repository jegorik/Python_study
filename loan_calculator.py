import argparse
import math


class LoanCalculator:
    """
    A class to calculate loan-related information based on user input.

    Attributes:
    - args: Holds the parsed arguments from user input.
    - VALID_ARGUMENTS: List of valid arguments for the loan calculation.

    Methods:
    - parse_arguments(): Parses the user input arguments using argparse.
    - validate_arguments(): Validates the user input arguments for correctness.
    - calculate_user_input(): Determines the type of calculation based on user input.
    - calculate_months_to_pay(): Calculates the number of months to repay the loan.
    - calculate_monthly_payment(): Calculates the monthly payment amount.
    - calculate_diff_payment(): Calculates the differentiated payment schedule.
    - calculate_annuity_payment(): Calculates the annuity payment amount.
    - calculate_loan_principal(): Calculates the loan principal amount.
    - interest_rate(): Calculates the monthly interest rate.
    - print_months_to_pay(): Formats the output for months to repay the loan.
    - calculate_overpayment(): Calculates the overpayment amount.

    """
    # Example of user_input: --type=diff --principal=1000000 --periods=10 --interest=10
    # put as entry arguments

    args = None
    VALID_ARGUMENTS = ['payment', 'principal', 'periods', 'interest']

    def __init__(self):
        self.args = self.parse_arguments()
        self.validate_arguments()
        self.initialize_loan_calculation()

    def initialize_loan_calculation(self):
        """
        Method to calculate the user input for loan calculation.
        """
        self.calculate_user_input()

    @staticmethod
    def parse_arguments():
        """
        Parses the user input arguments using argparse.

        Returns:
        - Parsed arguments from user input.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('--payment', type=float)
        parser.add_argument('--principal', type=int)
        parser.add_argument('--periods', type=int)
        parser.add_argument('--interest', type=float)
        parser.add_argument('--type')
        return parser.parse_args()

    def validate_arguments(self):
        """
        Validates the user input arguments for correctness.
        Exits the program if parameters are incorrect.
        """
        if self.args.type not in ["annuity", "diff"]:
            exit(print("Incorrect parameters"))

        for argument in self.VALID_ARGUMENTS:
            value = getattr(self.args, argument)
            if value is not None and value < 0:
                exit(print("Incorrect parameters"))

    def calculate_user_input(self):
        """
        Determines the type of calculation based on user input.
        """
        if self.args.payment is None:
            if all([self.args.principal, self.args.periods, self.args.interest]):
                self.calculate_monthly_payment()
                return
        elif self.args.principal is None:
            if all([self.args.payment, self.args.periods, self.args.interest]):
                self.calculate_loan_principal()
                return
        elif self.args.periods is None:
            if all([self.args.payment, self.args.principal, self.args.interest]):
                self.calculate_months_to_pay()
                return

        print("Incorrect parameters")

    def calculate_months_to_pay(self):
        """
        Calculates the number of months to repay the loan.
        """
        payment = self.args.payment
        principal = self.args.principal
        interest_rate = self.interest_rate()

        months_amount = math.ceil(math.log(payment / (payment - interest_rate * principal), 1 + interest_rate))

        years, months = divmod(months_amount, 12)

        total_paid = months_amount * payment

        if months > 0:
            years += months // 12
            months %= 12

        print(self.print_months_to_pay(years, months))
        print(self.calculate_overpayment(total_paid, principal))

    def calculate_monthly_payment(self):
        """
        Calculates the monthly payment amount.
        """
        principal = self.args.principal
        periods = self.args.periods
        interest_rate = self.interest_rate()
        type_of_payment = self.args.type
        total_paid = 0

        if type_of_payment == 'diff':
            total_paid = self.calculate_diff_payment(periods, principal, interest_rate)
        elif type_of_payment == 'annuity':
            total_paid = self.calculate_annuity_payment(periods, principal, interest_rate)

        print(self.calculate_overpayment(total_paid, principal))

    @staticmethod
    def calculate_diff_payment(periods, principal, interest_rate):
        """
        Calculates the differentiated payment schedule.
        """
        total_paid = 0
        for month in range(0, periods):
            result = math.ceil(
                round(principal / periods + interest_rate * (principal - ((principal * month - 1) / periods)),
                      2))
            total_paid += result
            print(f'Month {month + 1}: payment is {result}')
        print()
        return total_paid

    @staticmethod
    def calculate_annuity_payment(periods, principal, interest_rate):
        """
        Calculates the annuity payment amount.
        """
        result = math.ceil(principal * (interest_rate * pow(1 + interest_rate, periods)) / (
                pow(1 + interest_rate, periods) - 1))
        total_paid = result * periods
        print(f'Your monthly payment = {result}!')
        return total_paid

    def calculate_loan_principal(self):
        """
        Calculates the loan principal amount based on user input.

        Prints the loan principal and overpayment information.
        """
        payments = self.args.payment
        periods = self.args.periods
        interest_rate = self.interest_rate()
        principal = math.floor(payments / (interest_rate * pow(1 + interest_rate, periods) / (
                pow(1 + interest_rate, periods) - 1)))
        total_loan = payments * periods
        print(f'Your loan principal = {principal}!')
        print(self.calculate_overpayment(total_loan, principal))

    def interest_rate(self):
        """
        Calculates the monthly interest rate based on the user input.

        Returns:
        - Monthly interest rate.
        """
        interest = self.args.interest
        return interest / (12 * 100)

    @staticmethod
    def print_months_to_pay(years, months):
        """
        Formats the output for the number of months to repay the loan.

        Args:
        - years: Number of years to repay the loan.
        - months: Number of months to repay the loan.

        Returns:
        - Formatted string indicating the time to repay the loan.
        """
        years_str = f'{years} {"years" if years != 1 else "year"} ' if years != 0 else ''
        months_str = f'{months} {"months" if months != 1 else "month"}' if months != 0 else ''

        if years_str and months_str:
            middle_str = 'and '
        else:
            middle_str = ''

        return f'It will take {years_str}{middle_str}{months_str}to repay this loan!'

    @staticmethod
    def calculate_overpayment(total_amount, principal):
        """
        Calculates the overpayment amount for the loan.

        Args:
        - total_amount: Total amount paid over the loan period.
        - principal: Principal loan amount.

        Returns:
        - Formatted string indicating the overpayment amount.
        """
        return f'Overpayment: {math.ceil(total_amount - principal)}'


def main():
    """
    Main function to initiate the LoanCalculator class and perform loan calculations.
    """
    LoanCalculator()


if __name__ == '__main__':
    main()
