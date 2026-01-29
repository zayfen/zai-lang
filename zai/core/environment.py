class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.context = {}
        self.parent = parent

    def get_var(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_var(name)
        raise NameError(f"Variable '{name}' not found")

    def set_var(self, name, value):
        self.variables[name] = value

    def get_context(self, name):
        if name in self.context:
            return self.context[name]
        if self.parent:
            return self.parent.get_context(name)
        return None

    def set_context(self, name, value):
        self.context[name] = value
