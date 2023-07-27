from GameClasses.dinosaur_ia import DinosaurIA
from IA.neural_network import NN
from IA.elitist import Elitist
import numpy as np
import pickle


class GeneticAlgorithm:
    def __init__(self, num_generations, population_size, target, rate_mutation: float = 0.005,
                 start_rate_crossing: float = 0.8, start_rate_mutation: float = 0.2, decimal_place: int = 5,
                 number_of_elitists: int = 4, limit_stagnant_generations: int = 18, inferior_limit_pos: int = 80,
                 upper_limit_pos: int = 220):

        self.decimal_place = 10 ** decimal_place
        self.target = target
        self.expected_score = None

        self.num_generations = num_generations
        self.population_size = population_size
        self.num_of_elitists = number_of_elitists

        self.rate_mutation = rate_mutation
        self.start_rate_crossing = start_rate_crossing
        self.start_rate_mutation = start_rate_mutation

        self.current_rate_crossing = None
        self.current_rate_mutation = None

        self.inferior_limit_pos = inferior_limit_pos
        self.upper_limit_pos = upper_limit_pos

        self.current_generation = None
        self.stagnant_generations = None
        self.limit_stagnant_generations = limit_stagnant_generations

        self.population = None
        self.elitists = None

        self.best_nn = None
        self.file = "dino.obj"

    def load_best_ind(self):
        with open(self.file, "rb") as f:
            self.best_nn = pickle.load(f)

        best_dinosaur = DinosaurIA(color="red")
        best_dinosaur.neurons = self.best_nn

        return best_dinosaur

    def start_population(self):
        self.population = []
        self.elitists = []

        for i in range(self.population_size):
            self.population.append(DinosaurIA(x_pos=np.random.randint(self.inferior_limit_pos, self.upper_limit_pos)))

        for i in range(self.num_of_elitists):
            self.elitists.append(Elitist(self.population[i].neurons, self.population[i].score,
                                         self.population[i].x_pos))

        self.current_rate_crossing = self.start_rate_crossing
        self.current_rate_mutation = self.start_rate_mutation

        self.current_generation = 1
        self.stagnant_generations = 0
        self.expected_score = (self.target / self.num_generations) * self.current_generation

    @staticmethod
    def fitness(dinosaur: DinosaurIA):
        dinosaur.score = dinosaur.score

    def evaluation(self):
        sum_score = 0
        for idx, current in enumerate(self.population):
            self.fitness(self.population[idx])
            sum_score += current.score

        for current in self.population:
            current.performance = (current.score * 360) / sum_score

    def elitism(self):
        self.population = sorted(self.population, key=lambda x: x.score, reverse=True)

        for i in range(self.num_of_elitists):
            self.elitists.append(Elitist(self.population[i].neurons, self.population[i].score,
                                         self.population[i].x_pos))
        self.elitists = sorted(self.elitists, key=lambda x: x.score, reverse=True)
        self.elitists = self.elitists[0:self.num_of_elitists]

    def check_stagnation(self, max_score, epsilon: float = 0.98):
        #if self.current_generation == 1 and max_score < 1000:
        #    return True

        self.expected_score = (self.target/self.num_generations) * self.current_generation
        if max_score <= self.elitists[0].score * epsilon or max_score <= self.expected_score:
            self.stagnant_generations += 1
        else:
            self.stagnant_generations = 0

        return True if self.stagnant_generations == self.limit_stagnant_generations else False

    def info_betters(self):
        for idx, elit in enumerate(self.elitists):
            print(f"[{idx}] Dinosaur Neuron --- Score :: {elit.score}")

    def roulette(self) -> DinosaurIA:
        sorted_number = np.random.rand() * 360
        sum_performance = 0

        for current in self.population:
            sum_performance += current.performance
            if sum_performance >= sorted_number:
                return current

        return self.population[self.population_size - 1]

    def float_to_bin(self, x: float):
        bin_str = bin(int(x * self.decimal_place))
        idx = bin_str.find("b")
        return bin_str[idx + 1:]

    def bin_to_float(self, x: str):
        return int(x, 2) / self.decimal_place

    def cross_over(self, number1, number2):
        number1 = self.float_to_bin(number1)
        number2 = self.float_to_bin(number2)

        limit = len(number1) if len(number1) > len(number2) else len(number2)

        cut_point1 = np.random.randint(1, limit - 2)
        cut_point2 = np.random.randint(cut_point1 + 1, limit - 1)

        new_number1 = number1[:cut_point1] + number2[cut_point1:cut_point2] + number1[cut_point2:]
        new_number2 = number2[:cut_point1] + number1[cut_point1:cut_point2] + number2[cut_point2:]

        return self.bin_to_float(new_number1), self.bin_to_float(new_number2)

    def mutation(self, number: float, rate: float = None):
        if rate is None:
            rate = self.rate_mutation

        chromosome = self.float_to_bin(number)
        for i in range(len(chromosome)):
            if np.random.rand() < rate:
                current = chromosome[i:i + 1]
                current = '1' if current == '0' else '0'

                init = chromosome[0:i]
                end = chromosome[i + 1:32]
                chromosome = init + current + end

        return self.bin_to_float(chromosome)

    def reproduction(self, father_nn, father_pos, mother_nn, mother_pos) -> (DinosaurIA, DinosaurIA):
        first_son_nn = NN(father_nn.structure)
        second_son_nn = NN(father_nn.structure)

        for i, layer in enumerate(father_nn.layers):
            for j, weights in enumerate(layer.weights):
                for k, weight in enumerate(layer.weights[j]):

                    # Cross the Weights
                    if np.random.rand() < self.current_rate_crossing:
                        father_wei = father_nn.layers[i].weights[j][k]
                        mother_wei = mother_nn.layers[i].weights[j][k]
                        child1, child2 = self.cross_over(father_wei, mother_wei)

                        first_son_nn.layers[i].weights[j][k] = child1
                        second_son_nn.layers[i].weights[j][k] = child2
                    else:
                        first_son_nn.layers[i].weights[j][k] = father_nn.layers[i].weights[j][k]
                        second_son_nn.layers[i].weights[j][k] = mother_nn.layers[i].weights[j][k]

                    # Mutation Weights
                    if np.random.rand() < self.current_rate_mutation:
                        first_son_nn.layers[i].weights[j][k] = self.mutation(first_son_nn.layers[i].weights[j][k])
                        second_son_nn.layers[i].weights[j][k] = self.mutation(second_son_nn.layers[i].weights[j][k])

                # Cross the Bias
                if np.random.rand() < self.current_rate_crossing:
                    father_bias = father_nn.layers[i].bias[j]
                    mother_bias = mother_nn.layers[i].bias[j]
                    child1_bias, child2_bias = self.cross_over(father_bias, mother_bias)

                    first_son_nn.layers[i].bias[j] = child1_bias
                    second_son_nn.layers[i].bias[j] = child2_bias
                else:
                    first_son_nn.layers[i].bias[j] = father_nn.layers[i].bias[j]
                    second_son_nn.layers[i].bias[j] = mother_nn.layers[i].bias[j]

                # Mutation the bias
                if np.random.rand() < self.current_rate_mutation:
                    first_son_nn.layers[i].bias[j] = self.mutation(first_son_nn.layers[i].bias[j])
                    second_son_nn.layers[i].bias[j] = self.mutation(second_son_nn.layers[i].bias[j])

        first_son_pos = father_pos
        second_son_pos = mother_pos

        first_son = DinosaurIA(x_pos=first_son_pos, color="pink")
        first_son.neurons = first_son_nn

        second_son = DinosaurIA(x_pos=second_son_pos, color="green")
        second_son.neurons = second_son_nn

        return first_son, second_son

    def create_new_population(self):
        new_population = []

        for idx, elit in enumerate(self.elitists):
            color = "red" if idx != 0 else "orange"
            new_dinosaur = DinosaurIA(x_pos=elit.x_pos, color=color)
            new_dinosaur.neurons = elit.nn
            new_population.append(new_dinosaur)

        self.population = sorted(self.population, key=lambda x: x.performance)

        while True:
            father = self.roulette()
            mother = self.roulette()

            first_son, second_son = self.reproduction(father.neurons, father.x_pos,
                                                      mother.neurons, mother.x_pos)

            new_population.append(first_son)
            if len(new_population) == self.population_size:
                break

            new_population.append(second_son)
            if len(new_population) == self.population_size:
                break

        self.population = new_population
        self.current_generation += 1

    def update_rates(self):
        hi_score = self.elitists[0].score

        if hi_score <= self.target:
            linear_rate = (hi_score * (self.start_rate_crossing - self.start_rate_mutation))/self.target
            self.current_rate_mutation = self.start_rate_mutation + linear_rate
            self.current_rate_crossing = self.start_rate_crossing - linear_rate

    def get_mean_score(self):
        sum_score = 0
        for current in self.population:
            sum_score += current.score
        return sum_score / self.population_size

    def result_and_save(self):
        print(f"Number Generations :: {self.current_generation}\n")

        self.elitism()
        with open(self.file, "wb") as f:
            pickle.dump(self.elitists[0], f)

        print(f"Best in Generation {self.population[0].neurons.info_nn()}")
