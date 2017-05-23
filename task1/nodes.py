class Node:
    pass


class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class BooleanNode(BinaryNode):
    pass


class ComparisonOperator(BooleanNode):
    def __init__(self, left, right):
        assert isinstance(left, (int, float)), left
        assert isinstance(right, (int, float)), right
        super().__init__(left, right)


class GtOperator(ComparisonOperator):
    pass


class LtOperator(ComparisonOperator):
    pass


class EqOperator(ComparisonOperator):
    pass


class NeOperator(ComparisonOperator):
    pass


class LogicalOperator(BooleanNode):
    def __init__(self, left, right):
        assert isinstance(left, BooleanNode), left
        assert isinstance(right, BooleanNode), right
        super().__init__(left, right)


class AndOperator(LogicalOperator):
    pass


class OrOperator(LogicalOperator):
    pass
