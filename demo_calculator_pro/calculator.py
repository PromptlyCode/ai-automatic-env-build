class Calculator:
    """
    A calculator class that performs basic arithmetic operations.
    
    This class provides methods for addition, subtraction, multiplication,
    division, and additional utility functions like clear and memory operations.
    """
    
    def __init__(self):
        """Initialize the calculator with a memory value of 0."""
        self.memory = 0
        self.last_result = 0

    def add(self, x: float, y: float) -> float:
        """
        Add two numbers together.
        
        Args:
            x (float): First number
            y (float): Second number
            
        Returns:
            float: Sum of x and y
        """
        self.last_result = x + y
        return self.last_result

    def subtract(self, x: float, y: float) -> float:
        """
        Subtract the second number from the first number.
        
        Args:
            x (float): First number
            y (float): Second number
            
        Returns:
            float: Difference of x and y
        """
        self.last_result = x - y
        return self.last_result

    def multiply(self, x: float, y: float) -> float:
        """
        Multiply two numbers.
        
        Args:
            x (float): First number
            y (float): Second number
            
        Returns:
            float: Product of x and y
        """
        self.last_result = x * y
        return self.last_result

    def divide(self, x: float, y: float) -> float:
        """
        Divide the first number by the second number.
        
        Args:
            x (float): First number (dividend)
            y (float): Second number (divisor)
            
        Returns:
            float: Quotient of x and y
            
        Raises:
            ValueError: If attempting to divide by zero
        """
        if y == 0:
            raise ValueError("Cannot divide by zero")
        self.last_result = x / y
        return self.last_result

    def clear(self) -> None:
        """Reset the last result and memory to 0."""
        self.last_result = 0
        self.memory = 0

    def get_last_result(self) -> float:
        """
        Get the last calculated result.
        
        Returns:
            float: The last calculated result
        """
        return self.last_result

    def store_in_memory(self) -> None:
        """Store the last result in memory."""
        self.memory = self.last_result

    def recall_memory(self) -> float:
        """
        Recall the value stored in memory.
        
        Returns:
            float: The value stored in memory
        """
        return self.memory

    def clear_memory(self) -> None:
        """Clear the memory by setting it to 0."""
        self.memory = 0


# Example usage
if __name__ == "__main__":
    # Create a calculator instance
    calc = Calculator()
    
    # Perform some calculations
    print(calc.add(5, 3))        # Output: 8
    print(calc.subtract(10, 4))  # Output: 6
    print(calc.multiply(2, 3))   # Output: 6
    print(calc.divide(8, 2))     # Output: 4.0
    
    # Store result in memory
    calc.store_in_memory()
    
    # Perform more calculations
    print(calc.add(10, 5))       # Output: 15
    
    # Recall from memory
    print(f"Memory value: {calc.recall_memory()}")  # Output: Memory value: 4.0
    
    # Clear calculator
    calc.clear()
    print(f"After clear: {calc.get_last_result()}")  # Output: After clear: 0
    
    # Test division by zero error handling
    try:
        calc.divide(5, 0)
    except ValueError as e:
        print(f"Error: {e}")  # Output: Error: Cannot divide by zero