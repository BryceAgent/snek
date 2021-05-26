# snek
snek.py is a functional game of snake which a human can play.

You can run the game by calling main(). Controls are the arrow keys. Spacebar will pause and unpause.

snek_NN_player.py is a genetic algorithm designed to generate a neural network that will play snake. However, performance could never be improved beyond mediocre (for a human) results. Best score my NN GA could achieve was about 40 points after training for approximately one hour. I have decided to put it back on the shelf for now, perhaps I will come back to it later when I have some new ideas how to improve its performance. Considered but decided against implementing backpropagation as that would make it no longer a "pure" genetic algorithm which was the focus of my project.

Of note is that the use of a "segregated input layer" appeared to perform better than a more standard, "vanilla" neural network that processed all inputs through a single layer.

Also of note is the implementation of parfor in order to harness parallelization of code execution via multithreading on the multiple CPU cores on my computer.

I also implemented a variation on the genetic algorithm called "Non-Dominated Selection." It works by defining a pareto optimal boundary and then selecting several "tiers" of elites to be the parents of the next generation.
