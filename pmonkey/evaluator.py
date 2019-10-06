from pmonkey.objects import Integer
from pmonkey.objects import Boolean
from pmonkey.objects import Null
import pmonkey.ast as ast

TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()

def eval(node):
    node_type = type(node)
    if node_type == ast.Program:
        return eval_statements(node.statements)
    elif node_type == ast.ExpressionStatement:
        return eval(node.expression)
    elif node_type == ast.IntegerLiteral:
        int_obj = Integer(node.value)
        return int_obj
    elif node_type == ast.BooleanLiteral:
        bool_obj = TRUE if node.value else FALSE
        return bool_obj
    else:
        return None


def eval_statements(statements):
    for statement in statements:
        result = eval(statement)

    return result
