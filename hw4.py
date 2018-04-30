import random
import dynamic_prog_jumpit


def read_file(file_name):
    boards = []
    with open(file_name, 'r') as f:
        for line in f:
            boards.append(list(map(int, line.split())))
    return boards


def generate_population(board):
    population = []
    n = len(board)
    pop_size = n * 10
    for i in range(pop_size):
        chromosome = [1]
        for j in range(1, n):
            chromosome.append(int(round(random.random())))
            if chromosome[j - 1] == 0 and chromosome[j] == 0:
                chromosome[j] = 1
        chromosome[n - 1] = 1
        population.append(chromosome)
    return population


def calculate_fitness(board, chromosome):
    fitness = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            fitness += board[i]
    return fitness


# Make sure the given chromosome doesnt have two consecutive 0's
def is_child_valid(child):
    for i in range(1, len(child)):
        if child[i - 1] == 0 and child[i] == 0:
            return False
    return True


def crossover(parents):
    n = len(parents[0])
    # Keep mating parents until a valid child is created
    while True:
        cut_index = random.randint(1, n - 2)
        child1 = parents[0][:cut_index] + parents[1][cut_index:]
        child2 = parents[1][:cut_index] + parents[0][cut_index:]
        if is_child_valid(child1) and is_child_valid(child2):
            break
    return [child1, child2]


def mutate(chromosome):
    gene_index = random.randint(0, len(chromosome) - 1)
    chromosome[gene_index] = 0 if chromosome[gene_index] == 1 else 1


def main():
    boards = read_file("input1.txt")
    correct = 0
    for board in boards:
        population = generate_population(board)
        # Maximum number of generations
        for generation in range(500):
            fitnesses = [calculate_fitness(board, c) for c in population]

            # Select the parents and mate
            parents = random.choices(population, weights=[x ** -1 for x in fitnesses], k=2)
            children = crossover(parents)

            # Mutate children
            invalid_children = []
            for child in children:
                if random.randint(1, 100) == 1:
                    mutate(child)
                    if not is_child_valid(child):
                        invalid_children.append(child)
            for child in invalid_children:
                children.remove(child)

            # Replace the weak chromosomes in the population with the children
            weaklings = random.choices(population, weights=fitnesses, k=len(children))
            for i in range(len(weaklings)):
                population.remove(weaklings[i])
                population.append(children[i])

        # Check if solution found is correct
        dp_cost, dp_path = dynamic_prog_jumpit.main(board)
        ga_cost = min(fitnesses)
        if dp_cost == ga_cost:
            correct += 1

        print("Board:", board)
        print("DP Cost:", dp_cost)
        print("DP Path:", dp_path)
        print("GA Cost:", ga_cost)
        print("GA Path:")
        print("----------------------------------------------------")

    print("ACCURACY:", correct / len(boards) * 100, "%")


if __name__ == '__main__':
    main()
