class NumberNode:
    def __init__(self, token):
        self.token = token
        self.position_start = token.position_start
        self.position_end = token.position_end
    
    def __repr__(self) -> str:
        return f"{self.token}"

class BinaryOperationNode:
    def __init__(self, left_node, operator_token, right_node ) -> None:
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
        self.position_start = left_node.position_start
        self.position_end = right_node.position_end
        
    
    def __repr__(self) -> str:
        return f"({self.left_node}, {self.operator_token}, {self.right_node})"

class UnaryOperationNode:
    def __init__(self, operator_token, node) -> None:
        self.operator_token = operator_token
        self.node = node
        self.position_start = operator_token.position_start
        self.position_end = node.position_end
    
    def __repr__(self) -> str:
        return f"({self.operator_token}, {self.node})"