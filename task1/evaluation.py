class Node:
    pass


class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class ComparisonOperator(BinaryNode):
    def __init__(self, left, right):
        assert isinstance(left, float)
        assert isinstance(right, float)
        super().__init__(left, right)


class GtOperator(ComparisonOperator):
    pass


class LtOperator(ComparisonOperator):
    pass


class EqOperator(ComparisonOperator):
    pass


class NeOperator(ComparisonOperator):
    pass


class LogicalOperator(BinaryNode):
    def __init__(self, left, right):
        assert isinstance(left, ComparisonOperator)
        assert isinstance(right, ComparisonOperator)
        super().__init__(left, right)


class AndOperator(LogicalOperator):
    pass


class OrOperator(LogicalOperator):
    pass


class Factory:
    def create(self, data):
        operator_name = data.pop("operator")
        assert operator_name is not None, "expected `operator` field"
        method = getattr(self, "create_" + operator_name, None)
        assert method is not None, "Invalid operator type"
        return method(**data)

    def create_gt(self, left, right):
        return GtOperator(left, right)

    def create_lt(self, left, right):
        return LtOperator(left, right)

    def create_eq(self, left, right):
        return EqOperator(left, right)

    def create_ne(self, left, right):
        return NeOperator(left, right)

    def create_and(self, left, right):
        left_node = self.create(left)
        right_node = self.create(right)
        return AndOperator(left_node, right_node)

    def create_or(self, left, right):
        left_node = self.create(left)
        right_node = self.create(right)
        return OrOperator(left_node, right_node)
