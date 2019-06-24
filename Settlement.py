class Settlement(object):
    def __init__(self, model, demand=None, x=None, y=None, bin=1):
        self.model = model
        self.id = len(self.model.settlements)
        self.bin = bin
        if demand==None:
            raise Exception('Settlement has no demand')
        self.demand = demand
        if x == None and y == None:
            self.get_positions()
        else:
            self.x = x
            self.y = y
    
    @property
    def cell(self):
        return self.model.terrain.get_cell(self.x, self.y)
    
    def get_positions(self, placement_type='center'):
        # Get all cells in bin
        positions = self.model.terrain.terrain[(self.bin-1)*10:self.bin*10]

        # Get positions of first water cell from both the left and right side in each row
        possible_positions = []

        for row in positions:
            # get position left side, and corresponding waterheight
            for i, cell in enumerate(row):
                if cell.height_of_water > 0:
                    settlement_cell = row[i-1]
                    possible_positions.append((settlement_cell, cell.height_of_water))
                    # Should stop this for loop if water is found, continue to next row
                    break
            
            # get position right side, and corresponding waterheight
            for i, cell in enumerate(row[::-1]):
                if cell.height_of_water > 0:
                    settlement_cell = row[len(row)-i]
                    possible_positions.append((settlement_cell, cell.height_of_water))
                    break           

        assert len(possible_positions)!=0,"No place for settlement"

        possible_positions.sort(key=lambda x: x[1])

        selected_cell, _ = possible_positions[0]

        self.x, self.y = selected_cell.x, selected_cell.y

    def __repr__(self):
        return str("({}, {}) {}".format(self.x, self.y, self.demand))
