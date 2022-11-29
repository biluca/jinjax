

class Context:
    
    def __init__(self, display_name, parent=None, parent_entry_position=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_position= parent_entry_position
    
    def __repr__(self) -> str:
        return f"<{self.display_name}> from [{self.parent}]"