import pytest

def calculate_sum(numbers):
    return sum(numbers)

@pytest.fixture
def sample_numbers():
    return [10, 20, 30]

def test_calculate_sum(sample_numbers):
    result = calculate_sum(sample_numbers)

    assert result == 60



def calculate_total(order):
    subtotal = order["subtotal"]
    tax_rate = order["tax_rate"]
    return subtotal + (subtotal * tax_rate)

@pytest.fixture
def sample_data():
    return{"subtotal":80,
           "tax_rate":.1,
           "total":88}

def test_calculate_total(sample_data):
    assert calculate_total(sample_data) == sample_data["total"]
    


