class Settlement(object):
    def __init__(self, model, demand=None, x=None, y=None, line_number=None):
        assert demand!=None, Exception('Settlement has no demand')
        assert line_number!=None, Exception('Settlement has no line number')
        self.model = model
        self.id = len(self.model.settlements)
        self.demand = demand
        self.line_number = line_number
        if x == None and y == None:
            self.get_positions()
        else:
            self.x = x
            self.y = y
    
    @property
    def cell(self):
        return self.model.terrain.get_cell(self.x, self.y)
    
    def get_positions(self):
        # Get all cells in bin
        positions = self.model.terrain.terrain[self.line_number]

        # Get positions of first water cell from both the left and right side in each row
        positions_with_height = [[cell.x, cell.y, cell.height_of_water] for cell in positions]
        positions_with_height.sort(key=lambda x: x[2])
        self.x, self.y, _ = positions_with_height[0]

    def __repr__(self):
        return str("({}, {}) {}".format(self.x, self.y, self.demand))
