"""_summary_
"""

def create_account(account_number, balance):
    """_summary_
    """
    print(f"Account: {account_number} is created with balance: {balance}")
    return {"account_number": account_number, "balance": balance}


def deposit(account, amount):
    """_summary_
    """
    if amount > 0:
        account["balance"]  += amount
        print(f"Deposited {amount} to {account['account_number']}"
                f"account and new balance is {account['balance']}")
    else:
        print(f"Invalid amount: {amount}")


def withdraw(account, amount):
    """_summary_
    """
    if amount > 0 and amount < account["balance"]:
        account["balance"]  -= amount
        print(f"{amount} is withdrawn from {account['account_number']}"
                f"and new balance is {account['balance']}")
    else:
        print(f"Invalid amount: {amount}")


def get_balance(account):
    """_summary_
    """
    print(f"{account['account_number']} account balance is {account['balance']}")
    return account['balance']


account_01 = create_account(account_number="34242342343", balance=25000)
deposit(account_01, 2000)
withdraw(account_01, 500)
get_balance(account_01)
