class Calculator:
    """
    A calculator class that performs basic arithmetic operations.
    
    This class provides methods for addition, subtraction, multiplication,
    division, and power operations with error handling.
    """
    
    def __init__(self):
        """Initialize the Calculator class."""
        pass
    
    def add(self, x: float, y: float) -> float:
        """
        Add two numbers.
        
        Args:
            x (float): First number
            y (float): Second number
            
        Returns:
            float: Sum of x and y
        """
        return x + y
    
    def subtract(self, x: float, y: float) -> float:
        """
        Subtract two numbers.
        
        Args:
            x (float): First number
            y (float): Second number
            
        Returns:
            float: Difference of x and y (x - y)
        """
        return x - y
    
    def multiply(self, x: float, y: float) -> float:
        """
        Multiply two numbers.
        
        Args:
            x (float): First number
            y (float): Second number
            
        Returns:
            float: Product of x and y
        """
        return x * y
    
    def divide(self, x: float, y: float) -> float:
        """
        Divide two numbers.
        
        Args:
            x (float): Numerator
            y (float): Denominator
            
        Returns:
            float: Quotient of x and y (x / y)
            
        Raises:
            ValueError: If attempting to divide by zero
        """
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y
    
    def power(self, x: float, y: float) -> float:
        """
        Raise x to the power of y.
        
        Args:
            x (float): Base number
            y (float): Exponent
            
        Returns:
            float: x raised to the power of y
        """
        return x ** y


# Example usage
def main():
    # Create calculator instance
    calc = Calculator()
    
    try:
        # Test basic operations
        print(f"Addition: 5 + 3 = {calc.add(5, 3)}")
        print(f"Subtraction: 10 - 4 = {calc.subtract(10, 4)}")
        print(f"Multiplication: 6 * 7 = {calc.multiply(6, 7)}")
        print(f"Division: 15 / 3 = {calc.divide(15, 3)}")
        print(f"Power: 2 ^ 3 = {calc.power(2, 3)}")
        
        # Test error handling
        print(f"Division by zero: 5 / 0 = {calc.divide(5, 0)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()