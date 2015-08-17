import dis
import inspect
import logging


class VM:
    def __init__(self):
        self.stack = []
        self.names = {}

    def fit(self, code, globals=None, locals=None):
        if code == '':
            raise Exception('Code contains empty string')
        converted = self._compile(code)
        self._process(converted)

    def _compile(self, code):
        try:
            result = compile(code, "fun", "exec", 0, 1)
            return result
        except:
            raise Exception("Found errors in code compile")

    def _process(self, items):
        names = items.co_names
        varnames = items.co_varnames
        consts = items.co_consts
        code = items.co_code
        idx = 0
        while True:
            code_item = code[idx]
            item = self._parse(code_item)
            if item == '<0>':
                continue
            value = ''
            if item == 'RETURN_VALUE':
                break
            if code_item in dis.hasname:
                value = names[idx]
            if code_item in dis.hasconst:
                value = consts[idx]
            idx += 1
            self._process_opcode(item, value)

    def _parse(self, code):
        ''' After compiled, parse result'''
        return dis.opname[code]

    def _get(n):
        if n > len(self.stack):
            logging.info("Value is greater than size of stack")

    def _process_opcode(self, opcode, item):
        print(opcode, item)
        if opcode == 'LOAD_CONST':
            self.stack.append(item)
        if opcode == 'STORE_NAME':
            self.names[item] = self.stack.pop()
        if opcode == 'LOAD_ATTR':
            value = self.stack.pop()
        if opcode == 'LOAD_NAME':
            name = self.names[item]
            self.stack.append(name)
        if opcode == 'STORE_ATTR':
            value = self.stack.get(2)
            setattr(value, item)
        if opcode == 'POP_TOP':
            self.stack.pop()
        if opcode == 'ROT_TWO':
            value1 = self.stack.pop()
            value2 = self.stack.pop()
            self.stack.append(value1)
            self.stack.append(value2)
        if opcode.startswith('BINARY'):
            x = self.stack.pop()
            y = self.stack.pop()
            self.stack.append(self._binary_operations(opcode, x, y))
        if opcode.startsWith('UNARY'):
            x = self.stack.pop()

        if opcode == 'RETURN_VALUE':
            print(self.stack)

    def _binary_operations(op, x, y):
        if op == 'BINARY_POWER':
            return x ** y
        if op == 'BINARY_MULTIPLY':
            return x * y
        if op == 'BINARY_DIVIDE' or op == 'BINARY_TRUE_DIVIDE':
            return x/y
        if op == 'BINARY_FLOOR_DIVIDE':
            return x//y
        if op == 'BINARY_MODULO':
            return x%y
        if op == 'BINARY_ADD':
            return x + y
        if op == 'BINARY_SUBTRACT':
            return x - y
        if op == 'BINARY_SUBSCR':
            return x[y]
        if op == 'BINARY_LSHIFT':
            return x << y
        if op == 'BINARY_RSHIFT':
            return x >> y
        if op == 'BINARY_AND':
            return x & y
        if op == 'BINARY_XOR':
            return x ^ y
        if op == 'BINARY_OR':
            return x | y

    def _unary_operations(op, x):
        if op == 'UNARY_POSITIVE':
            return +x
        if op == 'UNARY_NEGATIVE':
            return -x
        if op == 'UNARY_NOT':
            return not x
        if op == 'UNARY_CONVERT':
            return repr(x)
        if op == 'UNARY_INVERT':
            return ~x
