import dis
import inspect


class VM:
    def __init__(self):
        self.stack = []
        self.names = {}

    def fit(self, code, globals=None, locals=None):
        if code == '':
            raise Exception('Code contains empty string')
        converted = self._compile(code)
        self._process(converted.co_code)

    def _compile(self, code):
        try:
            result = compile(code, "fun", "exec", 0, 1)
            return result
        except:
            raise Exception("Found errors in code compile")

    def _process(self, items):
        for item in items:
            result = self._parse(item)
            if result != '<0>':
                print(result)

    def _parse(self, code):
        ''' After compiled, parse result'''
        return dis.opname[code]

    def _process_opcode(self, opcode, item):
        if opcode == 'LOAD_CONST':
            self.stack.extend(item)
        if opcode == 'STORE_NAME':
            self.names[item] = self.stack.pop()
        if opcode == 'LOAD_ATTR':
            value = self.stack.pop()
        if opcode == 'STORE_ATTR':
            value = self.stack.pop()
            setattr(value, item)
