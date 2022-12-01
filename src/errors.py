from utils import *

class Error:
    def __init__(self, position_start, position_end, name, details) -> None:
        self.position_start = position_start
        self.position_end = position_end
        self.name = name
        self.details = details

    def as_string(self):
        result_error = f"{self.name}: {self.details}"
        result_error += f" File: {self.position_start.file_name}, Line: {self.position_start.line_number + 1}"
        result_error += '\n\n' + string_with_arrows(self.position_start.file_text, self.position_start, self.position_end )
        return result_error


class IllegaCharError(Error):
    def __init__(self, position_start, position_end, details) -> None:
        super().__init__(position_start, position_end, "IllegaCharError", details)

class InvalidSyntaxError(Error):
    def __init__(self, position_start, position_end, details) -> None:
        super().__init__(position_start, position_end, "InvalidSyntaxError", details)

class NumberOperationError(Error):
    def __init__(self, position_start, position_end, details, context) -> None:
        super().__init__(position_start, position_end, "NumberOperationError", details)
        self.context = context
    
    def as_string(self):
        result_error = self.generate_traceback()
        result_error += f"{self.name}: {self.details}"
        result_error += '\n\n' + string_with_arrows(self.position_start.file_text, self.position_start, self.position_end )
        return result_error

    def generate_traceback(self):
        result = ""
        position = self.position_start
        context = self.context
        
        while context:
            result = f"File {position.file_name}, Line {str(position.line_number+1)}, in {context.display_name}\n" + result
            position = context.parent_entry_position
            context = context.parent
        
        return 'Stacktrace: \n' + result

