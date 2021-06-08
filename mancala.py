state = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 5]
state2 = [13, 2, 3, 0, 0, 0, 0, 5, 1, 7, 3, 1, 6, 0]

mirror = {0: 12, 1: 11, 2: 10, 3: 9, 4: 8, 5: 7}
steal = True


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


# print(check_for_final(state))
# display_state(make_a_move(state2,0,"user")[0])