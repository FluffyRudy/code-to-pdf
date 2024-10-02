# title: 10
# aim: Program to implement Backpropagation Algorithm using Python.

import numpy as np


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights_input_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.weights_hidden_output = np.random.uniform(
            -1, 1, (hidden_size, output_size)
        )
        self.learning_rate = 0.1

    def feedforward(self, inputs):
        self.hidden = self.sigmoid(np.dot(inputs, self.weights_input_hidden))
        self.output = self.sigmoid(np.dot(self.hidden, self.weights_hidden_output))
        return self.output

    def backward(self, inputs, target):
        output_error = target - self.output
        output_delta = output_error * self.sigmoid_derivative(self.output)

        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(self.hidden)

        # Update weights
        self.weights_hidden_output += (
            self.hidden.T.dot(output_delta) * self.learning_rate
        )
        self.weights_input_hidden += inputs.T.dot(hidden_delta) * self.learning_rate

    def train(self, inputs, target):
        self.feedforward(inputs)
        self.backward(inputs, target)

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sigmoid_derivative(x):
        return x * (1 - x)


if __name__ == "__main__":
    nn = NeuralNetwork(3, 3, 1)
    inputs = np.array([[1, 0, 1], [0, 1, 0], [1, 1, 1]])
    targets = np.array([[1], [0], [1]])

    for epoch in range(1000):
        for i in range(len(inputs)):
            nn.train(inputs[i].reshape(1, -1), targets[i])  # Reshape inputs

    print("Final output after training:")
    for input in inputs:
        print(
            f"Input: {input}, Predicted Output: {nn.feedforward(input.reshape(1, -1))}"
        )
