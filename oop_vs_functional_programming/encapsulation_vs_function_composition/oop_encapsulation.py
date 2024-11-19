"""_summary_
"""

class BankAccount:
    """
        summary
    """
    def __init__(self, account_number, balance):
        self.__account_number = account_number
        self.__balance = balance
        print(f"Account: {self.__account_number} is created with balance: {balance}")


    def deposit(self, amount):
        """_summary_

        Args:
            amount (_type_): _description_
        """
        if amount > 0:
            self.__balance  += amount
            print(f"Deposited {amount} to {self.__account_number} "
                  f"account and new balance is {self.__balance}")
        else:
            print(f"Invalid amount: {amount}")


    def withdraw(self, amount):
        """_summary_

        Args:
            amount (_type_): _description_
        """
        if amount > 0 and amount < self.__balance:
            self.__balance  -= amount
            print(f"{amount} is withdrawn from {self.__account_number} "
                  f"and new balance is {self.__balance}")
        else:
            print(f"Invalid amount: {amount}")


    def get_balance(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        print(f"{self.__account_number} account balance is {self.__balance}")
        return self.__balance

account_01 = BankAccount(account_number="34242342343", balance=25000)
account_01.deposit(2000)
account_01.withdraw(500)
account_01.get_balance()
