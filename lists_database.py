

character_names = [
    "Ahsoka Tano", "Darth Vader", "Luke Skywalker", "Rey", "Kylo Ren",
    "Yoda", "Palpatine", "Han Solo", "Chewbacca", "Leia Organa",
    # Add the rest of your character names here...
]

Salvage = ["Carbonite circuit board", "Bronzium wiring", "Chromium transistor", "Aurodium heatsink",
           "Electrium conductor", "Zinbiddle card", "Impulse detector", "Aeromagnifier",
           "Gyrda keypad", "Droid brain"]

Signal_Data = ["Fragmented [light blue]", "Incomplete [green]", "Flawed [dark blue]"]

salvage_reqs = [
    [40, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # R0
    [30, 40, 0, 0, 0, 0, 0, 0, 0, 0],  # R1
    [30, 40, 0, 0, 0, 0, 0, 0, 0, 0],  # R2
    [30, 40, 40, 0, 0, 0, 0, 0, 0, 0],  # R3
    [30, 40, 30, 20, 0, 0, 0, 0, 0, 0],  # R4
    [20, 30, 30, 20, 20, 0, 0, 0, 0, 0],  # R5
    [20, 30, 20, 20, 20, 10, 0, 0, 0, 0],  # R6
    [0, 0, 20, 20, 20, 20, 20, 20, 0, 0],  # R7
    [0, 0, 20, 20, 20, 20, 20, 20, 20, 20],  # R8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # R9
]

signalData_reqs = [
    [0, 0, 0], [15, 0, 0], [20, 15, 0], [20, 25, 0],
    [20, 25, 15], [20, 25, 25], [20, 25, 35], [20, 25, 45],
    [30, 30, 55], [0, 0, 0]
]