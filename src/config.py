DRONE_CONFIG = {
    'max_speed': 96,
    'min_speed': 36,
    'speed_step': 4,
    'base_autonomy': 5000,
    'autonomy_correction': 0.93,
    'stop_consumption': 72,
    'landing_cost': 80.0,
}

OPERATION_CONFIG = {
    'start_hour': 6,
    'end_hour': 19,
    'max_days': 7,
}

GENETIC_CONFIG = {
    'population_size': 100,
    'generations': 200,
    'mutation_rate': 0.1,
    'crossover_rate': 0.8,
    'elite_size': 10,
    'tournament_size': 5,
}

WEATHER_DATA = {
    1: {6: (17, "ENE"), 9: (18, "E"), 12: (19, "E"), 15: (19, "E"), 18: (20, "E"), 21: (20, "E")},
    2: {6: (20, "E"), 9: (19, "E"), 12: (16, "E"), 15: (19, "E"), 18: (21, "E"), 21: (21, "E")},
    3: {6: (15, "ENE"), 9: (17, "NE"), 12: (8, "NE"), 15: (20, "E"), 18: (16, "E"), 21: (15, "ENE")},
    4: {6: (8, "ENE"), 9: (11, "ENE"), 12: (7, "NE"), 15: (6, "NE"), 18: (11, "E"), 21: (11, "E")},
    5: {6: (3, "WSW"), 9: (3, "WSW"), 12: (7, "WSW"), 15: (7, "SSW"), 18: (10, "E"), 21: (11, "ENE")},
    6: {6: (4, "NE"), 9: (5, "ENE"), 12: (4, "NE"), 15: (8, "E"), 18: (15, "E"), 21: (15, "E")},
    7: {6: (6, "NE"), 9: (8, "NE"), 12: (14, "NE"), 15: (16, "E"), 18: (13, "ENE"), 21: (10, "ENE")}
}

UNIBRASIL_CEP = "82821020"
CSV_FILE = "data/coordenadas.csv"