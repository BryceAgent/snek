import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from random import randint
import keyboard
import time
import argparse
import sys


def field_maker(x,y):
    global field,snek,direction,a,b,food,moves,score

    # create field
    field = np.array([])
    # create snek stack to record position of snake's points
    snek = []

    field = np.zeros(shape=(x,y))
    a = randint(5,x-5)
    b = randint(5,y-5)

    # snek's location on field
    field[a,b] = 1

    # initialize a direction for the snake to be moving
    direction = randint(0,3)

    snek = [[a,b]]

    food = food_add(x,y)

    moves = 100
    score = 0

    return field, snek, direction, a,b, food


def food_add(x,y):
    global food

    fx = randint(0,x-1)
    fy = randint(0,y-1)

    for pt in snek:
        if fx == pt[0] and fy == pt[1]:
            food_add(x,y)

    food = [fx,fy]

    return food


def pause():
    p = True

    while p is True:
        if keyboard.is_pressed('space'):
            p = False
        pass


def snek_update(frameNum,img,x,y):
    global field, snek, direction, a, b, food, score, moves, score_label, moves_label, new

    new = False

    new_field = field.copy()
    new_direction = direction
    new_snek = snek.copy()
    new_a = a
    new_b = b
    new_food = food

    # determine direction of movement
    start_time = time.time()
    seconds = 0.25
    loop = True

    while loop == True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > seconds:
            loop = False

        if keyboard.is_pressed('left arrow'):
            if new_direction == 2:
                pass
            else:
                new_direction = 0
        if keyboard.is_pressed('right arrow'):
            if new_direction == 0:
                pass
            else:
                new_direction = 2
        if keyboard.is_pressed('up arrow'):
            if new_direction == 3:
                pass
            else:
                new_direction = 1
        if keyboard.is_pressed('down arrow'):
            if new_direction == 1:
                pass
            else:
                new_direction = 3
        if keyboard.is_pressed('space'):
            pause()

        # movement
    if new_direction == 0:  # left
        new_b -= 1
    if new_direction == 1:  # up
        new_a -= 1
    if new_direction == 2:  # right
        new_b += 1
    if new_direction == 3:  # down
        new_a += 1

    # boundaries
    if new_a < 0 or new_b < 0:
        print("Woops!")
        print("Final score is {}".format(score))
        quit()

    if new_a > x-1 or new_b > y-1:
        print("Woops!")
        print("Final score is {}".format(score))
        quit()

    # collision detection
    for pt in range(len(new_snek)-1):
        if new_snek[0] == new_snek[pt+1]:
            print("Woops!")
            print("Final score is {}".format(score))
            quit()

    # move snek and find food
    if new_field[new_a,new_b] == 2:
        new_snek = [[new_a,new_b]] + new_snek
        new_field[new_a,new_b] = 1
        new_food = food_add(x,y)
        score += 1
        moves += 50
    else:
        new_snek = [[new_a,new_b]] + new_snek
        new_field[new_snek[-1][0],new_snek[-1][1]] = 0
        del new_snek[-1]

    moves = moves - 1
    if moves == 0:
        print("Dead!")
        print("Final score is {}".format(score))
        quit()

    # draw snek
    for pt in new_snek:
        new_field[pt[0],pt[1]] = 1

    new_field[new_food[0],new_food[1]] = 2

    # update data
    img.set_data(new_field)
    field[:] = new_field[:]
    snek[:] = new_snek[:]
    a = new_a
    b = new_b
    direction = new_direction
    food = new_food

    score_label.set_text(score)
    moves_label.set_text(moves)

    return img,direction,field,a,b,snek,food,


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="snek")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    args = parser.parse_args()

    # set field
    x = 20
    y = 20
    if args.N and int(args.N) > 8:
        x = int(args.x)
    if args.N and int(args.N) > 8:
        y = int(args.y)

    field, snek, direction, a,b, food = field_maker(x, y)

    updateInterval = 100
    if args.interval:
        updateInterval = int(args.interval)

    global score_label, moves_label

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(field, animated=True)
    img.axes.get_xaxis().set_visible(False)
    img.axes.get_yaxis().set_visible(False)

    score_label = ax.text(0,0.5, r'score: {}'.format(score), fontsize=10, color='white')
    moves_label = ax.text(0,1.5, r'moves: {}'.format(moves), fontsize=10, color='white')

    ani = animation.FuncAnimation(fig, snek_update, fargs=(img,x,y),
                                                    interval=updateInterval)


    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['vcodec', 'libx264'])

    plt.show()


main()
