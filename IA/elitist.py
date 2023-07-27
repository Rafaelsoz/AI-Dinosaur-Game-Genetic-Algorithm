from IA.neural_network import NN


class Elitist:
    def __init__(self, nn: NN, score, x_pos: int = 80):
        self.nn = nn
        self.score = score
        self.x_pos = x_pos
