import json

mirror = {0: 12, 1: 11, 2: 10, 3: 9, 4: 8, 5: 7}
steal = True
max_levels = 5

def save_game(save_name, state, current_player, is_final, another_turn, steal, max_levels, score):
    data = {
        "state": state,
        "current_player": current_player,
        "is_final": is_final,
        "another_turn": another_turn,
        "steal": steal,
        "max_levels": max_levels,
        "score": score,
    }
    with open(f'{save_name}.json', 'w') as outfile:
        json.dump(data, outfile)


def load_previous_game(save_name):
    with open(f'{save_name}.json') as json_file:
        data = json.load(json_file)
        return data

def display_state(state):
    print(f"""
\t\t\t\t\033[91mPlayer 2 - AI\033[0m

\t\033[91m【{state[13]}】\033[0m\t{state[12]}\t{state[11]}\t{state[10]}\t{state[9]}\t{state[8]}\t{state[7]}  
\t\033[1m____________________________________________________________\033[0m

\t\t{state[0]}\t{state[1]}\t{state[2]}\t{state[3]}\t{state[4]}\t{state[5]}\t\033[94m【{state[6]}】\033[0m
                
\t\t\t\t\033[94mPlayer 1 - User\033[0m
        
\t\033[1m-------------------------------------------------------------\033[0m
    """)


def check_for_final(state):
    is_final = False
    sum_left = 0
    if state[0:6] == [0, 0, 0, 0, 0, 0]:
        is_final = True
        for bin_number in range(7, 13):
            sum_left = sum_left + state[bin_number]
            state[bin_number] = 0
        state[13] = state[13] + sum_left

    elif state[7:13] == [0, 0, 0, 0, 0, 0]:
        is_final = True
        for bin_number in range(6):
            sum_left = sum_left + state[bin_number]
            state[bin_number] = 0
        state[6] = state[6] + sum_left

    return state, is_final


def make_a_move(state, bin_number, player):
    global steal
    move = state[:]
    another_turn = False
    if player == "user":
        stones = state[bin_number]
        if stones > 0:
            next_index = bin_number + 1
            for x in range(stones):
                if x == stones - 1:
                    if move[next_index] == 0 and not next_index == 13 and not next_index == 6 and steal:
                        if next_index < 6:
                            mirror_index = mirror[next_index]
                            move[bin_number] = move[bin_number] - 1
                            move[6] = move[6] + move[mirror_index] + 1
                            move[mirror_index] = 0
                        elif 7 <= next_index <= 12:
                            move[bin_number] = move[bin_number] - 1
                            move[next_index] = move[next_index] + 1
                    elif next_index == 6:
                        move[bin_number] = move[bin_number] - 1
                        move[next_index] = move[next_index] + 1
                        another_turn = True
                    elif next_index == 13:
                        next_index = 0
                        move[bin_number] = move[bin_number] - 1
                        if move[next_index] == 0 and steal:
                            mirror_index = mirror[next_index]
                            move[6] = move[6] + move[mirror_index] + 1
                            move[mirror_index] = 0
                        else:
                            move[next_index] = move[next_index] + 1
                    else:
                        move[bin_number] = move[bin_number] - 1
                        move[next_index] = move[next_index] + 1
                else:
                    if next_index == 13:  # dropping stone in ai's mancala is skipped
                        next_index = (next_index + 1) % 14
                        move[bin_number] = move[bin_number] - 1
                        move[next_index] = move[next_index] + 1
                    else:
                        move[bin_number] = move[bin_number] - 1
                        move[next_index] = move[next_index] + 1

                next_index = (next_index + 1) % 14

            move, is_final = check_for_final(move)
            return move, is_final, another_turn
        else:
            return [], False, False

    elif player == "ai":
        bin_number = bin_number + 7
        stones = state[bin_number]
        if stones > 0:
            next_index = bin_number + 1
            for x in range(stones):
                if x == stones - 1:
                    if move[next_index] == 0 and not next_index == 6 and not next_index == 13 and steal:
                        if 7 <= next_index <= 12:
                            mirror_index = list(
                                mirror.values()).index(next_index)
                            move[bin_number] = move[bin_number] - 1
                            move[13] = move[13] + move[mirror_index] + 1
                            move[mirror_index] = 0
                        elif 0 <= next_index <= 5:
                            move[bin_number] = move[bin_number] - 1
                            move[next_index] = move[next_index] + 1
                    elif next_index == 13:
                        move[bin_number] = move[bin_number] - 1
                        move[next_index] = move[next_index] + 1
                        another_turn = True
                    elif next_index == 6:
                        next_index = 7
                        move[bin_number] = move[bin_number] - 1
                        if move[next_index] == 0 and steal:
                            mirror_index = list(
                                mirror.values()).index(next_index)
                            move[13] = move[13] + move[mirror_index] + 1
                            move[mirror_index] = 0
                        else:
                            move[next_index] = move[next_index] + 1
                    else:
                        move[bin_number] = move[bin_number] - 1
                        move[next_index] = move[next_index] + 1
                else:
                    if next_index == 6:  # dropping stone in user's mancala is skipped
                        next_index = (next_index + 1) % 14
                        move[bin_number] = move[bin_number] - 1
                        move[next_index] = move[next_index] + 1
                    else:
                        move[bin_number] = move[bin_number] - 1
                        move[next_index] = move[next_index] + 1

                next_index = (next_index + 1) % 14

            move, is_final = check_for_final(move)
            return move, is_final, another_turn

        else:
            return [], False, False


def next_moves(state, player):
    global steal
    next_moves = []
    for bin_number in range(6):
        move, is_final, another_turn = make_a_move(state, bin_number, player)
        if move:
            next_moves.append((move, is_final, another_turn))

    return next_moves


def evaluate(state_tuple, is_max=1, level=0, alpha=float('-inf'), beta=float('inf')):
    global max_levels
    global steal
    state, is_final, another_turn = state_tuple

    if is_max:
        possible_states = next_moves(state, "ai")
    else:
        possible_states = next_moves(state, "user")

    optimal_next_state = tuple()
    # if we hit a state with no next moves, return the score of this state
    # if we reached the max depth return the value of the utility function (current score)
    if is_final or max_levels == level:
        return state[13] - state[6], state_tuple

    # if the user gets another turn flip is_max, so when it is flipped
    # it has the correct value
    if another_turn:
        next_max = is_max
    else:
        next_max = not is_max

    for next_state in possible_states:
        score, state_tuple = evaluate(
            next_state, next_max, level + 1, alpha, beta)

        if is_max:
            if score > alpha:
                alpha = score
                optimal_next_state = next_state
        else:
            if score < beta:
                beta = score
                optimal_next_state = next_state

        if alpha >= beta:
            break

    score = alpha if is_max else beta
    return score, optimal_next_state


def main():
    try:
        print("Welcome to Mancala! \n")
        try:
            new_game = bool(int(input(
                "Do you want a new game or load a previous game? Type 1 for new game and 0 for loading a previous game. \n")))
        except:
            new_game = True

        global max_levels
        global steal
        first_turn = True

        if new_game:
            difficulty = int(
                input("Select a difficulty (0 -> easy , 1 -> medium, 2 -> hard): \n"))
            if difficulty == 0:
                pass
            elif difficulty == 1:
                max_levels = 7
            elif difficulty == 2:
                max_levels = 12
            else:
                print("Input is not understood. setting difficulty to easy \n")

            mode = int(
                input("Do you want steal mode? Type 1 for steal and 0 for no steal \n"))

            if mode:
                steal = True
            else:
                steal = False

            start_first = input(
                "Do you want to start first? Type 'yes' or 'no' \n")

            current_player = False

            # False -> AI, True -> Human
            if start_first == "yes":
                current_player = True

            state = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

            # state_tuple -> (state_array, is_final, another_turn)
            # at start no another turn and it is not a final move
            state_tuple = (state, False, False)

            score = state[13] - state[6]

        else:  # load game from a file
            file_name = input(
                "Please enter the save file name without '.json' \n")
            prev_game = load_previous_game(file_name)
            if prev_game:
                print("\n Sucessfuly loaded!! \n \n")
            state_tuple = (
                prev_game["state"], prev_game["is_final"], prev_game["another_turn"])
            max_levels = prev_game["max_levels"]
            steal = prev_game["steal"]
            score = prev_game["score"]
            current_player = prev_game["current_player"]

        current_state_tuple = state_tuple
        save_mode = input(
            "Do you want to be asked to save the game every turn? 'yes' or 'no'\n")
        while True:
            current_state, is_final, another_turn = current_state_tuple

            display_state(current_state)
            score = current_state[13] - current_state[6]

            if is_final:
                break

            if not first_turn and save_mode == "yes":
                save = input(
                    "Do you want to save the game state? Type 1 for saving and 0 for no saving \n")

                if save == "1":
                    save_name = input("Enter the save name: ")
                    state, is_final, another_turn = current_state_tuple
                    score = state[13] - state[6]
                    save_game(save_name, state, current_player, is_final,
                              another_turn, steal, max_levels, score)
                    print("\n\t\t\t\tGame saved.\n")
                elif save == "0":
                    print("\n\t\t\t\tContinue playing :)\n")
                else:
                    print("\n\t\t\tInvalid input! not saving..\n")

            if not current_player:
                print("\t\t\t\t\033[93m-> AI's turn!\033[0m\n")
                score, current_state_tuple = evaluate(current_state_tuple)
            else:
                print("\t\t\t\t\033[93m-> Your turn!\033[0m\n")
                bin_number = int(
                    input("Please select a bin to empty (Type a number from 1 to 6): ")) - 1
                while not (0 <= bin_number <= 5):
                    print("Enter a valid bin number! \n")
                    bin_number = int(
                        input("Please select a bin to empty (Type a number from 1 to 6): ")) - 1
                while True:
                    current_state_tuple = make_a_move(
                        current_state, bin_number, "user")
                    if len(current_state_tuple[0]) > 0:
                        break
                    else:
                        print("You chose an empty bin! \n")
                        bin_number = int(
                            input("Please select a bin to empty (Type a number from 1 to 6): ")) - 1
                        while not (0 <= bin_number <= 5):
                            print("Enter a valid bin number! \n")
                            bin_number = int(
                                input("Please select a bin to empty (Type a number from 1 to 6): ")) - 1

            first_turn = False
            if not current_state_tuple[2]:
                current_player = not current_player

        print("\n\t\t\t\t\033[93mGame Finished!\033[0m\n")
        if score > 0:
            print("\t\t\t\t\033[91mAI won!\033[0m\n")
        elif score == 0:
            print("\t\t\t\t\033[92mDraw!\033[0m\n")
        else:
            print("\t\t\t\t\033[94mYou won!\033[0m\n")

    except KeyboardInterrupt:
        print("\n\033[93mClosing...\033[0m")


main()