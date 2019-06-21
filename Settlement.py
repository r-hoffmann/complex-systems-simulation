class Settlement(object):
    def __init__(self, model, demand=None, x=None, y=None):
        self.model = model
        self.id = len(self.model.settlements)
        if demand==None:
            raise Exception('Settlement has no demand')
        self.demand = demand
        if x == None and y == None:
            self.x, self.y = self.get_place()
        else:
            self.x = x
            self.y = y
    
    @property
    def cell(self):
        return self.model.terrain.get_cell(self.x, self.y)
    
    def get_place(self, placement_type='center'):
        if placement_type == 'center':
            x, y =int(self.model.terrain.width / 2), int(self.model.terrain.height / 2)
        elif placement_type == 'deepest_point':
            raise NotImplementedError
        elif placement_type == 'default':
            # Something smart
            raise NotImplementedError
        return x, y