from errors import NumberOperationError


class ResultNumber:
    def __init__(self) -> None:
        self.value = None
        self.error = None

    def register(self, result):
        if result.error:
            self.error = result.error
        return result.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self


class Number:
    def __init__(self, value):
        self.value = value
        self.set_position()
        self.set_context()

    def __repr__(self) -> str:
        return str(self.value)

    def set_context(self, context=None):
        self.context = context
        return self

    def set_position(self, position_start=None, position_end=None):
        self.position_start = position_start
        self.position_end = position_end
        return self

    def add_to(self, other_number):
        if isinstance(other_number, Number):
            number = Number(self.value + other_number.value)
            number.set_context(self.context)
            return number, None

    def subtract_by(self, other_number):
        if isinstance(other_number, Number):
            number = Number(self.value - other_number.value)
            number.set_context(self.context)
            return number, None

    def multiply_by(self, other_number):
        if isinstance(other_number, Number):
            number = Number(self.value * other_number.value)
            number.set_context(self.context)

            return number, None

    def divide_by(self, other_number):
        if isinstance(other_number, Number):
            if self.is_zero(other_number.value):
                error_details = "Division by Zero not allowed"
                error = NumberOperationError(
                    other_number.position_start,
                    other_number.position_end,
                    error_details,
                    self.context,
                )
                return None, error
            number = Number(self.value / other_number.value)
            breakpoint()
            number.set_context(self.context)

            return number, None

    def power_by(self, other_number):
        value = self.value
        number = Number(value)

        if not isinstance(other_number.value, int):
            error_details = (
                f"Expoent should be a Integer Number, instead got {other_number.value}"
            )
            error = NumberOperationError(
                other_number.position_start,
                other_number.position_end,
                error_details,
                self.context,
            )
            return None, error

        if isinstance(other_number, Number):
            for i in range(other_number.value - 1):
                number, error = number.multiply_by(Number(value))

        number.set_context(self.context)
        return number, None

    def is_zero(self, value):
        if value == 0:
            return True
        return False
