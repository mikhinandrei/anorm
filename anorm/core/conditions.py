class QueryConditions:
    def __init__(self, conditions: dict = {}) -> None:
        self.conditions = conditions

    def to_sql_where(self) -> str:
        if not self.conditions:
            return ""

        condition_pairs = []
        for column, value in self.conditions.items():
            condition_pairs.append(f"{column} = {value}")

        return "WHERE {}".format(", ".join(condition_pairs))
