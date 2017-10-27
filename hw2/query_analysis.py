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
        self.current_doc_id = 0

    def get_values(self, search):
        self.value = sorted(search.search_word(self.value))

    def goto(self, doc_id):
        self.value = [x for x in self.value if x >= doc_id]

    def evaluate(self):
        if self.value:
            return self.value[0]
        return self.value


class QTreeOperator(QtreeTypeInfo):
    def __init__(self, op):
        QtreeTypeInfo.__init__(self, op, op=True)
        self.priority = get_operator_prio(op)
        self.left = None
        self.right = None
        self.current_doc_id = -1

    def goto(self, doc_id):
        if self.left:
            self.left.goto(doc_id)
        self.right.goto(doc_id)
        self.current_doc_id = doc_id

    def evaluate(self):
        if self.value == "|":
            left = self.left.evaluate()
            right = self.right.evaluate()
            if not left:
                return right
            if not right:
                return left
            return min(left, right)

        if self.value == "&":
            left = self.left.evaluate()
            right = self.right.evaluate()
            while left and right and left != right:
                doc_next = max(left, right)
                self.left.goto(doc_next)
                self.right.goto(doc_next)
                left = self.left.evaluate()
                right = self.right.evaluate()
            if left and left == right:
                return left
            return list()

        if self.value == '!':
            val = self.right.evaluate()
            doc_id = self.current_doc_id
            while (doc_id == val):
                doc_id += 1
                self.right.goto(doc_id)
                val = self.right.evaluate()
            return doc_id



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





class Query:
    def __init__(self, search):
        self.search = search

    def handle_query(self, query):
        root = parse_query(query.lower())
        self.set_values(root)
        res = list()
        item = root.evaluate()
        while(item):
            res.append(item)
            root.goto(item + 1)
            item = root.evaluate()
        return res

    def set_values(self, root):
        if root.is_operator:
            if root.left:
                self.set_values(root.left)
            self.set_values(root.right)
            return
        root.get_values(self.search)

    # def handle_query(self, query):
    #     return self.execute_query(parse_query(query.lower()))

    # def execute_query(self, root, depth=0):
    #     if root.is_operator:
    #         if root.value == '&':
    #             left = self.execute_query(root.left, depth + 1)
    #             right = self.execute_query(root.right, depth + 1)
    #             if root.left.value == '!':
    #                 return right - left
    #             if root.right.value == '!':
    #                 return left - right
    #             return left & right
    #         if root.value == '|':
    #             left = self.execute_query(root.left, depth + 1)
    #             right = self.execute_query(root.right, depth + 1)
    #             return left | right
    #         return self.execute_query(root.right, depth + 1)
    #     else:
    #         return self.search.search_word(root.value)
