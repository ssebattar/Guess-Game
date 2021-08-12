import json
import random
import os
import boto3
import create_bucket as create
import delete_bucket as dlt
# from playsound import playsound


json_data = None
data_file = 'scores_nhl_2021_by_date_db.json'

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# Create S3 bucket to store a dataset
def create_s3_bucket():
    rand_4 = random.sample([*range(10)], 4)
    ls = ''
    for i in rand_4:
        ls += str(i )
    s3_bucket_name = "my-game-dataset-" + ls

    if s3.Bucket(s3_bucket_name).creation_date is None:
        bkt = create.create_bucket(s3_bucket_name)
    print(f'Creating {s3_bucket_name} bucket...')
    print(f'{s3_bucket_name} bucket has been created.')

    # Upload dataset file
    s3.Object(s3_bucket_name, data_file).upload_file(data_file)

# Create a dynamodb table to store game points
def create_table():
    table_name='Game'
    
    client = boto3.client('dynamodb')
    response = client.list_tables()
    if table_name in response['TableNames']:
        table_found = True
        return
    
    table = dynamodb.create_table (
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'GameID',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'GameID',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print(f"Creating {table_name} table...")
    table.wait_until_exists()
    return table

# Store game scores to db table
def store_game_score(table, score):
    table = dynamodb.Table('Game')
    
    rand_4 = random.sample([*range(10)], 4)
    GameID = 0
    for i in rand_4:
        GameID += i

    # put item in table
    table.put_item(
        Item={
            'GameID': GameID,
            'Score': score
        }
    ) 
        
    print(f"\n\nYour game score is stored in the databse")

# Read data file
def get_dataset(file):
    try:
        with open(file) as f:
            json_data = json.load(f)
    except FileNotFoundError:
        json.dumps({'Error': 'File not found!'})

    return json_data


# Global variables
data = get_dataset(data_file)
dates = []
for i in data.keys():
    dates.append(i)


# Instructions menu
def menu():
    print("""
        Welcome to the NHL sports game. Please follow the instructions
        below on how to play this game.

        1. Select which team you think won the match. You can choose to
           answer a draw match. You earn 1 pt if correct and 0 otherwise.

        2. Select the winning score. If you get both right, you earn 1 pt
           if you get it right and 0 if otherwise. You get another chance
           for this if the choice is incorrect with a new set of choices.

        3. You play three rounds and the game is over. Then you get to see
           your total game points. You can earn up to 6 points in this game.

        4. HAVE FUN!!
    """)


# Get sport matches and cards
def get_mathes():
    matches = []
    for i in range(len(data)):
        for j in data[dates[i]]:
            matches.append(j)

    return matches


# Game logic
def game_round():
    lm = '*'
    print(f'{lm*26}\n\tNew Round\n{lm*26}')
    matches = get_mathes()
    
    random_match = random.choice(matches)
    team1 = random_match['away_name']
    team2 = random_match['home_name']
    team1_score = random_match['away_score']
    team2_score = random_match['home_score']

    print(f'{team1} vs {team2} \n')
    print('Which team you think won this match? Choose')
    print(f'(1) for {team1}\n(2) for {team2}\n(3) for a draw.')

    choice = 0
    while True:
        try:
            choice = int(input())
            if choice in [1, 2, 3]:
                break
            print('Please enter a 1, 2 or 3')
        except Exception as e:
            print('Please enter a number')

    # eveluate input
    points = 0
    draw = False
    winner = None
    top_score = 0

    if team1_score == team2_score:
        draw = True
        top_score = team1_score
    elif team1_score > team2_score:
        winner = team1
        top_score = team1_score
    else:
        winner = team2
        top_score = team2_score

    if choice not in [1, 2] and draw == True:
        print('Nice guess! All teams made a draw in this match.')
        points += 1
    elif choice == 1 and winner == team1:
        print(f'Nice guess! {team1} won this match.')
        points += 1
    elif choice == 2 and winner == team2:
        print(f'Nice guess! {team2} won this match.')
        points += 1
    else:
        print(f'Not quite! But {winner} won this match.')
        

    print('\nSelect the top score for this match from these choices below.')

    # Get random score cards
    counter = 0
    for i in range(2):
        cards = set()
        rand_scores = [*range(10)] # * unpacks the range values
        cards.update(random.sample(rand_scores, 4))
        cards.add(top_score)

        # maintain 5 unique choices
        while len(cards) < 5:
            cards.update(random.sample(rand_scores, 1))

        for j in cards:
            print(f'|{j}| ', end="")
        print('\n')

        while True:
            try:
                sel = int(input())
                if sel in cards:
                    break
                print('Please select from the values given.')
            except Exception as e:
                print('Please enter a number')

        if sel == top_score:
            counter = 1
            points += 1

        # Allow another try if 
        if counter == 1:
            print('Good Job! ', end="")
            break
        elif i < 1:
            print('You did not get this right, try one more time.')
    print(f'The top score for this match was {top_score}')

    return points


# Game Entrance
def play_game():

    total_points = 0
    for i in range(3):
        total_points += game_round()

    print('Congratulations on finishing this game.\n')
    print(f'You have scored {total_points}.')
    # playsound(os.path.abspath('wow-congratulations.mp3'))
    
    return total_points

# Create aws resources
create_s3_bucket()
table = create_table()


while True:
    menu()
    total_points = play_game()
    store_game_score(table, total_points)
    cont = input("Do you want to continue? (Y or N):")
    while (cont.lower() not in ['y', 'n']):
        print("Please make a valid selection Y or N:")
        cont = input()
        
    if cont == 'n':
        print('\nThank you for trying this game.\n')
        break


