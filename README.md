# Guess-Game
Welcome to the NHL sports game. Please follow the instructions below on how to play this game.
Play the game by guessing NHL scores of 2021 teams and earn points.

This is a python guessing game that allows the player to earn points for each guess that is correct. Some guesses have two retries before points are awarded, only when there is a wrong selection. Then the player is allowed to play three rounds before the game is over. Then display the score. The maximum score is 9.

# Requirements
1.	Use a dataset to get data for the game. To be uploaded to s3
2.	Use a DynamoDB to store the game results.
3.	Use boto3 to make API calls

# Rules of the game
1. Select which team you think won the match. You can choose to answer a draw match. You earn 1 pt if correct and 0 otherwise.

2. Select the winning score. If you get both right, you earn 1 pt if you get it right and 0 if otherwise. You get another chance for this if the choice is incorrect with a new    set of choices.

3. You play three rounds and the game is over. Then you get to see your total game points. You can earn up to 6 points in this game.

4. HAVE FUN!!
