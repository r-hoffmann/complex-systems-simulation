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
    
    model.run(100)

    # This one takes long:
#     model.run_untill_other_side()
