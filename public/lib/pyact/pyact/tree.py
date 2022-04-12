class Tree:
    current = None

    def __init__(self, data=None, parent=None):
        Tree.current = self
        self.data = data
        self.parent = parent
        self.branches = []

    def branch_out(self, data=None):
        branch = Tree(data, self)
        self.branches.append(branch)
        return branch

    def branch_in(self):
        Tree.current = self.parent
        return self.parent
