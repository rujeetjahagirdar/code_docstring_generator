def example_function(a, b):
    """
    This function takes two arguments and returns their sum.

    Args:
        a (int): The first number
        b (int): The second number

    Returns:
        int: The sum of the two numbers
    """
    return a + b


class ExampleClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        """
        Prints a greeting message that includes the name of the user.
        """
        print(f"Hello, {self.name}!")


def multiply_numbers(x, y):
    return x * y


# Example usage
if __name__ == "__main__":
    example = ExampleClass("John")
    example.greet()
    print(multiply_numbers(3, 4))
    print(example_function(2, 5))
