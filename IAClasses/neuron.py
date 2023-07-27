import numpy as np


class Neuron:
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.weights = np.random.randn(self.output_size, self.input_size) * 10
        self.bias = np.random.randn(self.output_size)

    def forward(self, x: np.array):
        return x @ self.weights.T + self.bias

    def info(self, number: int = 0):
        if self.output_size > 1:
            print(f"[{number}] Layer :: Input size {self.input_size} and Output size {self.output_size}")
        else:
            print(f" Neuron :: Input size {self.input_size} and Output size {self.output_size}")
