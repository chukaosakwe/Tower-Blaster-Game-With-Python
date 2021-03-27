
import random

def setup_bricks():
    """Creates a main pile of 60 bricks, represented as a list containing the integers 1 – 60.
    Creates a discard pile of 0 bricks, represented as an empty list.
    Returns both lists."""
    main_pile = [] # stores main pile bricks
    #stores 60 numbers in the main pile
    for i in range(1,61):
        main_pile.append(i)
    discard_pile=[] #stores discard pile bricks
    return (main_pile,discard_pile)

def shuffle_bricks(bricks):
    """Shuffle the given bricks (represented as a list). (You’ll do this to start the game.)
    This function does not return anything."""
    random.shuffle(bricks)

def check_bricks(main_pile,discard):
    """Check if there are any cards left in the given main pile of bricks.
    If not, shuffle the discard pile (using the shuffle function) and move those bricks to the
    main pile.
    Then turn over the top card to be the start of the new discard pile."""
    # if the main pile is empty, shuffle the discard pile and add it to the main pile
    if (main_pile == []):
        shuffle_bricks(discard)
        for i in range(0,len(discard)):
            main_pile.append(discard[i])
        #empty the discard pile
        discard.clear()
        # turn over top card to be start of new discard pile
        discard.append(get_top_brick(main_pile))

def check_tower_blaster(tower):
    """Given a tower (the user’s or the computer’s list), determine if stability has been
    achieved.
    This function returns a boolean value."""
    # checks if tower is stable (elements are in increasing order from left to right)
    for i in range(1,len(tower)):
        if (tower[i]<tower[i-1]):
            return False
    return True

def get_top_brick(brick_pile):
    """Removes and returns the top brick from any given pile of bricks. This can be the main_pile,
    the discard pile, or your tower or the computer's tower. It removes and returns the
    first element of any given list. """
    return brick_pile.pop(0)

def deal_initial_bricks(main_pile):
    """Starts the game by dealing two sets of 10 bricks each, from the given main_pile.
    Returns a tuple with the computers hand and the users hand as lists"""
    users_hand=[] # stores the users pile of bricks
    computers_hand=[] # stores the computers pile of bricks
    for i in range(1,11):
        # deal the computers brick
        computers_hand.insert(0,get_top_brick(main_pile))
        # deal the users brick
        users_hand.insert(0,get_top_brick(main_pile))
    return (computers_hand,users_hand)

def add_brick_to_discard(brick,discard):
    """Adds the given brick (represented as an integer) to the top of the given discard pile
    (which is a list). This function does not return anything."""
    discard.insert(0,brick)

def find_and_replace(new_brick, brick_to_be_replaced,tower,discard):
    """Find the given brick to be replaced (represented by an integer) in the given tower and
    replace it with the given new brick.
    Return True if the given brick is replaced, otherwise return False"""
    try:
        index_to_replace= tower.index(brick_to_be_replaced)
        tower[index_to_replace] = new_brick
        discard.insert(0,brick_to_be_replaced)
        return True
    except Exception:
        return False

def find_and_replace_ask_user_input(new_brick,tower,discard,message):
    """Finds and replaces the given brick based on user input.
    Ensures the user inputs a valid brick. Doesn't return anything"""
    while (True):
        try:
            brick_to_be_replaced = int(input(message))
            if (find_and_replace(new_brick, brick_to_be_replaced,tower,discard) == True):
                print("You have replaced brick " + str(brick_to_be_replaced) + " with " +str(new_brick))
                print("Your brick tower: "+str(tower))
                return
            else:
                continue
        except:
            continue

def computer_play(tower,main_pile,discard):
    """Defines and runs the computer's strategy.
    Strategy overview: place each brick into its 'correct' position in the tower.
    i.e. any brick between 1-6 inclusive goes in index 0, 7-12 in index 1, 13-8 in index 2,
     19-24 in index 3, 25-30 in index 4, 31 to 36 in index 5, 37 to 42 in index 6,
     43 to 48 in index 7, 49 to 54 in index 8 and 55 to 60 in index 9.

     1. check the 'correct' position for the brick as defined above.
     2. check the brick that is already in that position in the tower. Is that brick where
     it should be?
     3. If yes, then pick from mystery pile. If no, then replace that brick.
     4. If the computer picks from the mystery pile, it checks the 'correct' position for it and places
     that brick in that position in the tower

    Returns the computer's tower."""

    print("--------COMPTUER'S TURN--------")

    # initial new brick
    new_brick = get_top_brick(discard)

    # where the computer is considering placing the new brick. The formula finds the correct position for this brick
    new_brick_position = (new_brick-1) // 6

    # computer looks at the brick currently in the position it may want to place the new brick
    old_brick_in_intended_position = tower[new_brick_position]

    # what is the correct position for the brick in the tower the computer is considering replacing?
    correct_position_for_old_brick = (old_brick_in_intended_position-1)//6

    # if the old brick is where it should be then pick from the mystery pile
    if (correct_position_for_old_brick == new_brick_position):
        # if old brick is already in correct position, then use the mystery pile.
        new_brick = get_top_brick(main_pile)

        #print computer action
        print("The computer picked "+ str(new_brick) + " from the mystery pile")

        # find the position for this new brick from the main pile
        new_brick_position = (new_brick-1) // 6

        # use this new brick
        brick_to_be_replaced = tower[new_brick_position]
        find_and_replace(new_brick,brick_to_be_replaced,tower,discard)

        #print actions
        print("The computer swapped "+ str(new_brick) + " for " + str(brick_to_be_replaced))
    else:
        #print computer action
        print("The computer picked "+ str(new_brick) + " from the discard pile")

        # brick in tower is not where it should be so replace it with this new brick
        brick_to_be_replaced = old_brick_in_intended_position
        find_and_replace(new_brick,brick_to_be_replaced,tower,discard)
        print("the computer swapped "+ str(new_brick) + " for " + str(old_brick_in_intended_position))
    return tower

def ask_user_input(required_input_1,required_input_2, message):
    """Asks the user for one of two inputs. Repeats the message until a valid response is given.
    Returns the user's input."""

    #stores the message input
    message_stored = (input(message)).lower()

    #ensures the human enters a valid input
    while True:
        if message_stored ==required_input_1 or message_stored ==required_input_2:
            break
        else:
            message_stored = (input(message)).lower()
    return message_stored

def human_play(tower, main_pile, discard):
    """Displays and effects the human player's actions. Doesn't return anything"""

    print("--------YOUR TURN--------")
    #print interim results of the game
    print_results("Mystery pile is hidden",discard[0],tower)

    # ask if user wants to pick from main/mystery pile or discard pile
    pick = ask_user_input("m","d","Pick which pile to draw a brick from. m for 'mystery pile', d for 'discard pile")

    # the user picked main/mystery pile
    if (pick == "m"):
        # retrieve the top brick from main pile
        new_brick = get_top_brick(main_pile)

        # interim results for user
        print_results(new_brick,discard[0],tower)

        # asks the user to use this brick or discard it
        use= ask_user_input("u","d","You have chosen to use from the mystery pile and cannot use from the discard pile anymore. Type 'u' to use this brick ("
                            + str(new_brick) + ") or 'd' to discard and skip your turn.")

        # if you use this brick, choose where to place the brick
        if(use == "u"):
            # finds and replaces a valid brick
            find_and_replace_ask_user_input(new_brick,tower,discard,"Specify which of the bricks in your tower to remove. Must be a valid integer")

        # if you discard, place the card into the discard pile and skip your turn
        if(use == "d"):
            discard.insert(0,new_brick)
            print("You have discarded the card and skipped your turn")
            return
    # user has chosen to use the discard pile and now must place it in discard pile
    if(pick == "d"):
        new_brick = get_top_brick(discard)
        # finds and replaces a valid brick
        find_and_replace_ask_user_input(new_brick,tower,discard,"Specify which of the bricks in your tower to remove. Must be a valid integer")
    return

def print_instructions():
    """Prints the instructions for the game."""
    print("Game Instructions:")
    print("The game starts with a main pile of 60 bricks, each numbered from 1 to 60")
    print("The first player to arrange 10 bricks in your own tower from lowest to highest wins")
    print("In this game, the left most integer in your list is the top of the tower")
    print("The right most integer in your list is the bottom of the tower")

def print_results(main_pile_show,discard_pile_show, humans_hand):
    """Prints the interim results of the game for the human"""
    print("Your brick tower: "+str(humans_hand))
    print("Top of discard pile: " + str(discard_pile_show))
    print("Top of mystery pile: " + str(main_pile_show))
    print("-----------------------")


def print_final_results(winner,humans_hand,computers_hand):
    """Prints the winner and the towers of both computer and user after the game is over"""
    print("-----------------------")
    print("GAME OVER")
    # print the winner
    if (winner=="computer"):
        print("You lost :( ")
    else:
        print("You won!")
    # print computer and user hands
    print("Your brick tower: "+str(humans_hand))
    print("Computer's brick tower: "+str(computers_hand))
    return

def main():
    """Runs the game"""
    #initialize the game
    print_instructions()
    (main_pile,discard_pile) = setup_bricks()
    shuffle_bricks(main_pile)
    # deal the players bricks
    (computers_hand,humans_hand)=deal_initial_bricks(main_pile)
    print("-----------------------")
    print("The computer's starting brick tower: "+str(computers_hand))
    print("Your starting brick tower: "+str(humans_hand))
    #take top brick in main pile and add it to discard pile
    add_brick_to_discard(get_top_brick(main_pile),discard_pile)
    #computer plays first
    game_over = False # tracks whether the game is over
    while(game_over==False):
        #computer plays first
        computer_play(computers_hand,main_pile,discard_pile)

        #check if game is over after computer plays
        game_over=check_tower_blaster(computers_hand)
        if (game_over == True):
            winner = "computer"
            break

        # reshuffle bricks if necessary
        check_bricks(main_pile,discard_pile)

        #human plays next
        human_play(humans_hand, main_pile,discard_pile)

        #check if game is over after human plays
        game_over=check_tower_blaster(humans_hand)
        if (game_over == True):
            winner = "human"
            break

        # reshuffle bricks if necessary
        check_bricks(main_pile,discard_pile)


    # game is over. print final results.
    print_final_results(winner, humans_hand, computers_hand)
    return

if __name__ == "__main__":
    main()