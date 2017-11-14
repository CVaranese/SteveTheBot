# neutral with actions
A = 0
B = 1
X = 2
Z = 3
L = 4
# 5 movements no action
RIGHT = 5
DOWN = 6
LEFT = 7
UP = 8
NEUTRAL = 9
# right with actions
A_RIGHT = 10
B_RIGHT = 11
X_RIGHT = 12
Z_RIGHT = 13
L_RIGHT = 14
# left with actions
A_LEFT = 15
B_LEFT = 16
X_LEFT = 17
Z_LEFT = 18
L_LEFT = 19
# down with actions
A_DOWN = 20
B_DOWN = 21
X_DOWN = 22
Z_DOWN = 23
L_DOWN = 24
# up with actions
A_UP = 25
B_UP = 26
X_UP = 27
Z_UP = 28
L_UP = 29
# taunt
TAUNT = 30


# takes the max of the output
# and returns (button, (x,y))
def decide_action(agentOutput):
    action_index = agentOutput.index(max(agentOutput))

    if action_index == A:
        return enums.Button.BUTTON_A, (.5, .5)
    elif action_index == B:
        return enums.Button.BUTTON_B, (.5, .5)
    elif action_index == X:
        return enums.Button.BUTTON_X, (.5, .5)
    elif action_index == L:
        return enums.Button.BUTTON_L, (.5, .5)
    elif action_index == Z:
        return enums.Button.BUTTON_Z, (.5, .5)

    elif action_index == RIGHT:
        return "", (1, .5)
    elif action_index == DOWN:
        return "", (.5, 0)
    elif action_index == LEFT:
        return "", (0, .5)
    elif action_index == UP:
        return "", (.5, 1)
    elif action_index == NEUTRAL:
        return "", (.5, .5)

    elif action_index == A_RIGHT:
        return enums.Button.BUTTON_A, (1, .5)
    elif action_index == B_RIGHT:
        return enums.Button.BUTTON_B, (1, .5)
    elif action_index == X_RIGHT:
        return enums.Button.BUTTON_X, (1, .5)
    elif action_index == L_RIGHT:
        return enums.Button.BUTTON_L, (1, .5)
    elif action_index == Z_RIGHT:
        return enums.Button.BUTTON_Z, (1, .5)

    elif action_index == A_LEFT:
        return enums.Button.BUTTON_A, (0, .5)
    elif action_index == B_LEFT:
        return enums.Button.BUTTON_B, (0, .5)
    elif action_index == X_LEFT:
        return enums.Button.BUTTON_X, (0, .5)
    elif action_index == L_LEFT:
        return enums.Button.BUTTON_L, (0, .5)
    elif action_index == Z_LEFT:
        return enums.Button.BUTTON_Z, (0, .5)

    elif action_index == A_DOWN:
        return enums.Button.BUTTON_A, (.5, 0)
    elif action_index == B_DOWN:
        return enums.Button.BUTTON_B, (.5, 0)
    elif action_index == X_DOWN:
        return enums.Button.BUTTON_X, (.5, 0)
    elif action_index == L_DOWN:
        return enums.Button.BUTTON_L, (.5, 0)
    elif action_index == Z_DOWN:
        return enums.Button.BUTTON_Z, (.5, 0)

    elif action_index == A_UP:
        return enums.Button.BUTTON_A, (.5, 1)
    elif action_index == B_UP:
        return enums.Button.BUTTON_B, (.5, 1)
    elif action_index == X_UP:
        return enums.Button.BUTTON_X, (.5, 1)
    elif action_index == L_UP:
        return enums.Button.BUTTON_L, (.5, 1)
    elif action_index == Z_UP:
        return enums.Button.BUTTON_Z, (.5, 1)

    elif action_index == TAUNT:
        return enums.Button.BUTTON_D_UP, (.5, .5)