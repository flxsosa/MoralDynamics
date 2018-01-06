# Moral Dynamics
This repo contains all the necessary code to reproduce the Moral Dynamics project. The project is headed by Felix Sosa, Tobias Gerstenberg, Tomer Ullman, Josh Tenenbaum, and Sam Gershman.

## Getting Started 
### Running Simulations Locally
From the terminal run:
```bash
$ git clone http://github.com/flxsosa/MoralDynamics
$ cd MoralDynamics/code/python
$ python main.py
```
Then simply follow the terminal prompt from there!

### Running MTurk Experiments Using Psiturk
From the terminal run:
```bash
$ git clone http://github.com/flxsosa/MoralDynamics
$ cd MoralDynamics/code/javascript/experiment_of_your_choice
$ psiturk
[psiturk]$ server on
[psiturk]$ debug
```
Then simply follow the webpage prompt from there!

## Simulation [Python] Overview 
### main.py
Serves as entry point. Contains functions for displaying terminal menu of possible simulations to choose from.

### simulations.py
Contains each simulation. Currently, each simulation is a function that is called on. Due to repetiive structure, this will be turned into a class in the future. Each simulation will be an instance of that class.

### infer.py
[Deprecated - to be replaced] Contains functions for inferring physical effort values exerted by an Agent given a simulation.

### graph.py
[Refactoring - in the process of refactoring] Contains functions for collecting and plotting simulation data, given a set of simulations.

### sim.py
[Deprecated - to be replaced] Contains each simulation needed for graph.py.

### helper.py
Contains helper functions for simulations.py, main.py, and graph.py.

### handlers.py
Contains Pymunk collision handlers for simulations.py.

### agents.py
Contains classes for each body in each simulation (Agent, Patient, Fireball).

## Experiment [Javascript] Overview 
### Experiment 1
### Experiment 2
