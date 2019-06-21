import json
from Terrain import Terrain
import numpy as np

class Model(object):
    def __init__(self, experiment=None):
        """
            dict parameters should contain the following keys:
                height (int)
                width (int)
                slope (float)
                gamma (float)
                rho (float)
                mu (float)
                cells (list of lists of dict containing the keys:
                    height_of_terrain
                    height_of_water
                    concentration_of_nutrients
                    peat_bog_thickness)
        """
        if experiment!=None:
            self.input_file = 'configuration_{}.json'.format(experiment)
            self.output_file = 'output_{}.json'.format(experiment)
        else:
            self.input_file = 'configuration.json'
            self.output_file = 'output.json'

        self.load_configuration()
        self.gamma = self.parameters['gamma']
        self.rho = self.parameters['rho']
        self.mu = self.parameters['mu']
        self.water_per_timestep = self.parameters['water_per_timestep']
        self.timesteps = self.parameters['timesteps']
        self.terrain = Terrain(self.parameters)
        self.max_depth = 0

    def load_configuration(self):
        with open(self.input_file) as file:
            self.parameters = json.load(file)

    def init_statistics(self):
        self.water_out = []
        self.water_in = []
        self.smooth_river = [[0]*self.parameters['width']]
        self.total_water = [self.get_total_water()]
        self.total_peat = [self.get_total_peat()]
        self.terrain_timeline = [self.terrain.get_summary()]

    def output_metrics(self):
        # print(self.terrain.terrain[-1][0].height_of_water)
        # self.water_cells_num = 0
        # previous_cell = 0
        # previous_cell_1 = 0
        # previous_cell_2 = 0

        # # self.num_of_outgoing_brenches = 0
        # # for cell in self.terrain.terrain[-3]:
        # #     if cell.height_of_water>0:
        # #         self.water_cells_num += 1
        # #         if (previous_cell == 0 and previous_cell_1 == 0) and previous_cell_2 ==0:
        # #             self.num_of_outgoing_brenches += 1
        # #     previous_cell_2 = previous_cell_1
        # #     previous_cell_1 = previous_cell
        # #     previous_cell = cell.height_of_water
        self.current_smooth_river = [0]*len(self.terrain.terrain[-3])
        for i in range(len(self.terrain.terrain[-3])-1):
            if i == 0 or i == len(self.terrain.terrain[-3])-1:
                continue
            self.current_smooth_river[i] = np.mean([self.terrain.terrain[-3][cell_mean].height_of_water for cell_mean in [i-1, i, i+1]])




        

        self.in_out_difference = self.current_water_in - self.current_water_out
        # print("water_cells_num", self.water_cells_num,"num_of_outgoing_brenches", self.num_of_outgoing_brenches,"in_out_difference",self.in_out_difference)


    def gather_statistics(self):
        self.water_out.append(self.current_water_out)
        self.water_in.append(self.current_water_in)
        self.total_water.append(self.get_total_water())
        self.total_peat.append(self.get_total_peat())
        self.smooth_river.append(self.current_smooth_river)
        self.terrain_timeline.append(self.terrain.get_summary())
    
    def run(self, dump_to_file=True):
        self.init_statistics()
        for t in range(self.timesteps):
            self.current_water_out = 0
            self.current_water_in = 0

            print("Timestep {}".format(t+1))
            self.timestep()
            if t % 10 == 0:
                self.gather_statistics()

        summary = self.get_summary()
        if dump_to_file:
            with open(self.output_file, 'w') as file:
                print("Output to {}".format(self.output_file))
                json.dump(summary, file)
        return summary

    def run_untill_other_side(self, timesteps=10, dump_to_file=True):
        self.init_statistics()
        t = 0
        while self.max_depth < 99:
            t += 1
            self.current_water_out = 0
            self.current_water_in = 0

            print("Timestep {}".format(t))
            self.timestep()

            self.gather_statistics()

        summary = self.get_summary()
        if dump_to_file:
            with open(self.output_file, 'w') as file:
                print("Output to {}".format(self.output_file))
                json.dump(summary, file)
        return summary

    def timestep(self):
        # Directly from paper
        self.mutations = []
        self.supply_water()
        self.remove_water()
        self.calculate_flows()
        self.update_water()
        self.output_metrics()
        self.calculate_nutrient_dist()
        self.calculate_peat_growth()

    def supply_water(self):
        self.mutations.append({
                'from': None,
                'to': self.terrain.terrain[0][int(self.terrain.width / 2)],
                'water': self.water_per_timestep
            })

    def remove_water(self):
        # @todo: Remove all water from last row?
        for cell in self.terrain.terrain[-1]:
            self.mutations.append({
                'from': cell,
                'to': None,
                'water': cell.height_of_water
            })

    def calculate_flows(self):
        # mutations is the collection of f[i] in the paper
        for cell in self.terrain.cells():
            mutations = cell.get_water_flow()
            # "commit"
            self.mutations += mutations

    def update_water(self):
        mutated = 0
        for mutation in self.mutations:
            # None cells are either inlet or outlet
            if mutation['water'] > 0:
                if mutation['from'] != None:
                    mutation['from'].height_of_water -= mutation['water']
                else:
                    self.current_water_in += mutation['water']
                if mutation['to'] != None:
                    mutation['to'].height_of_water += mutation['water']
                    if mutation['to'].y > self.max_depth:
                        self.max_depth = mutation['to'].y
                else:
                    self.current_water_out += mutation['water']
                mutated += 1
        print("Ran {} water mutations, max depth {}.".format(mutated, self.max_depth))

    def calculate_nutrient_dist(self):
        new_terrain = self.terrain.copy()
        for cell, new_cell in zip(self.terrain.cells(), new_terrain.cells()):
            if cell.height_of_water > 0:
                new_cell.concentration_of_nutrients = 1
            else:
                new_nutrients = self.gamma * max([neighbour_cell.concentration_of_nutrients for neighbour_cell in cell.neighbours()])
                if cell.concentration_of_nutrients < new_nutrients:
                    new_cell.concentration_of_nutrients = new_nutrients
                else:
                    new_cell.concentration_of_nutrients = cell.concentration_of_nutrients
        self.terrain = new_terrain

    def calculate_peat_growth(self):
        for cell in self.terrain.cells():
            if cell.height_of_water > 0:
                cell.peat_bog_thickness += self.mu * cell.height_of_water
            else:
                cell.peat_bog_thickness += self.rho * cell.concentration_of_nutrients

    def get_total_water(self):
        total_water = 0
        for cell in self.terrain.cells():
            total_water += cell.height_of_water
        return total_water

    def get_total_peat(self):
        total_peat = 0
        for cell in self.terrain.cells():
            total_peat += cell.peat_bog_thickness
        return total_peat

    def get_summary(self):
        self.gamma = self.parameters['gamma']
        self.rho = self.parameters['rho']
        self.mu = self.parameters['mu']
        print(self.total_peat)
        print(self.total_water)
        print(self.water_in)
        print(self.water_out)
        return {
            'gamma': self.gamma,
            'rho': self.rho,
            'mu': self.mu,
            'peat_timeline': self.total_peat,
            'river_timeline': self.smooth_river,
            'water_timeline': self.total_water,
            'water_in_timeline': self.water_in,
            'water_out_timeline': self.water_out,
            'terrain_timeline': self.terrain_timeline
        }
        
