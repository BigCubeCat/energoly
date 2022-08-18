class BaseObject:
    def __init__(self, index, parents, name) -> None:
        self.index = index
        self.parents = parents
        self.name = name    

    def __str__(self):
        return f"name: {self.name} index: {self.index} parents: {self.parents}"
