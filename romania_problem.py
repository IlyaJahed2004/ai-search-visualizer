# romania_problem.py

neighbors = {
    "Arad": ["Zerind", "Timisoara", "Sibiu"],
    "Zerind": ["Arad", "Oradea"],
    "Oradea": ["Zerind", "Sibiu"],
    "Timisoara": ["Arad", "Lugoj"],
    "Lugoj": ["Timisoara", "Mehadia"],
    "Mehadia": ["Lugoj", "Drobeta"],
    "Drobeta": ["Mehadia", "Craiova"],
    "Craiova": ["Drobeta", "Rimnicu", "Pitesti"],
    "Sibiu": ["Arad", "Oradea", "Fagaras", "Rimnicu"],
    "Rimnicu": ["Sibiu", "Craiova", "Pitesti"],
    "Fagaras": ["Sibiu", "Bucharest"],
    "Pitesti": ["Rimnicu", "Craiova", "Bucharest"],
    "Bucharest": ["Fagaras", "Pitesti", "Giurgiu", "Urziceni"],
    "Giurgiu": ["Bucharest"],
    "Urziceni": ["Bucharest", "Hirsova", "Vaslui"],
    "Hirsova": ["Urziceni", "Eforie"],
    "Eforie": ["Hirsova"],
    "Vaslui": ["Urziceni", "Iasi"],
    "Iasi": ["Vaslui", "Neamt"],
    "Neamt": ["Iasi"]
}

distances = {
    ("Arad", "Zerind"): 75, ("Zerind", "Arad"): 75,
    ("Arad", "Timisoara"): 118, ("Timisoara", "Arad"): 118,
    ("Arad", "Sibiu"): 140, ("Sibiu", "Arad"): 140,
    ("Zerind", "Oradea"): 71, ("Oradea", "Zerind"): 71,
    ("Oradea", "Sibiu"): 151, ("Sibiu", "Oradea"): 151,
    ("Timisoara", "Lugoj"): 111, ("Lugoj", "Timisoara"): 111,
    ("Lugoj", "Mehadia"): 70, ("Mehadia", "Lugoj"): 70,
    ("Mehadia", "Drobeta"): 75, ("Drobeta", "Mehadia"): 75,
    ("Drobeta", "Craiova"): 120, ("Craiova", "Drobeta"): 120,
    ("Craiova", "Rimnicu"): 146, ("Rimnicu", "Craiova"): 146,
    ("Craiova", "Pitesti"): 138, ("Pitesti", "Craiova"): 138,
    ("Sibiu", "Rimnicu"): 80, ("Rimnicu", "Sibiu"): 80,
    ("Sibiu", "Fagaras"): 99, ("Fagaras", "Sibiu"): 99,
    ("Fagaras", "Bucharest"): 211, ("Bucharest", "Fagaras"): 211,
    ("Rimnicu", "Pitesti"): 97, ("Pitesti", "Rimnicu"): 97,
    ("Pitesti", "Bucharest"): 101, ("Bucharest", "Pitesti"): 101,
    ("Bucharest", "Giurgiu"): 90, ("Giurgiu", "Bucharest"): 90,
    ("Bucharest", "Urziceni"): 85, ("Urziceni", "Bucharest"): 85,
    ("Urziceni", "Hirsova"): 98, ("Hirsova", "Urziceni"): 98,
    ("Hirsova", "Eforie"): 86, ("Eforie", "Hirsova"): 86,
    ("Urziceni", "Vaslui"): 142, ("Vaslui", "Urziceni"): 142,
    ("Vaslui", "Iasi"): 92, ("Iasi", "Vaslui"): 92,
    ("Iasi", "Neamt"): 87, ("Neamt", "Iasi"): 87
}

heuristics = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242,
    'Eforie': 161, 'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151,
    'Iasi': 226, 'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
    'Oradea': 380, 'Pitesti': 100, 'Rimnicu': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80,
    'Vaslui': 199, 'Zerind': 374
}

city_positions = {
    "Arad": (0, 1.5),
    "Zerind": (0, 2.5),
    "Oradea": (2, 2.5),
    "Sibiu": (1.2, -1.2),
    "Fagaras": (2, -2.8),
    "Rimnicu": (3, 0.3),
    "Timisoara": (-1, -1),
    "Lugoj": (-2, -2),
    "Mehadia": (-3, -3),
    "Drobeta": (-4, -2),
    "Craiova": (-2.8, -0.3),
    "Pitesti": (3, -0.8),
    "Bucharest": (4, -1.8),
    "Giurgiu": (4.2, -2.8),
    "Urziceni": (5.3, -0.8),
    "Hirsova": (6.8, 0),
    "Eforie": (7.5, -1.3),
    "Vaslui": (6, 0.8),
    "Iasi": (6.2, 1.8),
    "Neamt": (5.8, 2.8)
}
