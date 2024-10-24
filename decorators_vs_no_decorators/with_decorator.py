"""_summary_
"""

def authenticate(original_function: callable):
    """decorator function to authenticate

    Args:
        func (_type_): _description_
    """
    def modified_function(user: str, *args, **kwargs):
        if user != "admin":
            print("Unauthorized access!")
            return {"status": False, "message": "Unauthorized access!", "data": None}
        print("Authorized access!")
        return original_function(user, *args, **kwargs)
    return modified_function


def log_request(endpoint: str):
    """outer function to enclose decorator function

    Args:
        func (_type_): _description_
    """
    def decorator_function(original_function: callable):
        """decorator function to log requests

        Args:
            original_function (_type_): _description_
        """
        def modified_function(*args, **kwargs):
            print(f"Logging request: {endpoint}")
            return original_function(*args, **kwargs)

        return modified_function
    return decorator_function


@authenticate
@log_request("/get_user_data")
def get_user_data(user, user_id):
    """fetch user data endpoint

    Args:
        user (_type_): _description_
        user_id (_type_): _description_
    """
    # log_request("/user_data")

    # simulate user data fetching process
    print(f"Fetching user data for {user} with user id: {user_id}")

    return {
            "status": True
            ,"message": "Successfully fetched data"
            ,"data": {
                "user_id": user_id
                ,"name": "Vidumini Sulochana"
              }
           }


@authenticate
@log_request("/process_payment")
def process_payment(user, amount):
    """_summary_

    Args:
        amount (_type_): _description_

    Returns:
        _type_: _description_
    """
    # simulate payment process
    print(f"Processing {amount} amount of payment for {user}")
    return {
            "status": True
            ,"message": "Successfully processed payment"
            ,"data": {
                "amount": amount
              }
           }


# get_user_data("guest", 2)
# Unauthorized access!

get_user_data("admin", 1)
# Authorized access!
# Logging request: /get_user_data
# Fetching user data for admin with user id: 1
