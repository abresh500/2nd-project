
import ast
import operator as op
import argparse
import math

# supported operators
_OPERATORS = {
	ast.Add: op.add,
	ast.Sub: op.sub,
	ast.Mult: op.mul,
	ast.Div: op.truediv,
	ast.Mod: op.mod,
	ast.Pow: op.pow,
	ast.FloorDiv: op.floordiv,
	ast.UAdd: op.pos,
	ast.USub: op.neg,
}


def _eval(node):
	if isinstance(node, ast.Expression):
		return _eval(node.body)
	if isinstance(node, ast.Constant):
		if isinstance(node.value, (int, float)):
			return node.value
		raise ValueError("Only numeric constants are allowed")
	if isinstance(node, ast.Num):
		return node.n
	if isinstance(node, ast.BinOp):
		left = _eval(node.left)
		right = _eval(node.right)
		op_type = type(node.op)
		if op_type in _OPERATORS:
			return _OPERATORS[op_type](left, right)
	if isinstance(node, ast.UnaryOp):
		operand = _eval(node.operand)
		op_type = type(node.op)
		if op_type in _OPERATORS:
			return _OPERATORS[op_type](operand)
	raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def safe_eval(expr: str):
	parsed = ast.parse(expr, mode="eval")
	for node in ast.walk(parsed):
		if isinstance(node, ast.Call):
			raise ValueError("Function calls are not allowed")
		if isinstance(node, ast.Name):
			raise ValueError("Names are not allowed")
	return _eval(parsed)


def repl():
	print("Simple calculator. Type 'quit' or 'exit' to leave. Type 'help' for help.")
	while True:
		try:
			s = input("calc> ").strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if not s:
			continue
		if s.lower() in ("quit", "exit", "q"):
			break
		if s.lower() == "help":
			print("Enter arithmetic expressions using + - * / // % ** and parentheses.")
			continue
		try:
			result = safe_eval(s)
			if isinstance(result, float) and (math.isclose(result, int(result))):
				result = int(result)
			print(result)
		except Exception as e:
			print("Error:", e)


def run_tests():
	tests = [
		("1+2", 3),
		("2*3+4", 10),
		("2*(3+4)", 14),
		("10/4", 2.5),
		("2**3", 8),
		("-5+3", -2),
		("7//2", 3),
		("7%4", 3),
	]
	failed = 0
	for expr, expected in tests:
		try:
			out = safe_eval(expr)
		except Exception as e:
			print(f"FAIL: {expr} raised {e}")
			failed += 1
			continue
		if isinstance(expected, float):
			ok = math.isclose(out, expected)
		else:
			ok = out == expected
		if ok:
			print(f"OK: {expr} = {out}")
		else:
			print(f"FAIL: {expr} -> {out} (expected {expected})")
			failed += 1
	if failed:
		print(f"{failed} test(s) failed")
	else:
		print("All tests passed")


def main():
	parser = argparse.ArgumentParser(description="Simple safe calculator")
	parser.add_argument("-t", "--test", action="store_true", help="run built-in tests")
	args = parser.parse_args()
	if args.test:
		run_tests()
	else:
		repl()


if __name__ == "__main__":
	main()

