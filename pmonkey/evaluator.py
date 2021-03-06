import pmonkey.objects as obj
import pmonkey.ast as ast
from pmonkey.environment import Environment
from pmonkey.objects import Integer
from pmonkey.objects import Boolean
from pmonkey.objects import Null
from pmonkey.objects import ReturnValue
from pmonkey.objects import Error
from pmonkey.objects import Function

TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()


def eval(node, env):
    node_type = type(node)
    if node_type == ast.Program:
        return eval_program(node.statements, env)
    elif node_type == ast.ExpressionStatement:
        return eval(node.expression, env)
    elif node_type == ast.IntegerLiteral:
        int_obj = Integer(node.value)
        return int_obj
    elif node_type == ast.BooleanLiteral:
        bool_obj = native_boolean_to_boolean_object(node.value)
        return bool_obj
    elif node_type == ast.PrefixExpression:
        right = eval(node.right, env)
        if is_error(right):
            return right
        return eval_prefix_expression(node.operator, right)
    elif node_type == ast.InfixExpression:
        left = eval(node.left, env)
        if is_error(left):
            return left

        right = eval(node.right, env)
        if is_error(right):
            return right

        return eval_infix_expression(node.operator, left, right)
    elif node_type == ast.BlockStatement:
        return eval_block_statement(node.statements, env)
    elif node_type == ast.IfExpression:
        return eval_if_expression(node, env)
    elif node_type == ast.ReturnStatement:
        val = eval(node.return_value, env)
        if is_error(val):
            return val
        return ReturnValue(val)
    elif node_type == ast.LetStatement:
        val = eval(node.value, env)
        if is_error(val):
            return val
        env.set(node.name.value, val)
        return
    elif node_type == ast.Identifier:
        return eval_identifier(node, env)
    elif node_type == ast.FunctionLiteral:
        params = node.parameters
        body = node.body
        return Function(params, body, env)
    elif node_type == ast.CallExpression:
        function = eval(node.function, env)
        if is_error(function):
            return function
        args = eval_expressions(node.arguments, env)
        if len(args) == 1 and is_error(args[0]):
            return args

        return apply_function(function, args)
    else:
        return NULL


def eval_program(statements, env):
    for statement in statements:
        result = eval(statement, env)
        if result != None:
            if result.type() == obj.RETURN_VALUE_OBJ:
                return result.value
            elif result.type() == obj.ERROR_OBJ:
                return result

    return result


def eval_block_statement(statements, env):
    for statement in statements:
        result = eval(statement, env)

        if result.type() == obj.RETURN_VALUE_OBJ or result.type() == obj.ERROR_OBJ:
            return result

    return result


def eval_prefix_expression(op, right):
    if op == "!":
        return eval_bang_operator_expression(right)
    elif op == "-":
        return eval_minus_prefix_operator_expression(right)
    else:
        return Error(f"unknown operator: {op}{right.type()}")


def eval_infix_expression(op, left, right):
    if type(left) == Integer and type(right) == Integer:
        return eval_integer_infix_expression(op, left, right)
    elif op == "==":
        return native_boolean_to_boolean_object(left == right)
    elif op == "!=":
        return native_boolean_to_boolean_object(left != right)
    elif left.type() != right.type():
        return Error(f"type mismatch: {left.type()} {op} {right.type()}")
    else:
        return Error(f"unknown operator: {left.type()} {op} {right.type()}")


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
        return Error(f"unknown operator: -{right.type()}")

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
    elif op == "<":
        return native_boolean_to_boolean_object(left.value < right.value)
    elif op == ">":
        return native_boolean_to_boolean_object(left.value > right.value)
    elif op == "==":
        return native_boolean_to_boolean_object(left.value == right.value)
    elif op == "!=":
        return native_boolean_to_boolean_object(left.value != right.value)
    else:
        return Error(f"unknown operator: {left.type()} {op} {right.type()}")


def eval_if_expression(node, env):
    condition = eval(node.condition, env)
    if is_error(condition):
        return condition

    if is_truthy(condition):
        return eval(node.consequence, env)
    elif node.alternative:
        return eval(node.alternative, env)
    else:
        return NULL


def eval_identifier(node, env):
    val = env.get(node.value)
    if val == None:
        return Error(f"identifier not found: {node.value}")
    return val


def eval_expressions(exps, env):
    values = []
    for e in exps:
        evaluated = eval(e, env)
        if is_error(evaluated):
            return [evaluated]
        values.append(evaluated)

    return values


def is_truthy(value):
    if value == NULL:
        return False
    elif value == TRUE:
        return True
    elif value == FALSE:
        return False
    else:
        return True


def apply_function(function, args):
    env = extend_function_environment(function, args)
    evaluated = eval(function.body, env)
    if is_error(evaluated):
        return evaluated

    if evaluated.type() == obj.RETURN_VALUE_OBJ:
        return evaluated.value
    else:
        return evaluated


def extend_function_environment(function, args):
    internal_env = Environment(function.env)
    for i, param in enumerate(function.parameters):
        internal_env.set(param.value, args[i])

    return internal_env


def native_boolean_to_boolean_object(boolean_value):
    return TRUE if boolean_value else FALSE


def is_error(node):
    return node.type() == obj.ERROR_OBJ
