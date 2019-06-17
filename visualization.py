import json

with open('configuration.json') as json_file:  
    data = json.load(json_file)
    
    cell_data = data["cells"]
    
    for row in cell_data:
        for cell in row:
            print(cell)