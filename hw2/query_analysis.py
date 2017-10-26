import re

SPLIT_RGX = re.compile(r'\w+|[\(\)&\|!]', re.U)

class QtreeTypeInfo:
    def __init__(self, value, op=False, bracket=False, term=False):
        self.value = value
        self.is_operator = op
        self.is_bracket = bracket
        self.is_term = term

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        if isinstance(other, QtreeTypeInfo):
            return self.value == other.value
        return self.value == other


class QTreeTerm(QtreeTypeInfo):
    def __init__(self, term):
        QtreeTypeInfo.__init__(self, term, term=True)


class QTreeOperator(QtreeTypeInfo):
    def __init__(self, op):
        QtreeTypeInfo.__init__(self, op, op=True)
        self.priority = get_operator_prio(op)
        self.left = None
        self.right = None


class QTreeBracket(QtreeTypeInfo):
    def __init__(self, bracket):
        QtreeTypeInfo.__init__(self, bracket, bracket=True)


def get_operator_prio(s):
    if s == '|':
        return 0
    if s == '&':
        return 1
    if s == '!':
        return 2
    return None


def is_operator(s):
    return get_operator_prio(s) is not None


def tokenize_query(q):
    tokens = []
    for t in map(lambda w: w.encode('utf-8'), re.findall(SPLIT_RGX, q)):
        if t == '(' or t == ')':
            tokens.append(QTreeBracket(t))
        elif is_operator(t):
            tokens.append(QTreeOperator(t))
        else:
            tokens.append(QTreeTerm(t))
    return tokens


def build_query_tree(tokens):
    stack = list()
    prios = list()
    for token in tokens:
        if not is_operator(token):
            if (token == '('):
                stack.append(token)
                prios.append(-1)
            elif (token == ')'):
                while(True):
                    a = stack.pop()
                    op1 = stack.pop()
                    prios.pop()
                    if (op1 == '('):
                        stack.append(a)
                        break
                    if get_operator_prio(op1) != 2:
                        b = stack.pop()
                        op1.left = b
                    op1.right = a
                    stack.append(op1)
            else:
                stack.append(token)
        elif not prios or get_operator_prio(token) > prios[-1]:
            stack.append(token)
            prios.append(get_operator_prio(token))
        else:
            a = stack.pop()
            op1 = stack.pop()
            if get_operator_prio(op1) != 2:
                b = stack.pop()
                op1.left = b
            op1.right = a
            prios.pop()
            stack.append(op1)
            stack.append(token)
            prios.append(get_operator_prio(token))
    while len(stack) > 1:
        a = stack.pop()
        op1 = stack.pop()
        if get_operator_prio(op1) != 2:
            b = stack.pop()
            op1.left = b
        op1.right = a
        stack.append(op1)
    return stack[0]

def parse_query(q):
    tokens = tokenize_query(q)
    return build_query_tree(tokens)

def qtree2str(root, depth=0):
    if root.is_operator:
        need_brackets = depth > 0 and root.value != '!'
        res = ''
        if need_brackets:
            res += '('
        if root.left:
            res += qtree2str(root.left, depth+1)
        if root.value == '!':
            res += root.value
        else:
            res += ' ' + root.value + ' '
        if root.right:
            res += qtree2str(root.right, depth+1)
        if need_brackets:
            res += ')'
        return res
    else:
        return root.value

class Query:
    def __init__(self, search):
        self.search = search

    def handle_query(self, query):
        return self.execute_query(parse_query(query.lower()))

    def execute_query(self, root, depth=0):
        if root.is_operator:
            if root.value == '&':
                left = self.execute_query(root.left, depth + 1)
                right = self.execute_query(root.right, depth + 1)
                if root.left.value == '!':
                    return right - left
                if root.right.value == '!':
                    return left - right
                return left & right
            if root.value == '|':
                left = self.execute_query(root.left, depth + 1)
                right = self.execute_query(root.right, depth + 1)
                return left | right
            return self.execute_query(root.right, depth + 1)
        else:
            return self.search.search_word(root.value)
