import pytest
from calculator import Calculator

class TestCalculator:
    """Test suite for Calculator class"""
    
    @pytest.fixture
    def calculator(self):
        """Fixture to create a Calculator instance for each test"""
        return Calculator()
    
    # Addition Tests
    def test_add_positive_numbers(self, calculator):
        assert calculator.add(5, 3) == 8
        
    def test_add_negative_numbers(self, calculator):
        assert calculator.add(-5, -3) == -8
        
    def test_add_zero(self, calculator):
        assert calculator.add(5, 0) == 5
        assert calculator.add(0, 5) == 5
        
    def test_add_floats(self, calculator):
        assert calculator.add(2.5, 3.7) == pytest.approx(6.2)
    
    # Subtraction Tests
    def test_subtract_positive_numbers(self, calculator):
        assert calculator.subtract(10, 4) == 6
        
    def test_subtract_negative_numbers(self, calculator):
        assert calculator.subtract(-10, -4) == -6
        
    def test_subtract_zero(self, calculator):
        assert calculator.subtract(5, 0) == 5
        assert calculator.subtract(0, 5) == -5
        
    def test_subtract_floats(self, calculator):
        assert calculator.subtract(5.5, 2.2) == pytest.approx(3.3)
    
    # Multiplication Tests
    def test_multiply_positive_numbers(self, calculator):
        assert calculator.multiply(6, 7) == 42
        
    def test_multiply_negative_numbers(self, calculator):
        assert calculator.multiply(-6, -7) == 42
        assert calculator.multiply(-6, 7) == -42
        
    def test_multiply_zero(self, calculator):
        assert calculator.multiply(5, 0) == 0
        assert calculator.multiply(0, 5) == 0
        
    def test_multiply_floats(self, calculator):
        assert calculator.multiply(2.5, 3.0) == pytest.approx(7.5)
    
    # Division Tests
    def test_divide_positive_numbers(self, calculator):
        assert calculator.divide(15, 3) == 5
        
    def test_divide_negative_numbers(self, calculator):
        assert calculator.divide(-15, -3) == 5
        assert calculator.divide(-15, 3) == -5
        
    def test_divide_by_one(self, calculator):
        assert calculator.divide(5, 1) == 5
        
    def test_divide_zero_by_number(self, calculator):
        assert calculator.divide(0, 5) == 0
        
    def test_divide_floats(self, calculator):
        assert calculator.divide(5.0, 2.0) == pytest.approx(2.5)
    
    def test_divide_by_zero_raises_error(self, calculator):
        with pytest.raises(ValueError) as exc_info:
            calculator.divide(5, 0)
        assert str(exc_info.value) == "Cannot divide by zero"
    
    # Power Tests
    def test_power_positive_numbers(self, calculator):
        assert calculator.power(2, 3) == 8
        
    def test_power_negative_base(self, calculator):
        assert calculator.power(-2, 3) == -8
        assert calculator.power(-2, 2) == 4
        
    def test_power_zero_exponent(self, calculator):
        assert calculator.power(5, 0) == 1
        assert calculator.power(0, 0) == 1
        
    def test_power_one_exponent(self, calculator):
        assert calculator.power(5, 1) == 5
        
    def test_power_zero_base(self, calculator):
        assert calculator.power(0, 5) == 0
        
    def test_power_floats(self, calculator):
        assert calculator.power(2.0, 3.0) == pytest.approx(8.0)
        
    def test_power_fractional_exponent(self, calculator):
        assert calculator.power(4, 0.5) == pytest.approx(2.0)

    # Type Tests
    def test_operations_return_float(self, calculator):
        assert isinstance(calculator.add(1, 2), float)
        assert isinstance(calculator.subtract(1, 2), float)
        assert isinstance(calculator.multiply(1, 2), float)
        assert isinstance(calculator.divide(1, 2), float)
        assert isinstance(calculator.power(1, 2), float)