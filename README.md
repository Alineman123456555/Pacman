# Pacman
Pacman

Classes (Notes)

CliController?
Probably just have this logic in the Game class for now.

Game (Controller)
Has the main loop for the game (tick)
- Get input from cli (Controller)
    - Update the player direction obtained from controller
- Have every DynamicEntity in the World move
- Check the new game state (Game logic)
- Render World (Controller)
- Loop back to top

Stores World
Stores Controller?

enum Direction
- up
- down
- left
- right

World
Stores 2d array of list of entities (3d array)
Stores list of Dynamic Entities

Func get_surrounding_walls()
- Returns 4 things if a wall is up, down, left, right
or fun get_surroundings()?
that returns the entity list for the surroundings??

Is_valid_move()?
If true then move the character in the direction they were

move(direction: Direction, entity: DynamicEntity)
Moves an entitiy from one location to another
I guess it should use the direction stored in the Entity??


Entities
- Dynamic Entity
    - Player
    - Ghost
        - DumbGhost
        - Pinky
        - ...

- Static Entity
    - Wall
    - Interactible
        - Small Dot
        - Big Dot
        - Fruit?

Questions
I don't know where storing the direction makes the most sense.
If Ghosts need to know their last direction to make a choise about their next move, then ghosts need to store direction.
If there's no direction update for the player, then the player needs to continue moving in the same direction it was last game tick.



# Installing dependencies
Install pipenv
Run: `python3 -m pip install --user pipenv`

Install modules: `pipenv install`

