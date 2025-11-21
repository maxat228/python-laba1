import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
# noinspection PyUnresolvedReferences
from calculator import tokenize_char, shunting_yard, calculate

def test_tokenize_valid_expressions(valid_expressions):
    for expr in valid_expressions.values():
        tokens = tokenize_char(expr)
        assert len(tokens) > 0

def test_tokenize_invalid_expressions(invalid_expressions):
    for expr in invalid_expressions.values():
        with pytest.raises(ValueError):
            tokenize_char(expr)

def test_tokenize_unary_minus():
    tokens = tokenize_char("-5 + 3")
    assert tokens[0] == "-5"
    assert tokens[1] == "+"
    assert tokens[2] == "3"

def test_tokenize_nested_parentheses():
    expr = "((2 + 3) * (4 - (1 + 1)))"
    tokens = tokenize_char(expr)
    assert tokens.count("(") == 4
    assert tokens.count(")") == 4

def test_shunting_yard_basic(tokenized_expression):
    result = shunting_yard(tokenized_expression)
    assert '(' not in result
    assert ')' not in result

def test_shunting_yard_unbalanced_brackets():
    with pytest.raises(ValueError):
        shunting_yard(['(', '3', '+', '2'])

def test_shunting_yard_operator_order():
    tokens = ['2', '+', '3', '*', '4']
    result = shunting_yard(tokens)
    assert result == ['2', '3', '4', '*', '+']

def test_shunting_yard_with_parentheses():
    tokens = ['(', '2', '+', '3', ')', '*', '4']
    result = shunting_yard(tokens)
    assert result == ['2', '3', '+', '4', '*']

def test_calculate_postfix(postfix_expression):
    result = calculate(postfix_expression)
    assert "Операция выполнена успешно." in result

def test_calculate_floats():
    expr = ['5.5', '2.0', '*', '1', '+']
    result = calculate(expr)
    assert "Операция выполнена успешно." in result

def test_calculate_zero_division():
    with pytest.raises(ZeroDivisionError):
        calculate(['5', '0', '/'])

def test_calculate_invalid_integer_only():
    with pytest.raises(ValueError):
        calculate(['5.5', '2', ':'])
    with pytest.raises(ValueError):
        calculate(['3.3', '2', '%'])

def test_calculate_missing_operands():
    with pytest.raises(ValueError):
        calculate(['5', '+'])

def test_calculate_extra_operands():
    with pytest.raises(ValueError):
        calculate(['2', '3', '4', '+'])

def test_calculate_unary_minus_in_postfix():
    result = calculate(['-5', '3', '+'])
    assert "Операция выполнена успешно." in result

def test_full_pipeline(valid_expressions):
    for expr in valid_expressions.values():
        tokens = tokenize_char(expr)
        postfix = shunting_yard(tokens)
        result = calculate(postfix)
        assert "Операция выполнена успешно." in result

def test_full_pipeline_invalid(invalid_expressions):
    for expr in invalid_expressions.values():
        with pytest.raises(ValueError):
            tokens = tokenize_char(expr)
            postfix = shunting_yard(tokens)
            calculate(postfix)
            
