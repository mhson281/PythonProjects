import math
import argparse


class CreditCalc:

    def __init__(self):
        # Initialize the parser
        self.parser = argparse.ArgumentParser(description="Loan calculator")

        # Add the parameters positional/optional
        self.parser.add_argument("-t", "--type", choices=['annuity', 'diff'], help="Incorrect parameters.")
        self.parser.add_argument("-p", "--payment", help="monthly payment amount", type=float)
        self.parser.add_argument("-P", "--principal", help="total loan amount", type=int)
        self.parser.add_argument("-n", "--periods", help="number of payments", type=int)
        self.parser.add_argument("-i", "--interest", help="Incorrect parameters.", type=float, default=1)

        # Parse the arguments
        self.args = self.parser.parse_args()

    def main(self):
        if self.args.type != 'diff' and self.args.type != 'annuity':
            print('Incorrect parameters')
        if self.args.interest >= 0:
            print('Incorrect parameters')

        if self.args.type == "annuity":
            loan_principal = self.args.principal
            annuity_payment = self.args.payment
            monthly_interest = self.args.interest / 1200
            if self.args.periods is None:
                number_of_months = math.ceil(
                    math.log((annuity_payment / (annuity_payment - monthly_interest * loan_principal)),
                             1 + monthly_interest))
                convert_to_years = math.floor(number_of_months // 12)
                convert_to_months = math.ceil(number_of_months % 12)
                if convert_to_years == 0 and convert_to_months != 0:
                    print("It will take {} months to repay this loan".format(convert_to_months))
                elif convert_to_months == 0 and convert_to_years != 0:
                    print("It will take {} years to repay this loan".format(convert_to_years))
                elif convert_to_months == 1 and convert_to_years == 0:
                    print("It will take 1 month to repay this loan")
                elif convert_to_years == 1 and convert_to_months == 0:
                    print("It will take 1 year to repay this loan")
                else:
                    print("It will take {} years and {} months to repay this loan!".format
                          (round(number_of_months // 12), round(number_of_months % 12)))
                print("Overpayment = {}".format(math.ceil(annuity_payment * number_of_months - loan_principal)))
            elif self.args.payment is None:
                loan_principal = self.args.principal
                number_of_periods = self.args.periods
                monthly_interest = self.args.interest / 1200
                annuity_payment = (loan_principal * (
                        monthly_interest * (1 + monthly_interest) ** number_of_periods)) / (
                                          (1 + monthly_interest) ** number_of_periods - 1)
                print("Your annuity payment = {}!".format(math.ceil(annuity_payment)))
                print("Overpayment = {}".format(math.ceil(annuity_payment) * number_of_periods - loan_principal))
            elif self.args.principal is None:
                annuity_payment = self.args.payment
                number_of_periods = self.args.periods
                monthly_interest = self.args.interest / 1200
                loan_principal = (annuity_payment * ((1 + monthly_interest) ** number_of_periods - 1)) / (
                        monthly_interest * (1 + monthly_interest) ** number_of_periods)
                print("Your loan principal = {}!".format(math.floor(loan_principal)))
                print("Overpayment = {}".format(math.ceil(annuity_payment * number_of_periods - loan_principal)))

        elif self.args.type == "diff":
            loan_principal = self.args.principal
            number_of_months = self.args.periods
            monthly_interest = self.args.interest / 1200
            i_month = 0  # mth differentiated payment
            payments_principal = 0
            if monthly_interest is None or number_of_months is None:
                print("Incorrect parameters")
            else:
                while i_month < number_of_months:
                    i_month += 1
                    payment = (loan_principal / number_of_months) + monthly_interest * \
                              (loan_principal - ((loan_principal * (i_month - 1)) / number_of_months))
                    payments_principal += math.ceil(payment)
                    print("Month {}: payment is {}".format(i_month, math.ceil(payment)))
                print()
                print("Overpayment = {}".format(payments_principal - loan_principal))


if __name__ == '__main__':
    CreditCalc().main()
