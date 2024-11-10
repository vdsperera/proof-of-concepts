"""_summary_

Returns:
	_type_: _description_
"""


class Person:
    """_summary_"""

    def __init__(self, name, age):
        """_summary_

        Args:
                name (_type_): _description_
                age (_type_): _description_
        """
        self.name = name
        self.age = age

    def describe(self):
        """_summary_

        Returns:
                _type_: _description_
        """
        return f"{self.name} is {self.age} years old"


person = Person(name="Vidumini", age=28)
print(person.describe())
