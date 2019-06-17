import json
from Model import Model

def read_json(filename='configuration.json'):
    with open(filename) as file:
        return json.load(file)

if __name__ == "__main__":
    parameters = read_json()

    model = Model(parameters)
    # model.step()

    # for cell in model.terrain.cells():
    #     print(cell)
    #     for n in cell.neighbours():
    #         print(n)
    #     print()

    for i in range(3):
        for cell in model.terrain.cells():
            if cell.height_of_water > 0:
                print(cell)
        print()
        model.run()
