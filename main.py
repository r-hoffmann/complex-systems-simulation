import json
from Model import Model

def read_json(filename='configuration.json'):
    with open(filename) as file:
        return json.load(file)

if __name__ == "__main__":
    parameters = read_json()

    model = Model(parameters)
    model.step()