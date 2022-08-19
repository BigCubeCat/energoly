class BaseObject:
    def __init__(self, index, parent, name) -> None:
        self.index = index
        self.parent = parent
        self.name = name    

    def __str__(self):
        return f"name: {self.name} index: {self.index} parent: {self.parent}"
