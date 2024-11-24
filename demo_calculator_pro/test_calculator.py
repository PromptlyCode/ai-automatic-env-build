import pytest
from calculator import Calculator

class TestCalculator:
    @pytest.fixture
    def calculator(self):
        """Fixture to create a new calculator instance for each test."""
        return Calculator()

    def test_initialization(self, calculator):
        """Test that calculator initializes with zero values."""
        assert calculator.memory == 0
        assert calculator.last_result == 0

    def test_add(self, calculator):
        """Test addition functionality."""
        assert calculator.add(2, 3) == 5
        assert calculator.add(-1, 1) == 0
        assert calculator.add(0.1, 0.2) == pytest.approx(0.3)
        assert calculator.get_last_result() == pytest.approx(0.3)

    def test_subtract(self, calculator):
        """Test subtraction functionality."""
        assert calculator.subtract(5, 3) == 2
        assert calculator.subtract(1, 5) == -4
        assert calculator.subtract(0.5, 0.2) == pytest.approx(0.3)
        assert calculator.get_last_result() == pytest.approx(0.3)

    def test_multiply(self, calculator):
        """Test multiplication functionality."""
        assert calculator.multiply(2, 3) == 6
        assert calculator.multiply(-2, 3) == -6
        assert calculator.multiply(0.5, 0.2) == pytest.approx(0.1)
        assert calculator.get_last_result() == pytest.approx(0.1)

    def test_divide(self, calculator):
        """Test division functionality."""
        assert calculator.divide(6, 2) == 3
        assert calculator.divide(5, 2) == 2.5
        assert calculator.divide(-6, 2) == -3
        assert calculator.get_last_result() == -3

    def test_divide_by_zero(self, calculator):
        """Test division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(5, 0)

    def test_clear(self, calculator):
        """Test clear functionality."""
        calculator.add(5, 3)
        calculator.store_in_memory()
        calculator.clear()
        assert calculator.last_result == 0
        assert calculator.memory == 0

    def test_get_last_result(self, calculator):
        """Test getting last result."""
        calculator.add(2, 3)
        assert calculator.get_last_result() == 5
        calculator.multiply(4, 2)
        assert calculator.get_last_result() == 8

    def test_memory_operations(self, calculator):
        """Test memory store, recall, and clear operations."""
        # Test storing and recalling
        calculator.add(5, 3)
        calculator.store_in_memory()
        assert calculator.recall_memory() == 8
        
        # Test memory persists after new calculations
        calculator.add(1, 1)
        assert calculator.recall_memory() == 8
        
        # Test clear memory
        calculator.clear_memory()
        assert calculator.recall_memory() == 0

    def test_floating_point_precision(self, calculator):
        """Test handling of floating point calculations."""
        result = calculator.add(0.1, 0.2)
        assert result == pytest.approx(0.3)
        
        result = calculator.multiply(0.1, 0.3)
        assert result == pytest.approx(0.03)

    def test_negative_numbers(self, calculator):
        """Test operations with negative numbers."""
        assert calculator.add(-2, -3) == -5
        assert calculator.subtract(-5, -3) == -2
        assert calculator.multiply(-2, -3) == 6
        assert calculator.divide(-6, -2) == 3

    def test_operation_sequence(self, calculator):
        """Test a sequence of operations."""
        calculator.add(5, 3)  # 8
        calculator.store_in_memory()
        calculator.multiply(2, 4)  # 8
        calculator.subtract(3, 1)  # 2
        calculator.divide(10, 2)  # 5
        assert calculator.get_last_result() == 5
        assert calculator.recall_memory() == 8