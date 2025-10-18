import pytest
from src.calculator import tokenize_char, shunting_yard, calculate

# Тесты для функции tokenize_char

def test_tokenize_valid_expressions(valid_expressions):
    # Проверяем, что токенизация возвращает список строк без ошибок.
    for expr in valid_expressions.values():
        tokens = tokenize_char(expr)
        assert isinstance(tokens, list)
        assert all(isinstance(t, str) for t in tokens)
        assert len(tokens) > 0


def test_tokenize_invalid_expressions(invalid_expressions):
    # Если выражение неправильное — должна быть ошибка.
    for expr in invalid_expressions.values():
        with pytest.raises(ValueError):
            tokenize_char(expr)


def test_tokenize_unary_minus():
    # Проверяем случай с унарным минусом (например, -5 + 3).
    tokens = tokenize_char("-5 + 3")
    assert tokens[0] == "-5"
    assert tokens[1] == "+"
    assert tokens[2] == "3"


def test_tokenize_nested_parentheses():
    # Сложные скобки — проверяем, что парсер не теряется.
    expr = "((2 + 3) * (4 - (1 + 1)))"
    tokens = tokenize_char(expr)
    assert tokens.count("(") == 4
    assert tokens.count(")") == 4


# Тесты для функции shunting_yard

def test_shunting_yard_basic(tokenized_expression):
    # Проверяем, что из инфиксной записи делается постфиксная.
    result = shunting_yard(tokenized_expression)
    assert '(' not in result
    assert ')' not in result


def test_shunting_yard_unbalanced_brackets():
    # Если скобки не закрыты — должна быть ошибка.
    with pytest.raises(ValueError):
        shunting_yard(['(', '3', '+', '2'])


def test_shunting_yard_operator_order():
    # Проверяем, что * имеет приоритет над +.
    tokens = ['2', '+', '3', '*', '4']
    result = shunting_yard(tokens)
    assert result == ['2', '3', '4', '*', '+']


def test_shunting_yard_with_parentheses():
    # Проверяем, что скобки правильно влияют на порядок.
    tokens = ['(', '2', '+', '3', ')', '*', '4']
    result = shunting_yard(tokens)
    assert result == ['2', '3', '+', '4', '*']


# Тесты для функции calculate

def test_calculate_postfix(postfix_expression):
    # Простая проверка, что посчиталось без ошибок.
    result = calculate(postfix_expression)
    assert "Операция выполнена успешно." in result


def test_calculate_floats():
    # Проверка на вещественные числа.
    expr = ['5.5', '2.0', '*', '1', '+']
    result = calculate(expr)
    assert "Операция выполнена успешно." in result


def test_calculate_zero_division():
    # Проверка деления на ноль.
    with pytest.raises(ZeroDivisionError):
        calculate(['5', '0', '/'])


def test_calculate_invalid_integer_only():
    # Операции %, : не должны работать с дробями.
    with pytest.raises(ValueError):
        calculate(['5.5', '2', ':'])
    with pytest.raises(ValueError):
        calculate(['3.3', '2', '%'])


def test_calculate_missing_operands():
    # Если не хватает чисел перед оператором — ошибка.
    with pytest.raises(ValueError):
        calculate(['5', '+'])


def test_calculate_extra_operands():
    # Если чисел больше, чем операций — тоже ошибка.
    with pytest.raises(ValueError):
        calculate(['2', '3', '4', '+'])


def test_calculate_unary_minus_in_postfix():
    # Проверка вычисления выражения с унарным минусом.
    result = calculate(['-5', '3', '+'])
    assert "Операция выполнена успешно." in result


# Здесь я проверяю работу калькулятора от и до: токенизация, перевод в ОПН, подсчет результата

def test_full_pipeline(valid_expressions):
    # Проверяем, что все функции вместе работают правильно.
    for expr in valid_expressions.values():
        tokens = tokenize_char(expr)
        postfix = shunting_yard(tokens)
        result = calculate(postfix)
        assert "Операция выполнена успешно." in result


def test_full_pipeline_invalid(invalid_expressions):
    # Если выражение плохое — на любом этапе должна быть ошибка.
    for expr in invalid_expressions.values():
        with pytest.raises(Exception):
            tokens = tokenize_char(expr)
            postfix = shunting_yard(tokens)
            calculate(postfix)


