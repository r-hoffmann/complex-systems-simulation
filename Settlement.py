class Settlement(object):
    def __init__(self, model, demand=None, x=None, y=None, bin=1):
        self.model = model
        self.id = len(self.model.settlements)
        self.bin = bin
        if demand==None:
            raise Exception('Settlement has no demand')
        self.demand = demand
        if x == None and y == None:
            print("x0y0")
            # self.x, self.y = self.get_place()
            self.get_place()
        else:
            self.x = x
            self.y = y
    
    @property
    def cell(self):
        return self.model.terrain.get_cell(self.x, self.y)
    
    def get_place(self, placement_type='center'):
        print("GET PLACE")

        # Get all cells in bin
        positions = self.model.terrain.terrain[(self.bin-1)*10:self.bin*10]

        print(positions[5][0].height_of_water)
        positions[5][0].height_of_water = 1
        print(positions[5][0].height_of_water)

        # Get positions of first water cell from both the left and right side in each row
        possible_positions = []

        for row in positions:
            print(row)
            
            # get position left side, and corresponding waterheight
            for cell in row:
                if cell.height_of_water > 0:
                    possible_positions.append((cell, cell.height_of_water))

                    # Should stop this for loop if water is found, continue to next row
                    break
                else:
                    continue
            
            # get position right side, and corresponding waterheight
            for cell in row[::-1]:
                if cell.height_of_water > 0:
                    possible_positions.append((cell, cell.height_of_water))
                    break
                else:
                    continue                

            # @todo: place_settlement() for no_of_settlements; 
            # Sort positions on left column, take top position, remove positions in the neighborhood from [possible_positions]
            # Repeat

            

        # if placement_type == 'center':
        #     self.x, self.y =int(self.model.terrain.width / 2), int(self.model.terrain.height / 2)
        # elif placement_type == 'deepest_point':
        #     raise NotImplementedError
        # elif placement_type == 'default':
        #     # Something smart
        #     raise NotImplementedError
        # return x, y