# Pascal Mehnert
# 07.03.2016
#
# V 0.1


def validate_axis_size(expression, entry_dialog):
    if expression.match(entry_dialog.get()):
        return True
    else:
        return False
