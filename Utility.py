import numpy as np
import melee
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
# up right with actions
A_NE = 30
B_NE = 31
X_NE = 32
Z_NE = 33
L_NE = 34
# up left with actions
A_NW = 35
B_NW = 36
X_NW = 37
Z_NW = 38
L_NW = 39
# down right with actions
A_SE = 40
B_SE = 41
X_SE = 42
Z_SE = 43
L_SE = 44
# down left with actions
A_SW = 45
B_SW = 46
X_SW = 47
Z_SW = 48
L_SW = 49
# 4 more movements no action
NE = 50
NW= 51
SE = 52
SW = 53


# takes the max of the output
# and returns (button, (x,y))
def decide_action(action_index):
    #agentOutput.index(max(agentOutput))

    if action_index == A:
        return melee.enums.Button.BUTTON_A, (.5, .5)
    elif action_index == B:
        return melee.enums.Button.BUTTON_B, (.5, .5)
    elif action_index == X:
        return melee.enums.Button.BUTTON_X, (.5, .5)
    elif action_index == L:
        return melee.enums.Button.BUTTON_L, (.5, .5)
    elif action_index == Z:
        return melee.enums.Button.BUTTON_Z, (.5, .5)

    elif action_index == RIGHT:
        return None, (1, .5)
    elif action_index == DOWN:
        return None, (.5, 0)
    elif action_index == LEFT:
        return None, (0, .5)
    elif action_index == UP:
        return None, (.5, 1)
    elif action_index == NEUTRAL:
        return None, (.5, .5)

    elif action_index == NE:
        return None, (1, 1)
    elif action_index == NW:
        return None, (0, 1)
    elif action_index == SE:
        return None, (1, 0)
    elif action_index == SW:
        return None, (0, 0)

    elif action_index == A_RIGHT:
        return melee.enums.Button.BUTTON_A, (1, .5)
    elif action_index == B_RIGHT:
        return melee.enums.Button.BUTTON_B, (1, .5)
    elif action_index == X_RIGHT:
        return melee.enums.Button.BUTTON_X, (1, .5)
    elif action_index == L_RIGHT:
        return melee.enums.Button.BUTTON_L, (1, .5)
    elif action_index == Z_RIGHT:
        return melee.enums.Button.BUTTON_Z, (1, .5)

    elif action_index == A_LEFT:
        return melee.enums.Button.BUTTON_A, (0, .5)
    elif action_index == B_LEFT:
        return melee.enums.Button.BUTTON_B, (0, .5)
    elif action_index == X_LEFT:
        return melee.enums.Button.BUTTON_X, (0, .5)
    elif action_index == L_LEFT:
        return melee.enums.Button.BUTTON_L, (0, .5)
    elif action_index == Z_LEFT:
        return melee.enums.Button.BUTTON_Z, (0, .5)

    elif action_index == A_DOWN:
        return melee.enums.Button.BUTTON_A, (.5, 0)
    elif action_index == B_DOWN:
        return melee.enums.Button.BUTTON_B, (.5, 0)
    elif action_index == X_DOWN:
        return melee.enums.Button.BUTTON_X, (.5, 0)
    elif action_index == L_DOWN:
        return melee.enums.Button.BUTTON_L, (.5, 0)
    elif action_index == Z_DOWN:
        return melee.enums.Button.BUTTON_Z, (.5, 0)

    elif action_index == A_UP:
        return melee.enums.Button.BUTTON_A, (.5, 1)
    elif action_index == B_UP:
        return melee.enums.Button.BUTTON_B, (.5, 1)
    elif action_index == X_UP:
        return melee.enums.Button.BUTTON_X, (.5, 1)
    elif action_index == L_UP:
        return melee.enums.Button.BUTTON_L, (.5, 1)
    elif action_index == Z_UP:
        return melee.enums.Button.BUTTON_Z, (.5, 1)

    elif action_index == A_NE:
        return melee.enums.Button.BUTTON_A, (1, 1)
    elif action_index == B_NE:
        return melee.enums.Button.BUTTON_B, (1, 1)
    elif action_index == X_NE:
        return melee.enums.Button.BUTTON_X, (1, 1)
    elif action_index == L_NE:
        return melee.enums.Button.BUTTON_L, (1, 1)
    elif action_index == Z_NE:
        return melee.enums.Button.BUTTON_Z, (1, 1)

    elif action_index == A_NW:
        return melee.enums.Button.BUTTON_A, (0, 1)
    elif action_index == B_NW:
        return melee.enums.Button.BUTTON_B, (0, 1)
    elif action_index == X_NW:
        return melee.enums.Button.BUTTON_X, (0, 1)
    elif action_index == L_NW:
        return melee.enums.Button.BUTTON_L, (0, 1)
    elif action_index == Z_NW:
        return melee.enums.Button.BUTTON_Z, (0, 1)

    elif action_index == A_SW:
        return melee.enums.Button.BUTTON_A, (0, 0)
    elif action_index == B_SW:
        return melee.enums.Button.BUTTON_B, (0, 0)
    elif action_index == X_SW:
        return melee.enums.Button.BUTTON_X, (0, 0)
    elif action_index == L_SW:
        return melee.enums.Button.BUTTON_L, (0, 0)
    elif action_index == Z_SW:
        return melee.enums.Button.BUTTON_Z, (0, 0)

    elif action_index == A_SE:
        return melee.enums.Button.BUTTON_A, (1, 0)
    elif action_index == B_SE:
        return melee.enums.Button.BUTTON_B, (1, 0)
    elif action_index == X_SE:
        return melee.enums.Button.BUTTON_X, (1, 0)
    elif action_index == L_SE:
        return melee.enums.Button.BUTTON_L, (1, 0)
    elif action_index == Z_SE:
        return melee.enums.Button.BUTTON_Z, (1, 0)
