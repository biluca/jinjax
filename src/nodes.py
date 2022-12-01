class NumberNode:
    def __init__(self, nominal):
        self.nominal = nominal
        self.position_start = nominal.position_start
        self.position_end = nominal.position_end
    
    def __repr__(self) -> str:
        return f"{self.nominal}"

class BinaryOperationNode:
    def __init__(self, left_node, operator_nominal, right_node ) -> None:
        self.left_node = left_node
        self.operator_nominal = operator_nominal
        self.right_node = right_node
        self.position_start = left_node.position_start
        self.position_end = right_node.position_end
        
    
    def __repr__(self) -> str:
        return f"({self.left_node}, {self.operator_nominal}, {self.right_node})"

class UnaryOperationNode:
    def __init__(self, operator_nominal, node) -> None:
        self.operator_nominal = operator_nominal
        self.node = node
        self.position_start = operator_nominal.position_start
        self.position_end = node.position_end
    
    def __repr__(self) -> str:
        return f"({self.operator_nominal}, {self.node})"