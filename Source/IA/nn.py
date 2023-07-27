from IA.neuron import Neuron
import numpy as np


class NN:
    def __init__(self, size_input_and_amount_neurons_in_layer: np.array):  # Size inputs and outputs the each layer
        self.structure = size_input_and_amount_neurons_in_layer
        self.layers = []
        for i in range(len(self.structure) - 1):
            self.layers.append(Neuron(self.structure[i], self.structure[i + 1]))

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def softmax(x):
        shifted_x = x - np.max(x)
        exp_x = np.exp(shifted_x)
        return exp_x / np.sum(exp_x)

    def forward_nn(self, x: np.array):
        results = x
        num_layers = len(self.layers) - 1

        for idx, layer in enumerate(self.layers):
            results = layer.forward(results)
            if idx < num_layers:
                results = self.relu(results)
            else:
                results = self.softmax(results)

        return np.argmax(results)  # Return activate neuron

    def info_nn(self):
        for i, layer in enumerate(self.layers):
            layer.info(i)
            print("Bias :: ", layer.bias)
            print("Wights :: \n", layer.weights)
