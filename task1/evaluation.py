from .nodes import Node


class Evaluator:
    def evaluate(self, node):
        assert isinstance(node, Node)
        node_type = type(node).__name__
        method = getattr(self, "eval_" + node_type, None)
        assert method is not None, "Invalid node type"
        return method(node)

    def eval_GtOperator(self, node):
        return node.left > node.right

    def eval_LtOperator(self, node):
        return node.left < node.right

    def eval_EqOperator(self, node):
        return node.left == node.right

    def eval_NeOperator(self, node):
        return node.left != node.right

    def eval_AndOperator(self, node):
        return self.evaluate(node.left) and self.evaluate(node.right)

    def eval_OrOperator(self, node):
        return self.evaluate(node.left) or self.evaluate(node.right)
