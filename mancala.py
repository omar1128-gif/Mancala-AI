state = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 5]
state2 = [13, 2, 3, 0, 0, 0, 0, 5, 1, 7, 3, 1, 6, 0]


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


print(check_for_final(state))
display_state(state2)
