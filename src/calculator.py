def tokenize_char(expression: str) -> list:
    expr = expression + " "
    valid_chars = set("0123456789+-*/.():^% ")
    operators = set("+-*/:^%")

    # Проверяем, что инфиксное выражние не является пустым
    if not expr.replace(" ", ""):
        raise ValueError("Инфиксное выражение не должно быть пустым.")

    # Проверка на наличие недопустимых символов
    for char in expr:
        if char not in valid_chars:
            raise ValueError(f"В инфиксном выражении присутствует недопустимый символ: '{char}'.")

    # Проверка на количество открывающих и закрывающих скобок
    bracket = 0
    for char in expr:
        if char == "(":
            bracket += 1
        elif char == ")":
            bracket -= 1
    if bracket != 0:
        raise ValueError(f"В инфиксном выражении скобки не сбалансированы.")

    # Токенизация с дополнительными проверками
    i, tokens, char, last_type = 0, [], "", None
    while i < len(expr):
        # Если символ является строкой
        if expr[i].isdigit():
            # Выводим ошибку, если пользователь ввёл два числа подряд, но между ними нет знака операции
            if last_type == "number":
                raise ValueError("В инфиксном выражении стоят два или более чисел подряд.")
            # Если все нормально, собираем посимвольно число
            else:
                last_type = "number"
                char += expr[i]
                i += 1
                while i < len(expr):
                    if expr[i].isdigit():
                        char += expr[i]
                        i += 1
                    # Если встречается точка, то собираем вещественное число
                    elif expr[i] == '.':
                        # Если в вещественном числе есть точка, но на подходе уже вторая, то выводим ошибку
                        if char.count('.'):
                            raise ValueError("В инфиксном выражении у вещественного"
                                             " числа должна быть только одна точка.")
                        else:
                            char += expr[i]
                            i += 1
                    # Собрали число - добавляем в стек
                    else:
                        tokens.append(char)
                        char = ""
                        break
        # Если точка стоит перед числом, выводим ошибку
        elif expr[i] == '.' and last_type != 'number':
            raise ValueError("Недопустимый формат вещественного числа в инфиксном выражении.")

        # В конце выражения специально стоит пробел. Здесь цикл while заканчивает свою работу
        elif expr[i].isspace() or expr[i] == '\t':
            i += 1

        elif expr[i] in operators:
            # Случай с унарным минусом
            if expr[i] == "-" and expr[i + 1].isdigit():
                # Если минус стоит между двумя числами, то мы его засчитываем как бинарный
                if expr[i - 1].isdigit():
                    tokens.append(expr[i])
                    last_type = "operator"
                    i += 1
                    continue
                char += expr[i]
                i += 1
            # Случай с бинарным минусом
            elif expr[i] == '-' and (expr[i + 1].isspace() or expr[i + 1] == '-'):
                tokens.append(expr[i])
                last_type = "operator"
                i += 1
            # Два бинарных знака операций приведут к ошибке -> 3 + * 2 = ошибка
            elif last_type == "operator":
                raise ValueError("В инфиксном выражении стоят два или более знаков операций подряд.")
            # Если знак операции без дела стоит в начале выражения, выводим ошибку
            elif not last_type:
                raise ValueError("В инфиксном выражении знак операции не должен стоять в начале.")
            # Все кроме минуса сразу добавляем в стек
            else:
                tokens.append(expr[i])
                last_type = "operator"
                i += 1

        # Если встречаем открывающую скобку
        elif expr[i] == "(":
            # Ошибка с открывающей скобкой
            if last_type == "number":
                raise ValueError("В инфиксном выражении перед открывающей скобкой"
                                 " не может быть числа без знака операции.")
            last_type = "open"
            tokens.append(expr[i])
            i += 1

        # Если встречаем закрывающую скобку
        elif expr[i] == ")":
            # Ошибка с закрывающей скобкой
            if last_type in "open operator":
                raise ValueError("В инфиксном выражении перед закрывающей скобкой"
                                 " не может быть открывающей скобки или знака операции.")
            tokens.append(expr[i])
            last_type = "close"
            i += 1

    # Ошибка с лишним знаком операции в конце
    if last_type == "operator":
        raise ValueError("Инфиксное выражение не должно заканчиваться знаком операции.")

    return tokens


def shunting_yard(expression: list) -> list:
    # Приоритеты операций
    p = {'+': 1, '-': 1, '*': 2, '/': 2, ':': 2, '%': 2, '^': 3}

    # Выходной стек
    output = []
    # Стек для хранения знаков операций, из него мы при необходимости их достаем
    stack = []

    for token in expression:
        # Числа закидываем в выходной стек сразу
        if token.replace(".", "").isdigit() or token[1:].replace(".", "").isdigit():
            output.append(token)
        # Eсли текущий токен — это оператор, то ->
        elif token in p:
            # Пока в стеке есть операторы с большим или равным приоритетом
            # (а '^' обрабатывается отдельно — она правоассоциативная)
            while (stack and stack[-1] in p and ((p[stack[-1]] > p[token]) or
                                                 (p[stack[-1]] == p[token] and token != '^'))):

                # -> выталкиваем оператор из стека в выходной стек
                output.append(stack.pop())
            # После того как убрали из стека все более приоритетные операторы, добавляем текущий в стек
            stack.append(token)
        # Когда видим открывашку, запоминаем, что нужно отложить выполнение операций внутри неё
        elif token == '(':
            stack.append(token)
        # Когда видим закрывашку, достаем операторы из стека до ближайшей открывашки и отправляем в выходной стек
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            # Если так и не нашли открывашку, выводим ошибку
            if not stack:
                raise ValueError(f"В инфиксном выражении скобки не сбалансированы.")
            stack.pop()

    # Проверка стека на наличие незакрытых открывашек
    while stack:
        if stack[-1] == '(':
            raise ValueError(f"В инфиксном выражении скобки не сбалансированы.")
        output.append(stack.pop())

    return output


def calculate(expression: list) -> str:
    # Стек для чисел и промежуточных результатов
    stack = []
    # С помощью лямбда-функций определяем, что делает каждый оператор
    operators = {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y, '/': lambda x, y: x / y,
                 '%': lambda x, y: x % y, '^': lambda x, y: x ** y, ':': lambda x, y: x // y}

    for token in expression:
        # Числа сразу кладем в стек
        if token.replace(".", "").isdigit() or token[1:].replace(".", "").isdigit():
            stack.append(float(token))
        # Если текущий токен - оператор, достаем два последних числа из стека
        else:
            # Проверяем, что в стеке есть как минимум два числа
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для выполнения операции.")
            try:
                b = stack.pop()
                a = stack.pop()
                # Для деления нацело и вычисления остатка от деления нужно использовать только целые числа, иначе ошибка
                if token == ':' and (int(a) != a or int(b) != b):
                    raise ValueError("Для выполнения операции '//' необходимы только целые числа.")
                if token == '%' and (int(a) != a or int(b) != b):
                    raise ValueError("Для выполнения операции '%' необходимы только целые числа.")
                # Делаем промежуточные расчеты и результат кладем обратно в стек
                if token in operators:
                    stack.append(operators[token](a, b))
            # Предотвращаем деление на ноль
            except ZeroDivisionError:
                raise ZeroDivisionError("Ошибка деления на ноль.")

    # Проверяем, что после вычислений остался ровно один результат
    if len(stack) != 1:
        raise ValueError("Ошибка в выражении: остались лишние операнды или операций не хватает.")

    # Возвращаем результат
    return 'Операция выполнена успешно.' + '\n' + str(stack[0])


if __name__ == "__main__":
    print(calculate(shunting_yard(tokenize_char(input("Введите выражение: ")))))
