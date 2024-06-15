from GameClasses.ai_dinosaur import DinosaurAI
from AIClasses.elitist import Elitist
from copy import deepcopy
import numpy as np
import pickle


class GeneticAlgorithm:
    def __init__(self,
                 num_generations,
                 population_size,
                 rate_mutation: float = 0.04,
                 limit_stagnant_generations: int = 20,
                 inferior_limit_pos: int = 80,
                 upper_limit_pos: int = 220):

        self.num_generations = num_generations
        self.population_size = population_size

        self.rate_mutation = rate_mutation
        self.start_rate_mutation = rate_mutation

        self.inferior_limit_pos = inferior_limit_pos
        self.upper_limit_pos = upper_limit_pos

        self.current_generation = None
        self.stagnant_generations = None
        self.limit_stagnant_generations = limit_stagnant_generations

        self.population = None

        self.best_nn = None
        self.best_pos = None
        self.best_score = None
        self.file = "dino.obj"

    def load_best_ind(self):
        with open(self.file, "rb") as f:
            self.best_nn = pickle.load(f)

        best_dinosaur = DinosaurAI(color="red")
        best_dinosaur.neurons = self.best_nn

        return best_dinosaur

    def start_population(self):
        self.population = []

        for _ in range(self.population_size):
            self.population.append(DinosaurAI(
                x_pos=np.random.randint(self.inferior_limit_pos, self.upper_limit_pos),
                color=np.random.choice(["pink", "green", "orange", "red", "grey", "purple"])
            ))

        self.best_nn = deepcopy(self.population[0].neurons)
        self.best_pos = self.population[0].x_pos
        self.best_score = 0
        self.current_generation = 1
        self.stagnant_generations = 0

    def evaluate(self):
        self.population = sorted(self.population, key=lambda x: x.score, reverse=True)
        if self.best_score < self.population[0].score:
            self.best_nn = deepcopy(self.population[0].neurons)
            self.best_score = self.population[0].score
            self.best_pos = self.population[0].x_pos

            self.rate_mutation = self.start_rate_mutation
        else:
            self.rate_mutation += self.start_rate_mutation / 20

    def check_stagnation(self, max_score, epsilon: float = 0.98):
        if max_score <= self.best_score * epsilon:
            self.stagnant_generations += 1
        else:
            self.stagnant_generations = 0

        return True if self.stagnant_generations == self.limit_stagnant_generations else False

    def info_betters(self):
        print(f"Dinosaur Neuron --- Score :: {self.best_score}")

    def clone_best(self) -> DinosaurAI:
        son_nn = deepcopy(self.best_nn)

        for s_layer in son_nn.layers:
            for s_weights in s_layer.weights:
                if np.random.rand() <= self.rate_mutation:
                    idx = np.random.choice(s_weights.shape[0])
                    s_weights[idx] += np.random.normal(0, 1) * self.rate_mutation * 5

            if np.random.rand() <= self.rate_mutation:
                idx = np.random.choice(s_layer.bias.shape[0])
                s_layer.bias[idx] += np.random.normal(0, 1) * self.rate_mutation * 5

        son = DinosaurAI(x_pos=self.best_pos + np.random.rand() * 100,
                         color=np.random.choice(["pink", "green", "orange", "red", "grey", "purple"]))
        son.neurons = son_nn
        return son

    def create_new_population(self):
        new_population = []

        for _ in range(self.population_size):
            new_population.append(self.clone_best())

        self.population = new_population
        self.current_generation += 1

    def get_mean_score(self):
        sum_score = 0
        for current in self.population:
            sum_score += current.score
        return sum_score / self.population_size

    def result_and_save(self):
        print(f"Number Generations :: {self.current_generation}\n")

        elit = Elitist(self.best_nn, self.best_pos, self.best_score)
        with open(self.file, "wb") as f:
            pickle.dump(elit, f)
