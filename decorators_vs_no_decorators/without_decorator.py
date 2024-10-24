"""
 summary
"""

def authenticate(user):
    """_summary_

    Args:
        user (_type_): _description_

    Returns:
        _type_: _description_
    """
    if user != "admin":
        print("Unauthorized access!")
        return False
    print("Authorized access!")
    return True


def log_request(endpoint):
    """_summary_

    Args:
        request (_type_): _description_
    """
    print(f"Logging request: {endpoint}")


def get_user_data(user, user_id):
    """fetch user data endpoint

    Args:
        user (_type_): _description_
        user_id (_type_): _description_
    """
    log_request("/user_data")

    if not authenticate(user):
        print(f"Authentication failed for: {user}")
        return {"status": False, "message": "Unauthorized access!", "data": None}

    # simulate user data fetching process
    print(f"Fetching user data for: {user}")

    return {
            "status": True
            ,"message": "Successfully fetched data"
            ,"data": {
                "user_id": user_id
                ,"name": "Vidumini Sulochana"
              }
           }


def process_payment(user, amount):
    """process payment endpoint

    Args:
        user (_type_): _description_
        amount (_type_): _description_
    """
    log_request("/payment_process")

    if not authenticate(user):
        print(f"Authentication failed for: {user}")
        return {"status": False, "message": "Unauthorized access!", "data": None}

    # simulate payment process
    print(f"Processing {amount} amount of payment for: {user}")
    return {
            "status": True
            ,"message": "Successfully processed payment"
            ,"data": {
                "amount": amount
              }
           }


get_user_data("admin", 1)
# Logging request: /user_data
# Authorized access!
# Fetching user data for: admin

get_user_data("guest", 2)
# Logging request: /user_data
# Unauthorized access!
# Authentication failed for: guest
