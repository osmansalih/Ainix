def calculate_expression(expression):
    try:
        result = eval(expression)
        return f"الناتج هو {result}."
    except Exception as e:
        return f"خطأ في الحسابات: {e}"
