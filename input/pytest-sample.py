import pytest

def capital_case(x):
    return x.capitalize()
#exemplo de código de teste
def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'

def test_capital_case1():
    assert capital_case('semaphore') == 'Semaphore'

def test_raises_exception_on_non_string_arguments():
    with pytest.raises(TypeError):
        capital_case('semaphore')