from Model import Model

if __name__ == "__main__":
    parameters = {
        'height_of_terrain': 1,
        'height_of_water': 1,
        'concentration_of_nutrients': 1,
        'peat_bog_thickness': 1
    }
    height = 530
    width = 530
    gamma = 0.02
    rho = 0.0002
    mu = 0.00014
    slope = 0.05
    model = Model(height, width, gamma, rho, mu, slope, parameters)
    model.step()