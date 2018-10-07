import numpy as np
from random import shuffle, seed
from copy import deepcopy

test_size = 0.1
val_size = 0.2

seed(42)

with open("sudoku.csv") as file:
    lines = file.read().strip().split("\n")[1:]

shuffle(lines)

with open("test_sudoku.csv", "w") as file:
    file.write("\n".join(lines[:int(len(lines)*test_size)]))

lines = lines[int(len(lines)*test_size):]
lines = list(map(lambda line: line.split(","), lines))
quizzes = [line[0] for line in lines]
solved = [line[1] for line in lines]
quizzes = np.array(list(map(lambda line: list(map(float, line)), quizzes))).reshape((-1,9,9))
solved = np.array(list(map(lambda line: list(map(float, line)), solved))).reshape((-1,9,9))

for q, s in zip(quizzes, solved):
    if q[0,0] == 0: continue
    wh = np.where(q == 0)
    i, j = wh[0][0], wh[1][0]
    while i > 2:
        q[3*(i//3-1):3*(i//3),:], q[3*(i//3):3*(i//3+1),:] = deepcopy(q[3*(i//3):3*(i//3+1),:]), deepcopy(q[3*(i//3-1):3*(i//3),:])
        s[3*(i//3-1):3*(i//3),:], s[3*(i//3):3*(i//3+1),:] = deepcopy(s[3*(i//3):3*(i//3+1),:]), deepcopy(s[3*(i//3-1):3*(i//3),:])
        i -= 3
    while i > 0:
        q[i,:], q[i-1,:] = deepcopy(q[i-1,:]), deepcopy(q[i,:])
        s[i,:], s[i-1,:] = deepcopy(s[i-1,:]), deepcopy(s[i,:])
        i -= 1

    while j > 2:
        q[:,3*(j//3-1):3*(j//3)], q[:,3*(j//3):3*(j//3+1)] = deepcopy(q[:,3*(j//3):3*(j//3+1)]), deepcopy(q[:,3*(j//3-1):3*(j//3)])
        s[:,3*(j//3-1):3*(j//3)], s[:,3*(j//3):3*(j//3+1)] = deepcopy(s[:,3*(j//3):3*(j//3+1)]), deepcopy(s[:,3*(j//3-1):3*(j//3)])
        j -= 3
    while j > 0:
        q[:,j], q[:,j-1] = deepcopy(q[:,j-1]), deepcopy(q[:,j])
        s[:,j], s[:,j-1] = deepcopy(s[:,j-1]), deepcopy(s[:,j])
        j -= 1

    if q[0,0] != 0:
        print(q, s)


quizzes = quizzes.reshape(-1,81)
solved = solved.reshape(-1,81)

quizzes = ["".join(map(lambda x: str(int(x)), q)) for q in quizzes]
solved = ["".join(map(lambda x: str(int(x)), s)) for s in solved]

lines = [q+","+s for q,s in zip(quizzes, solved)]

with open("validation_sudoku.csv", "w") as file:
    file.write("\n".join(lines[:int(len(lines)*val_size)]))

with open("train_sudoku.csv", "w") as file:
    file.write("\n".join(lines[int(len(lines)*val_size):]))