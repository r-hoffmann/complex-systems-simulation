import json
from threading import Thread
from multiprocessing import Queue, cpu_count
from Terrain import Terrain

class Model(object):
    def __init__(self, parameters=None):
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
        self.parameters = parameters
        self.gamma = self.parameters['gamma']
        self.rho = self.parameters['rho']
        self.mu = self.parameters['mu']
        self.terrain = Terrain(parameters)
        self.max_depth = 0

        self.number_of_threads = cpu_count() - 2
        print("Running on {} threads.".format(self.number_of_threads))

    def init_statistics(self):
        self.water_out = []
        self.water_in = []
        self.total_water = [self.get_total_water()]
        self.total_peat = [self.get_total_peat()]
        self.terrain_timeline = [self.terrain.get_summary()]

    def gather_statistics(self):
        self.water_out.append(self.current_water_out)
        self.water_in.append(self.current_water_in)
        self.total_water.append(self.get_total_water())
        self.total_peat.append(self.get_total_peat())
        self.terrain_timeline.append(self.terrain.get_summary())
    
    def run(self, timesteps=10, dump_to_file=True):
        self.init_statistics()
        for t in range(timesteps):
            self.current_water_out = 0
            self.current_water_in = 0

            print("Timestep {}".format(t+1))
            self.timestep()

            self.gather_statistics()

        summary = self.get_summary()
        if dump_to_file:
            with open('output.json', 'w') as file:
                print("Output to output.json")
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
            with open('output.json', 'w') as file:
                print("Output to output.json")
                json.dump(summary, file)
        return summary

    def timestep(self):
        mutations = Queue()
        worker_supply_water = Thread(target = self.supply_water, args = (mutations,))
        worker_remove_water = Thread(target = self.remove_water, args = (mutations,))
        worker_calculate_flows = self.calculate_flows(mutations)
        
        workers = [worker_supply_water, worker_remove_water] + worker_calculate_flows

        for worker in workers:
            worker.setDaemon(True)
            worker.start()

        self.mutations = []
        for worker in workers:
            worker.join()
        
        while not mutations.empty():
            self.mutations.append(mutations.get())

        self.update_water()
        self.calculate_nutrient_dist()
        self.calculate_peat_growth()

    def supply_water(self, mutations):
        # @todo: Make some kind of distribution?
        for cell in self.terrain.terrain[0]:
            mutations.put({
                'from': None,
                'to': cell,
                'water': 10
            })
        return 0

    def remove_water(self, mutations):
        # @todo: Remove all water from last row?
        for cell in self.terrain.terrain[-1]:
            mutations.put({
                'from': cell,
                'to': None,
                'water': cell.height_of_water
            })
        return 0

    def calculate_flows(self, mutations):
        # mutations is the collection of f[i] in the paper
        processes = []

        for cell in self.terrain.cells():
            process = Thread(target = self.calculate_flow, args = (cell, mutations))
            processes.append(process)

        return processes
    
    def calculate_flow(self, cell, mutations):
        for mutation in cell.get_water_flow():
            mutations.put(mutation)
        return 0

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
                cell.concentration_of_nutrients = 1
            else:
                new_cell.concentration_of_nutrients = self.gamma * max([neighbour_cell.concentration_of_nutrients for neighbour_cell in cell.neighbours()])
        self.terrain = new_terrain

    def calculate_peat_growth(self):
        for cell in self.terrain.cells():
            if cell.height_of_water > 0:
                cell.peat_bog_thickness += self.mu * cell.concentration_of_nutrients
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
            'water_timeline': self.total_water,
            'water_in_timeline': self.water_in,
            'water_out_timeline': self.water_out,
            'terrain_timeline': self.terrain_timeline
        }
        
