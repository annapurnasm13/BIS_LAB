import random

# Define a network graph as an adjacency dictionary with edge costs (e.g., delay/latency)
NETWORK_GRAPH = {
    'A': {'B': 2, 'C': 5},
    'B': {'A': 2, 'C': 1, 'D': 4},
    'C': {'A': 5, 'B': 1, 'D': 2, 'E': 7},
    'D': {'B': 4, 'C': 2, 'E': 3, 'F': 5},
    'E': {'C': 7, 'D': 3, 'F': 1},
    'F': {'D': 5, 'E': 1}
}

SOURCE = 'A'
DESTINATION = 'F'

# GA Parameters
POPULATION_SIZE = 20
GENERATIONS = 50
MUTATION_RATE = 0.2

def generate_random_path(start, goal, graph):
    """Generates a random valid path from start to goal without infinite loops."""
    current = start
    path = [current]
    visited = set([current])
    
    while current != goal:
        neighbors = [n for n in graph[current] if n not in visited]
        if not neighbors:
            return None  # Dead end reached
        next_node = random.choice(neighbors)
        path.append(next_node)
        visited.add(next_node)
        current = next_node
    return path

def calculate_path_cost(path, graph):
    """Calculates the total cost (fitness score to minimize) of a path."""
    if not path:
        return float('inf')
    cost = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        if v in graph.get(u, {}):
            cost += graph[u][v]
        else:
            return float('inf')  # Invalid edge
    return cost

def create_initial_population(size, start, goal, graph):
    """Initializes the population with valid random paths."""
    population = []
    while len(population) < size:
        path = generate_random_path(start, goal, graph)
        if path:
            population.append(path)
    return population

def crossover(parent1, parent2):
    """Crossover: combines two paths at a shared common node."""
    common_nodes = set(parent1[1:-1]).intersection(set(parent2[1:-1]))
    if not common_nodes:
        return parent1  # No crossover point, return parent1
    
    node = random.choice(list(common_nodes))
    idx1 = parent1.index(node)
    idx2 = parent2.index(node)
    
    child = parent1[:idx1] + parent2[idx2:]
    # Check for internal loops in child
    if len(child) == len(set(child)):
        return child
    return parent1

def mutate(path, graph, goal):
    """Mutation: alters part of the path randomly."""
    if len(path) <= 2 or random.random() > MUTATION_RATE:
        return path
    
    mut_idx = random.randint(1, len(path) - 2)
    sub_path = generate_random_path(path[mut_idx - 1], goal, graph)
    if sub_path:
        return path[:mut_idx - 1] + sub_path
    return path

def run_genetic_algorithm():
    population = create_initial_population(POPULATION_SIZE, SOURCE, DESTINATION, NETWORK_GRAPH)
    
    for generation in range(GENERATIONS):
        # Sort population by path cost (lowest cost is best fitness)
        population = sorted(population, key=lambda p: calculate_path_cost(p, NETWORK_GRAPH))
        
        # Elitism: keep top 20%
        top_count = max(1, POPULATION_SIZE // 5)
        new_population = population[:top_count]
        
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.choices(population[:10], k=2)
            child = crossover(parent1, parent2)
            child = mutate(child, NETWORK_GRAPH, DESTINATION)
            if calculate_path_cost(child, NETWORK_GRAPH) != float('inf'):
                new_population.append(child)
                
        population = new_population

    best_path = min(population, key=lambda p: calculate_path_cost(p, NETWORK_GRAPH))
    return best_path, calculate_path_cost(best_path, NETWORK_GRAPH)

# Execute
optimal_path, optimal_cost = run_genetic_algorithm()
print(f"Optimal Path: {' -> '.join(optimal_path)}")
print(f"Total Cost (Delay/Weight): {optimal_cost}")
