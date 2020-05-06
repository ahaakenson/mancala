####################################################                       
# Mancala with Two Players                         #
# Asks user for number of seeds and rounds.        #
# Then simulates games of mancala with             #
# one player choosing randomly the starting        #
# house and the other making strategic decisions.  #
#                                                  #
# Creates two files reporting what is happening    #
# during single play and statistics for multi play #
####################################################

import copy
import statistics
from random import randrange
import random

def create_board(houses, seeds):
    ''' Input: 2 integers: number of houses on board
        and number of seeds in each house
        Creates a list with each element in list representing a house on board.
        Return: a list representing board'''
    new_board = [seeds]*houses
    return new_board

def player_move(board_own, board_opp, score_own, score_opp, house):
    ''' Input: two lists representing both sides of the board, both scores(int)
        and selected house to begin turn from(int).
        
        Function empties the starting house and puts the seeds into a variable.
        The player's board is iterated through until the scoring house is 
        reached or the number of seeds in hand is 0.
        If the end of the first player's board is reached, then the function
        iterates through the other player's board.
        An additional turn is added if the last seed is placed in own scoring
        house.
        If the last house sowed was on own side and empty, the seeds are scored
        
        Return: both board lists, both scores, and if an additional turn was
        granted.
    '''
    
    carried_seeds = board_own[house]
    board_own[house] = 0
    index = house + 1
    board = 'own'
    add_turn = False
    while carried_seeds > 0:
        if board == 'own':    
            # adds to score if index is at the scoring plot
            if index == 6:
                score_own += 1
                board = 'opp'
                index = -1
                # if last seed in hand is scored, additional turn granted
                if carried_seeds == 1:
                    add_turn = True
            else:
                board_own[index] += 1
        elif board == 'opp':
            if index == 6:
                score_opp += 1
                board = 'own'
                index = -1
            else:
                board_opp[index] += 1
        # shifts one house to the right and subtracts one seed from hand
        index += 1 
        carried_seeds -= 1
    # if last seed is put in empty plot on own side, player captures the seed
    if board == 'own':
        # ignores empty capture if last seed went into store
        if index != 0:
            index -= 1
        if board_own[index] == 1:
            # captures opponent's seeds across the board
            score_own += board_own[index] + board_opp[5-index]
            board_own[index] = board_opp[5-index] = 0
    return board_own, board_opp, score_own, score_opp, add_turn

def check_win(board1, board2):
    ''' Input: both sides of board (list)
        
        The function iterates through both lists and if either one contains
        only houses with 0 seeds, returns win condition is True
        If neither returns True, the function returns False
        
        Return: whether win condition is true or false (bool)
    '''
    zeros = 0
    # iterates through each house to check if it has 0 seeds
    for house in board1:
        if house == 0:
            zeros += 1
    # if all of the houses had no seeds, win condition is True
    if zeros == 6:
        return True
    
    zeros = 0
    # iterates through other side of board to check how many houses are emtpy
    for house in board2:
        if house == 0:
            zeros += 1
    # returns win condition is true if all houses had no seeds
    if zeros == 6:
        return True
    
    # returns win condition is false if neither board returned true
    return False
    

def rand_player_move(board_own):
    ''' Input: player's own side of the board (list)
        
        Function generates a random number for house to sow. If house is
        empty, another number is generated until a non empty house is chosen
        
        Return: random player's house to start turn on (int)
    '''
    if board_own == [0,0,0,0,0,0]:
        return -1
    # generates random number from 0-5 representing house index on own side
    house = randrange(6)
    # checks if house at the random index is empty
    while board_own[house] == 0:
        house = randrange(6)
    return house

def strat_player_move(board_own):
    ''' Input: own side of board (list)
        
        Iterates through each house and tests whether player would gain an
        additional turn if it started at that house.
        If no additional turn selections are possible, iterates through each
        house again until it reaches closest house to store with seeds in it
        
        Return: strategic player selection (int)
    '''
    # iterates through board in reverse order (closest to store first)
    for house in range(5,-1,-1):
        # deepcopies board so the original doesn't change
        copied_board = copy.deepcopy(board_own)
        # creates a board since the opponent's board doesn't matter
        arbitrary_board = [0,0,0,0,0,0]
        # tests each house as starting point to see if it grants an extra turn
        exp_board, exp_board1, score0, score1, add_turn = \
        player_move(copied_board, arbitrary_board, 0, 0, house)
        if add_turn == True:
            return house
    # if no moves give player extra turn, iterates through board again
    for house in range(5,-1,-1):
        # finds closest house to store with seeds in it
        if board_own[house] != 0:
            return house
def print_results(strat_board, rand_board, turn, rand_score, strat_score, \
                  prev_rand_score, prev_strat_score, move, add_move, file):
    '''Input: both boards in list format, whose turn it is, both scores, both
    previous scores, starting house, whether player got an extra turn, and 
    file pointer
    
    Writes turn summary to a file input into the function.
    
    Output: None'''
    
    house = move+1
    # reverses one of the boards like it would be on an actual board
    strat_board_rev = strat_board[::-1]
    # finds out whose turn it is for when it is printed
    if turn == 'strat':
        player = 'StratPlayer'
    else:
        player = 'RandPlayer'
    file.write("It was {:s}'s turn\n".format(player))
    file.write("{:s} picked up seeds from house number {:d} (1-6 possible, " \
               "with 6 being closest to each player's store and top board"\
               "is in reverse order)\n".format(player, house))
    # prints out current board with top board reversed
    file.write('\nCurrent Board:\n')
    file.write('{:15s} |{:d}|{:d}|{:d}|{:d}|{:d}|{:d}|\n'.format(\
               'House number:', 6, 5, 4, 3, 2, 1))
    file.write('{:15s}|{:d}|{:d}|{:d}|{:d}|{:d}|{:d}|\n'.format\
               ('Strategy Player:', *strat_board_rev))
    file.write('{:16s}|{:d}|{:d}|{:d}|{:d}|{:d}|{:d}| \n'.format\
          ('Random Player:', *rand_board))
    file.write('{:15s} |{:d}|{:d}|{:d}|{:d}|{:d}|{:d}|\n\n'.format(\
               'House number:', 1, 2, 3, 4, 5, 6))
    
    file.write('RandPlayer score: {:d}\n'.format(rand_score))
    file.write('StratPlayer score: {:d}\n'.format(strat_score))

    file.write('Additional move: {:}\n'.format(add_move))
    
    file.write('StratPlayer score change: {:d} -> {:d}\n'.format\
               (prev_strat_score, strat_score))
    file.write('RandPlayer score change: {:d} -> {:d}\n'.format\
               (prev_rand_score, rand_score))  
    file.write('----------------------------------\n')

def roll_turn():
    '''Input: None
    
    Generates a random number to decide which player goes first for multi play
    
    Output: Whose turn it is (string)'''
    # generates random number 0 or 1
    turn = randrange(2)
    # returns whether it's StratPlayer or RandPlayer's turn
    if turn == 0:
        return 'strat'
    else:
        return 'rand'
 
def single_play(seed):
    '''Input: Number of seeds in each house
    
    Creates boards based on seeds, and plays out a single game 
    Writes a summary of each turn to a file
    
    Output: None
    '''
    sp = open('single_play.txt', 'w') #opens output file to write game info
    
    # creates both boards with 4 seeds
    rand_board = create_board(6, 4)
    strat_board = create_board(6, 4)
    
    # seeds random player
    random.seed(seed)
    
    rand_score = strat_score = prev_rand_score = prev_strat_score = 0
    
    # StratPlayer starts game
    player = 'strat'
    # loops until check_win is True, meaning someone has met win conditions
    while check_win(rand_board, strat_board) == False:
        if player == 'strat':
            move = strat_player_move(strat_board)
            strat_board, rand_board, strat_score, rand_score, add_turn = \
            player_move(strat_board, rand_board, strat_score, rand_score, move)
            
            print_results(strat_board, rand_board, player, rand_score, \
                          strat_score, prev_rand_score, prev_strat_score, \
                          move, add_turn, sp)
            # switches to other player if no extra turn granted. Otherwise, 
            # Stratplayer makes another move in next iteration of loop
            if add_turn == False:
                player = 'rand'

            prev_rand_score = rand_score
            prev_strat_score = strat_score
  
        elif player == 'rand':
            move = rand_player_move(rand_board)
            
            rand_board, strat_board, rand_score, strat_score, add_turn = \
            player_move(rand_board, strat_board, rand_score, strat_score, move)
            
            print_results(strat_board, rand_board, player, rand_score, \
                          strat_score, prev_rand_score, prev_strat_score, \
                          move, add_turn, sp)
            prev_rand_score = rand_score
            prev_strat_score = strat_score
            # switches to StratPlayer if no extra turn granted
            # RandPlayer will make another move on next loop cyle otherwise
            if add_turn == False:
                player = 'strat'

    if strat_score > rand_score:
        sp.write('StratPlayer won!\n')
    else:
        sp.write('RandPlayer won!\n')

    sp.write('Final scores: \n')
    sp.write('Strategy Player: {:d}\n'.format(strat_score))
    sp.write('Random Player: {:d}'.format(rand_score))
    
    sp.close()
def multi_play(rounds):
    '''Input: Number of rounds (int)
    
    Plays as many rounds as input into function.  Each round starts with a new
    board, and RandomPlayer seeded with the round number.   Opens 
    'multiple_play.txt' file and records game statistics on file.
    
    Return: None
    
    '''
    rand_score_list = []
    strat_score_list = []
    strat_add_moves = 0
    rand_add_moves = 0
    
    mp = open('multiple_play.txt', 'w')
    # loops games for how many rounds were inputted
    for n in range(1, rounds+1):
        # seeds random player with round number
        random.seed(n)
        # creates boards with 4 seeds
        rand_board = create_board(6,4)
        strat_board = create_board(6,4)

        rand_score = strat_score = 0

        # rolls for who goes first
        player = roll_turn()
        # plays game until someone meets win conditions
        while check_win(strat_board, rand_board) == False:
            if player == 'strat':
                move = strat_player_move(strat_board)

                strat_board, rand_board, strat_score, rand_score, add_turn = \
                player_move(strat_board, rand_board, strat_score, rand_score,\
                            move)
                # switches to rand player if no extra turn
                if add_turn == False:
                    player = 'rand'
                # adds 1 to additional turn statistic if player got one
                elif add_turn == True:
                    strat_add_moves += 1
                
            elif player == 'rand':
                move = rand_player_move(rand_board)
                # carries out move
                rand_board, strat_board, rand_score, strat_score, add_turn = \
                player_move(rand_board, strat_board, rand_score, strat_score,\
                            move)
                # switches to strat player if no extra turn
                if add_turn == False:
                    player = 'strat'
                # adds 1 to additional turn statistic if player got one
                elif add_turn == True:
                    rand_add_moves += 1
        # appends both scores to player's respective score list
        else:
            rand_score_list.append(rand_score)
            strat_score_list.append(strat_score)

    both_score_list = rand_score_list + strat_score_list
    
    # calculates all of the game statistics
    num_rounds = len(rand_score_list)
    avg_both = sum(both_score_list) / (num_rounds *2)
    avg_rand = sum(rand_score_list) / num_rounds
    avg_strat = sum(strat_score_list) / num_rounds
    
    med_both = statistics.median(both_score_list)
    med_rand = statistics.median(rand_score_list)
    med_strat = statistics.median(strat_score_list)
    
    min_strat = min(strat_score_list)
    min_rand = min(rand_score_list)
    max_strat = max(strat_score_list)
    max_rand = max(rand_score_list)
    
    HEADERS = ['Player', 'Average Score', 'Median Score', 'Minimum Score', \
               'Maximum Score', 'Extra Moves']
    
    mp.write('Number of rounds played: {:d}\n'.format(num_rounds))
    mp.write('{:<10s}{:<17s}{:<16s}{:<17s}{:<17s}{:<15s}\n'.format(*HEADERS))
    mp.write('{:<10s}{:<17.2f}{:<16.1f}{:<17d}{:<17d}{:<15d}\n'.format(\
             'Random', avg_rand, med_rand, min_rand, max_rand, rand_add_moves))
    mp.write('{:<10s}{:<17.2f}{:<16.1f}{:<17d}{:<17d}{:<15d}\n'.format(\
             'Strat', avg_strat, med_strat, min_strat, max_strat, \
             strat_add_moves))
    mp.write('{:<10s}{:<17.2f}{:<16.1f}\n'.format('Both', avg_both, med_both))

    mp.close()
def main():
    ''' Input: None
    
    Asks user for number of seeds for single play and rounds for multiple play.
    Runs single play and multi play with inputted information
    
    Return: None'''
    success = False
    # loops until valid integer given
    while success == False:
        seed = input('RandomPlayer seed: ')
        try:
            seed = int(seed)
            success = True
        # prints out error message if input isn't an integer
        except ValueError:
            print('Error. Please input an integer.')
    success = False
    # loops until valid integer given
    while success == False:
        rounds = input('Number of rounds in multi-round: ')
        # tries to turn inputted value into an integer
        try:
            rounds = int(rounds)
            success = True
        # prints out error message if input isn't an integer
        except ValueError:
            print('Error. Please input an integer.')
    single_play(seed)
    multi_play(rounds)
    
if __name__ == '__main__':
    main()