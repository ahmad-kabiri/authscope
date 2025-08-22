
import ast

ALLOWED_NODES = {
    ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp,
    ast.Compare, ast.Name, ast.Load, ast.Constant, ast.List, ast.Tuple,
    ast.Dict, ast.And, ast.Or, ast.Eq, ast.NotEq, ast.In, ast.NotIn,
    ast.Attribute, ast.Subscript, ast.Index
}

def _get_attr(obj, attr):
    return getattr(obj, attr) if hasattr(obj, attr) else obj.get(attr)

def _eval(node, names):
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Disallowed expression node: {type(node).__name__}")
    if isinstance(node, ast.Expression):
        return _eval(node.body, names)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return names[node.id]
    if isinstance(node, ast.Attribute):
        base = _eval(node.value, names)
        return _get_attr(base, node.attr)
    if isinstance(node, ast.Subscript):
        base = _eval(node.value, names)
        if isinstance(node.slice, ast.Slice):
            raise ValueError("Slices not allowed")
        key = _eval(node.slice, names)
        return base[key]
    if isinstance(node, ast.List):
        return [_eval(elt, names) for elt in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(_eval(elt, names) for elt in node.elts)
    if isinstance(node, ast.Dict):
        return { _eval(k, names): _eval(v, names) for k,v in zip(node.keys, node.values) }
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.Not):
            return not _eval(node.operand, names)
        raise ValueError("Only 'not' unary op is supported")
    if isinstance(node, ast.BoolOp):
        vals = [_eval(v, names) for v in node.values]
        if isinstance(node.op, ast.And):
            res = True
            for v in vals:
                res = res and v
            return res
        if isinstance(node.op, ast.Or):
            res = False
            for v in vals:
                res = res or v
            return res
        raise ValueError("Unsupported BoolOp")
    if isinstance(node, ast.Compare):
        left = _eval(node.left, names)
        result = True
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval(comparator, names)
            if isinstance(op, ast.Eq):
                result = result and (left == right)
            elif isinstance(op, ast.NotEq):
                result = result and (left != right)
            elif isinstance(op, ast.In):
                result = result and (left in right)
            elif isinstance(op, ast.NotIn):
                result = result and (left not in right)
            else:
                raise ValueError("Only ==, !=, in, not in are supported")
            left = right
        return result
    raise ValueError("Unsupported expression")

def safe_eval(expr: str, names: dict):
    tree = ast.parse(expr, mode="eval")
    return _eval(tree, names)
