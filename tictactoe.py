import random


# AI algorithm for two-player games which is for "Hard" option here.
def minimax(predictive_cells, playing_player, play_decide, action):
    # Checking for win.
    if check(playing_player, predictive_cells):
        return 10
    # Checking for lose i.e opposition's win.
    elif check('O' if playing_player == 'X' else 'X', predictive_cells):
        return -10
    # Checking for draw.
    elif [j for i in predictive_cells for j in i].count(' ') == 0:
        return 0
    choices = []
    for i in range(3):
        for j in range(3):
            # Player's turn.
            if predictive_cells[i][j] == ' ' and play_decide:
                predictive_cells[i][j] = playing_player
                play_decide = False
                choices.append(minimax(predictive_cells, playing_player, play_decide,
                                       "minimize" if action == 'maximize' else "maximize"))
                play_decide = True
                action = "minimize" if action == 'maximize' else "maximize"
                predictive_cells[i][j] = ' '
            # opponent's turn.
            elif predictive_cells[i][j] == ' ' and not play_decide:
                predictive_cells[i][j] = 'O' if playing_player == 'X' else 'X'
                play_decide = True
                choices.append(minimax(predictive_cells, playing_player, play_decide,
                                       "minimize" if action == 'maximize' else "maximize"))
                play_decide = False
                action = "minimize" if action == 'maximize' else "maximize"
                predictive_cells[i][j] = ' '
    if action == 'maximize':
        return min(choices)
    else:
        return max(choices)


# Medium option
def medium(symbol, formatted_cells):
    cols = [[1 if j == symbol else j for j in i] for i in formatted_cells]
    rows = [[1 if f == symbol else f for f in k] for k in
            [[formatted_cells[j][lk] for j in range(3)] for lk in range(3)]]
    leading_diagonal = [1 if formatted_cells[i][j] == symbol else formatted_cells[i][j] for i in range(3) for j in
                       range(3) if i == j]
    leading_diagonal_dict = {0: (1, 1), 1: (2, 2), 2: (3, 3)}
    opp_diagonal = [1 if formatted_cells[i][j] == symbol else formatted_cells[i][j] for i in range(3) for j in range(3)
                    if i == 2 - j]
    opp_diagonal_dict = {0: (1, 3), 1: (2, 2), 2: (3, 1)}
    broke = False
    coordinates_i, coordinates_j = -1, -1
    for i in range(3):
        #Player's chance of winning through rows and columns.
        if 1 in cols[i] and cols[i].count(1) == 2 and ' ' in cols[i]:
            coordinates_i, coordinates_j = i + 1, cols[i].index(' ') + 1
            broke = True
            break
        elif 1 in rows[i] and rows[i].count(1) == 2 and ' ' in rows[i]:
            coordinates_i, coordinates_j = rows[i].index(' ') + 1, i + 1
            broke = True
            break
        #Opponent's chance of winning through rows and columns.
        elif 3 - cols[i].count(' ') == 2 and 1 not in cols[i]:
            coordinates_i, coordinates_j = i + 1, cols[i].index(' ') + 1
            broke = True
            break
        elif 3 - rows[i].count(' ') == 2 and 1 not in rows[i]:
            coordinates_i, coordinates_j = rows[i].index(' ') + 1, i + 1
            broke = True
            break
    if not broke:
        #Player's chance of winning through leading and opposite diagonals.
        if leading_diagonal.count(1) == 2 and leading_diagonal.count(' ') == 1:
            coordinates_i, coordinates_j = leading_diagonal_dict[leading_diagonal.index(' ')]
        elif 1 not in leading_diagonal and 3 - leading_diagonal.count(' ') == 2 and leading_diagonal.count(' ') == 1:
            coordinates_i, coordinates_j = leading_diagonal_dict[leading_diagonal.index(' ')]
        #Opponent's chance of winning through leading and opposite diagonals.
        elif opp_diagonal.count(1) == 2 and opp_diagonal.count(' ') == 1:
            coordinates_i, coordinates_j = opp_diagonal_dict[opp_diagonal.index(' ')]
        elif 1 not in opp_diagonal and 3 - opp_diagonal.count(' ') == 2 and opp_diagonal.count(' ') == 1:
            coordinates_i, coordinates_j = opp_diagonal_dict[opp_diagonal.index(' ')]
    return coordinates_i, coordinates_j


def printing(formatted_cells):
    print(*['-' for _ in range(9)], sep='')
    for i in reversed(range(3)):
        print("|", end=' ')
        for j in range(3):
            print(formatted_cells[j][i], end=' ')
        print("|", end=' ')
        print()
    print(*['-' for _ in range(9)], sep='')


#Checking for win.
def check(arg, formatted_cells_check):
    #Column-wise check.
    if any(i.count(arg) == 3 for i in formatted_cells_check):
        return True
    #Row-wise check.
    elif any(k.count(arg) == 3 for k in [[formatted_cells_check[j][lk] for j in range(3)] for lk in range(3)]):
        return True
    #Leading and Opposite diagonals check.
    elif all(
            True if formatted_cells_check[i][j] == arg else False for i in range(3) for j in range(3) if i == j) or all(
            [True if formatted_cells_check[i][j] == arg else False for i in range(3) for j in range(3) if i == 2 - j]):
        return True
    else:
        return False


def check_inputs(coordinates_i, coordinates_j, player, formatted_cells):
    if coordinates_i >= 3 or coordinates_j >= 3:
        if player == 'user':
            print("Coordinates should be from 1 to 3!")
        return False
    #Checking whether the given input position is empty.
    elif formatted_cells[coordinates_i][coordinates_j] != ' ':
        if player == 'user':
            print("This cell is occupied! Choose another one!")
        return False
    return True


def menu(option):
    formatted_cells = [[" " for _ in range(3)] for _ in range(3)]
    player = option[1]
    printing(formatted_cells)
    if player == 'easy' or player == 'medium' or player == 'hard':
        print('Making move level "{}"'.format(player))
    player_option = True
    while True:
        if player == 'user':
            try:
                coordinates_i, coordinates_j = map(int, input("Enter the coordinates: >").split())
            except ValueError:
                print("You should enter numbers!")
                continue
        elif player == 'medium':
            if option[1] == 'medium' and player_option:
                symbol = 'X'
            else:
                symbol = 'O'
            coordinates_i, coordinates_j = medium(symbol, formatted_cells)
            if coordinates_i == -1 and coordinates_j == -1:
                coordinates_i = random.choice([1, 2, 3])
                coordinates_j = random.choice([1, 2, 3])
        elif player == 'hard':
            if option[1] == 'hard' and player_option:
                symbol = 'X'
            else:
                symbol = 'O'
            max_choice = -10
            predicting_cells = [[j for j in i] for i in formatted_cells]
            if predicting_cells == [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]:
                coordinates_i = random.choice([1, 2, 3])
                coordinates_j = random.choice([1, 2, 3])
            else:
                choices = []
                for i in range(3):
                    for j in range(3):
                        if predicting_cells[i][j] == ' ':
                            predicting_cells[i][j] = symbol
                            choice = minimax(predicting_cells, symbol, False, "maximize")
                            if choice >= max_choice:
                                max_choice = choice
                                choices.append((i + 1, j + 1))
                            predicting_cells[i][j] = ' '
                coordinates_i, coordinates_j = medium(symbol, formatted_cells)
                if coordinates_i == -1 and coordinates_j == -1:
                    coordinates_i, coordinates_j = random.choice(choices)
        else:
            coordinates_i = random.choice([1, 2, 3])
            coordinates_j = random.choice([1, 2, 3])
        if check_inputs(coordinates_i - 1, coordinates_j - 1, player, formatted_cells):
            formatted_cells[coordinates_i - 1][coordinates_j - 1] = 'X' if player_option else 'O'
            printing(formatted_cells)
            player_option = False if player_option else True
            player = option[1] if player_option else option[2]
            if check("X", formatted_cells):
                print("X wins")
                exit()
            elif check("O", formatted_cells):
                print("O wins")
                exit()
            elif not any(True if j == ' ' else False for i in formatted_cells for j in i):
                print("Draw")
                exit()
            if player == 'easy' or player == 'medium' or player == 'hard':
                print('Making move level "{}"'.format(player))


if __name__ == '__main__':
    while True:
        inp = input("Input command: >").strip()
        if len(inp.split()) == 1 and inp == 'exit':
            exit()
        elif len(inp.split()) == 3 and inp.split()[0] == 'start' and inp.split()[1] in ['user', 'easy', 'medium',
                                                                                        'hard'] and inp.split()[2] in [
            'user', 'easy', 'medium', 'hard']:
            menu(inp.split())
        else:
            print("Bad parameters!")
