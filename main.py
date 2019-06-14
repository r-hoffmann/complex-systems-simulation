from Model import Model

if __name__ == "__main__":
    parameters = {
        'height_of_terrain': 1,
        'height_of_water': 1,
        'concentration_of_nutrients': 1,
        'peat_bog_thickness': 1
    }
    model = Model(300, 300, parameters)
    model.step()