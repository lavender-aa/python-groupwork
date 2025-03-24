# Course Project
This project will be a game about a calculator inspired by [the password game](https://neal.fun/password-game/), and [balatro](https://store.steampowered.com/app/2379780/Balatro/).

## Rounds
The game will be round-based. Each round:
- There will be a target number that the player must attempt to reach via performing calculations.
- There will be a maximum number of button presses allowed
- There will be a number of random effects placed on the calculator.

As input, the player can enter at most a 2 digit number (excluding a negative sign). The target number may be any number of digits long.

At the beginning of each round, the player is given a random 1- or 2-digit number to work with. The result of each calculation is the first operand in the next. An example to illustrate:
- The player is given the value 9
- To calculate 18, the player hits "*2="
- To calculate 20, the player hits "+1="

## Scoring
This game will be an endless-runner style game. Each time a game starts, the player starts with 100 score. If the score reaches 0, the game ends and the high score is the number of rounds survived. As rounds continue, the punishments get bigger and the rewards smaller.

Things that increase score:
- Being close to the target
- Using very few button presses

Things that reduce score:
- Being far from the target
- Using too many button presses

## Random Effects
As rounds continue, more random effects are applied. The first round will have no effects, and the second will have 1 effect. After that, the number of effects will grow at a constant rate (1 more for every 5-10 rounds).

Some examples of what effects can look like:
- Can't use even buttons
- Multiplication button uses 10 score
- Addition only
- SADMEP (reverse order of operations)
- Strict PEMDAS (multiplication before division and addition before subtraction)
- Can only use equals button once
- No parentheses

Overlapping effects may cause the round to be very difficult or even impossible. As the game continues, luck playes a bigger and bigger part of surviving rounds.