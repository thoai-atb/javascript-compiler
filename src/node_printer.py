from lib.pptree import *

class NodePrinter:
    def __init__ (self, node):
        self.print_node = Node(self.get_name(node))
        self.construct(node, self.print_node)

    def get_name(self, node):
        return type(node).__name__

    def construct(self, node, print_node):
        method_name = f'construct_{type(node).__name__}'
        method = getattr(self, method_name, self.no_construct_method)
        method(node, print_node)
    
    def construct_BinOpNode(self, node, print_node):
        left = Node(self.get_name(node.left_node), print_node)
        op = Node(node.token.type, print_node)
        right = Node(self.get_name(node.right_node), print_node)
        self.construct(node.left_node, left)
        self.construct(node.right_node, right)

    def construct_NumberNode(self, node, print_node):
        Node(str(node.token.value), print_node)

    def construct_VarAccessNode(self, node, print_node):
        Node(str(node.token), print_node)

    def construct_VarAssignNode(self, node, print_node):
        Node(str(node.var_name_token), print_node)
        expr = Node(self.get_name(node.expr_node), print_node)
        self.construct(node.expr_node, expr)
    
    def construct_VarDeclarationNode(self, node, print_node):
        Node(str(node.var_name_token), print_node)
        expr = Node(self.get_name(node.expr_node), print_node)
        self.construct(node.expr_node, expr)

    def construct_UnaryOpNode(self, node, print_node):
        Node(str(node.token), print_node)
        p_node = Node(self.get_name(node.node), print_node)
        self.construct(node.node, p_node)
    
    def construct_StatementListNode(self, node, print_node):
        for n in node.list:
            p_node = Node(self.get_name(n), print_node)
            self.construct(n, p_node)

    def no_construct_method(self, node, print_node):
        raise Exception(f'No construct_{type(node).__name__} method defined')

    def print(self):
        print_tree(self.print_node, horizontal=True)