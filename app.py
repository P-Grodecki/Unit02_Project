import constants
import random
import copy


TEAMS = copy.deepcopy(constants.TEAMS)
PLAYERS = copy.deepcopy(constants.PLAYERS)


def clean_data(all_player_data):
    """
    Function Cleans the Player Data List Received from the constants file
    and exports a list of formatted player details.
    """
    # Initialize Dictionary of All Players
    player_list = []
    # Initialize ID Counter for players
    player_id = 0
    # Populate Dictionary of All Players
    for player in all_player_data:
        # initialize player_details dictionary
        player_details = {}
        # Establish a Player ID        
        player_details['id'] = player_id
        # Preserve Player Name
        player_details['name'] = player['name']
        # Clean up Guardian Data
        player_details['guardians'] = player['guardians'].split(' and ')
        # Clean up Experience Data
        if player['experience'].upper() == 'YES':
            player_details['experience'] = True
        elif player['experience'].upper() == 'NO':
            player_details['experience'] = False
        # Clean Up Height Data
        player_details['height'] = int(player['height'].split()[0])
        # Create a Details Dictionary about a Player
        player_list.append(player_details)
        # Increase the player_id counter
        player_id += 1
    return player_list


def balance_teams(teams, players):
    """
    Balance the threee teams based on:
        experience (equal number of experienced, not experienced players)
        & number of players must be equal for all teams.
    """
    # Create Copy of players to iterate through
    balance_players = []
    balance_players.extend(players)
    
    # Create Working Team Members List with an empty list for each team
    team_roster = []
    for team in teams:
        team_roster.append([])
    
    # Initialize the iteration counter
    iteration_counter = 0
    
    # While there remains players in the list
    while len(balance_players) > 0:
        # Iteratively Cycle through each of the teams,
        # adding either an experienced or inexperienced player each iteration.
        current_team_int = iteration_counter % len(teams)
        current_roster = team_roster[current_team_int]
        
        # Odd Iteration - Add Experienced Player
        if iteration_counter % 2 == 1:
            # Then we look for an Experienced Player to Add
            has_experience = True
        else:
            # Even Iteration - Add Inexperienced Player
            # Then we look for an inexperienced player
            has_experience = False
        # Find a candidate player that meets the experience requirements.
        player_added = False
        find_player_counter = 0
        while not player_added == True or find_player_counter == (len(balance_players) - 1):
            selected_player = random.randint(0, len(balance_players) - 1)
            if balance_players[selected_player]['experience'] == has_experience:
                current_roster.append(balance_players[selected_player]['id'])
                del balance_players[selected_player]
                player_added = True
            else:
                find_player_counter += 1
        # Increase the iteration count by 1
        iteration_counter += 1
    return team_roster    


def team_stats(selected_team, teams, rosters, players):
    """
    Given a team number, list of teams, list of team rosters, list of player info:
    Return a dictionary containing the required statistics of the team for presentation: 
        Number of players on teamConvert the team roster into whatever you want. 
    """
    team_num = selected_team - 1
    stats = {}
    # Team Name
    stats['Team Name: '] = teams[team_num]
    # Total number of players on team
    stats['Number of Players: '] = len(rosters[team_num])
    # The player names of that team in a single string
    player_names = []
    experienced_players = []
    inexperienced_players = []
    player_heights = []
    player_guardians = []
    for player_id in rosters[team_num]:
        player_names.append(players[player_id]['name'])
        player_heights.append(players[player_id]['height'])
        player_guardians.append(", ".join(players[player_id]['guardians']))
        if players[player_id]['experience'] == True:
            experienced_players.append(players[player_id]['experience'])
        else:
            inexperienced_players.append(players[player_id]['experience'])
    stats['Player Names: '] = ", ".join(player_names)
    # The total number of inexperienced players
    stats['Inexperienced Players Total: '] = len(inexperienced_players)
    # The total number of experienced players
    stats['Experienced Players Total: '] = len(experienced_players)
    # Average height of the team
    stats['Average Player Height: '] = str(round(sum(player_heights)/len(player_heights),1)) + " inches"
    # List of team guardians joined as comma separated string.
    stats['Guardian Names: '] = ", ".join(player_guardians)
    return stats
    

def display_team_stats(team_stats):
    """
    Print out the Dictionary of Team Stats
    """
    print('\n' + '-' * 5 + " Team Statistics " + '-' * 5)
    for label, stat in team_stats.items():    
        if len(label + str(stat)) < 70:
            print(f'{label}{stat}')
        else:
            print(f'{label}\n\t{stat}')
        if label == 'Team Name: ':
            print('-' * 27)
        

def user_entry_allowable_list_string(title_string, 
                                     instruction_string,
                                     choices_list,
                                     label_list,
                                     prompt_string,
                                     error_entry_string
                                    ):
    """
    Display the title string and instruction string,
    present the lists of labels / corresponding choices,
    (The label list and choice lists MUST consist of all strings.)
    prompt the user for input and perform continuous loop until
    user enters an option which is in the list, displaying
    the error_entry_string each time there is an incorrect input.
    """
    if title_string != '':
        print(title_string + "\n")
    correct_entry = False
    while not correct_entry:
        print(instruction_string)
        for row in range(0,len(choices_list)):
            print(f'   {choices_list[row]} - {label_list[row]}')
        print()
        user_choice = input(prompt_string)    
        if user_choice in choices_list:
            correct_entry = True
            return user_choice
            break
        else:
            print(error_entry_string)
        
        
if __name__ == '__main__':
    # Print Title
    print("\nBASKETBALL TEAM STATS TOOL")
    first_loop_rebalance_teams = True
    while True:
        # Prompt User to either display the team stats or quit
        user_choice = user_entry_allowable_list_string(
            title_string = '\n' + '-'*5 + 'MENU' + '-'*5, 
            instruction_string = "Please select from the following choices:", 
            choices_list = ['1','2'], 
            label_list = ["Display Team Stats", "Quit"],
            prompt_string = "Enter an option from above >  ", 
            error_entry_string = 'Invalid Responce. Please select a value from the list (1, 2) Try again.\n'
        )
        if user_choice == '2': # User elected to quit the program
            break
        # Otherwise, user elected to see the team stats.
        if first_loop_rebalance_teams:
            # Clean the player data that has been obtained from the constants file.
            clean_players = clean_data(PLAYERS)
            # Establish the team rosters
            rosters = balance_teams(TEAMS, clean_players)            
        # Create the choice list for the user
        choice_values = []
        for build_choice_value in range(0,len(TEAMS)):
            choice_values.append(str(build_choice_value+1))
        # User shall select a team from a list
        user_team_choice = user_entry_allowable_list_string(
            title_string = '', 
            instruction_string = "\nPlease select a team from the following choices:", 
            choices_list = choice_values, 
            label_list = TEAMS,
            prompt_string = "Enter the number of a team from above >  ", 
            error_entry_string = "Please select a value from the list. Try again."
        )
        user_team_choice = int(user_team_choice)
        # Compile the statistics for the selected team
        the_stats = team_stats(user_team_choice, TEAMS, rosters, clean_players)
        # Display the statistics for the selected team
        display_team_stats(the_stats)
        input('\nPress ENTER to Continue....')
        first_loop_rebalance_teams = True
    print("\nYou have exited the basketball stats program. Thank you.")
