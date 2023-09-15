# neat-pong

### Requirements for this project: python, pygame, neat-python

The game itself is just a standard pong game made in a class for easier use for the AI, with small extras like hit counter which you can turn on/off, and a Game Informations class for easier data passing.
You can modify the height and width values of different objects as well as the window size however you'd like.
If you'd like to play normal game of pong with a friend, just run the `__init__.py` file.

All the AI things are in `pong_neat.py` file. You can try and train it by yourself, just simply un-comment `run(config)` and comment `load_ai(config)` in the main function.

When training it saves each generation into a 'snapshot', so that you can stop training and then resume from it at any time.
Also, the best AI gets saved into a python pickle format, so that you can play against it by yourself.

To play vs my trained AI just run `pong_neat.py`.
