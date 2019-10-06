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
    elif node_type == ast.PrefixExpression:
        right = eval(node.right)
        return eval_prefix_expression(node.operator, right)
    elif node_type == ast.InfixExpression:
        left = eval(node.left)
        right = eval(node.right)
        return eval_infix_expression(node.operator, left, right)
    else:
        return NULL


def eval_statements(statements):
    for statement in statements:
        result = eval(statement)

    return result


def eval_prefix_expression(op, right):
    if op == "!":
        return eval_bang_operator_expression(right)
    elif op == "-":
        return eval_minus_prefix_operator_expression(right)
    else:
        return NULL


def eval_infix_expression(op, left, right):
    if type(left) == Integer and type(right) == Integer:
        return eval_integer_infix_expression(op, left, right)
    else:
        return NULL


def eval_bang_operator_expression(right):
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE


def eval_minus_prefix_operator_expression(right):
    if type(right) != Integer:
        return NULL

    value = right.value
    return Integer(-value)


def eval_integer_infix_expression(op, left, right):
    if op == "+":
        return Integer(left.value + right.value)
    elif op == "-":
        return Integer(left.value - right.value)
    elif op == "*":
        return Integer(left.value * right.value)
    elif op == "/":
        return Integer(left.value / right.value)
    else:
        return NULL
