# Construction and Optimization of a Neural Network using a Genetic Algorithm for the T-Rex Game
<img src="Assets/gif.gif" alt="Show Game" style="max-width:100%; height:auto;">

## Summary
1. [Introduction](#introduction)
2. [Neural Network](#neural-network)
3. [Genetic Algorithm](#genetic-algorithm)
4. [Prerequisites](#prerequisites)
5. [Usage](#usage)
6. [License](#license)

## Introduction
In this repository, you will find the construction and optimization of a Neural Network using only the Numpy library for building the architecture and a Genetic Algorithm for optimization. The main goal is to enable Artificial Intelligence to play the T-Rex Game interactively with the environment.

The T-Rex Game is an offline game available in the Google Chrome browser, where a dinosaur must jump over cacti and avoid obstacles to survive as long as possible. Its simplicity makes it excellent for development and testing.

## Neural Network
As mentioned earlier, the Neural Network was built using only the Numpy library. The idea is to understand the architecture and basic functioning behind libraries like PyTorch and TensorFlow. Neural Networks are structures composed of multiple artificial neurons organized in layers. These networks can learn and perform complex tasks through a training process, adjusting the weights of connections between neurons to minimize error in the output.

<table>
  <tr>
    <td>
      <h3>Class - Artificial Neuron</h3>
      <img src="Assets/neuron.png" alt="neuron class" width="450" height="250">
      <li><strong>Weight Initialization</strong>: The weights were initialized according to the He method.</li>
    </td>
    <td>
      <h3>Class - Neural Network</h3>
      <img src="Assets/nn.png" alt="ceural cetwork class" width="500" height="300">
    </td>
  </tr>
</table>

## Genetic Algorithm
Genetic Algorithms are optimization methods inspired by Darwin's theory of evolution. They use processes of natural selection, crossover, and mutation to evolve solutions to specific problems over several generations, continuously improving the fitness of solutions.

<table style="width:100%;">
  <tr>
    <td style="width:60%;">
      <h3>GA Pipeline</h3>
      <img src="Assets/GA.png" alt="ga pipeline" style="width:100%; height:auto;">
    </td>
    <td style="width:40%;">
      <img src="Assets/large_gif.gif" alt="show pipeline" style="max-width:100%; height:auto;">
      <h3>Selection</h3>
      <p>Selecting the best individual</p>
      <h3>Cloning and Mutation</h3>
      <p>The best individual is cloned, and then small random mutations are made.</p>
      <h3>Genocide</h3>
      <p>An additional step implemented is Genocide. Since the Genetic Algorithm is sensitive to the initial population, creating a large population increases the search space, allowing convergence points to be found more quickly. However, to demonstrate an iterative process, we work with only 200 agents. If stagnation occurs for 20 epochs, the entire population is randomly reinitialized.</p>
    </td>
  </tr>
</table>

## Prerequisites
Before starting, ensure you have the following prerequisites installed on your system:
- [Python 3.x](https://www.python.org/downloads/)
- [NumPy](https://numpy.org/install/)
- [Matplotlib](https://matplotlib.org/stable/users/installing.html)
- [Pygame](https://www.pygame.org/docs/)

## Usage
To explore the project, follow the steps below to download and run the main file:
```sh
python main.py
```
After execution, the game will start, and you will have three options:
1. Play
2. Play against the AI
3. Watch the iterative training

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
