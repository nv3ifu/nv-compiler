class Environment:
    def __init__(self,parent=None):
        self.parent = parent
        self.var = {}
        self.funcs = {}

    def get_var(self,name):
        while self:
            value = self.var.get(name)
            if value is not None:
                return value
            self = self.parent
        return None
    def set_var(self,name,value):
        original_env = self
        while self:
            if self.var.get(name) is not None:
                self.var[name] = value
                return value
            self = self.parent
        original_env.var[name] = value

    def new_env(self):
        return Environment(parent=self)

    def get_func(self,name):
        while self:
            value = self.funcs.get(name)
            if value is not None:
                return value
            self = self.parent
        return None
    def set_func(self,name,value):
        self.funcs[name] = value

    def set_local(self,name,value):
        self.var[name] = value


