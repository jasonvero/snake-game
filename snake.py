import random
import curses

# initialize screen
s = curses.initscr()

# set cursor to 0 so it doesn't appear on screen
curses.curs_set(0)

# get width and height from x get max
sh, sw = s.getmaxyx()

# create new window using height, width, and starting at the top left hand corner of the screen
w = curses.newwin(sh, sw, 0, 0)

# accepts keypad input
w.keypad(1)

# refreshes screen every 100 milliseconds
w.timeout(100)

### create snake's initial position ###
# x is the middle of screen divided by 4
snk_x = sw//4

# y is the height of the screen divided by 2 (a little left of center)
snk_y = sh//2

# create initial snake body parts

snake = [
	# first snake body part is the y and then the x
	[snk_y, snk_x],
	# one left of the head
	[snk_y, snk_x-1],
	# two left of the head
	[snk_y, snk_x-2] 

]

### end - create snake's initial position ###

### create the food ###
# starting place for the food as the center of the screen
food = [sh//2, sw//2]
# add the food to the screen, and the food is going to be PI
w.addch(food[0], food[1], curses.ACS_PI)

### end - create the food ###

# need to tell the snake where he's going initially
key = curses.KEY_RIGHT

### start infinite loop for every movement of the snake ###
while True:
	# need to see what the next key is 
	next_key = w.getch()
	# this will then give us either nothing or the next key
	key = key if next_key == -1 else next_key

	# check to see if the person lost the game
	# if the y position is either at the top or at the height of the screen
	# or if the x position is either to the left or the width of the screen
	# or if your snake is in itself 
	if snake[0][0] in [0, sh] or snake [0][1] in [0, sw] or snake[0] in snake[1:]:
		# if any of above happens, kill the window and quit
		curses.endwin()
		quit()

	# determine what new head of snake is going to be
	# start by taking to old head of the snake as our starting point
	new_head = [snake[0][0], snake[0][1]]

	# we need to figure out what the actual key being clicked is
	# if key is being clicked down we need to take the y position and add 1 to it
	if key == curses.KEY_DOWN:
		new_head[0] += 1
	# if key is being clicked up we need to take the y position and go negative 1
	if key == curses.KEY_UP:
		new_head[0] -= 1
	# if key is being clicked left we need to take the x position and go negative 1
	if key == curses.KEY_LEFT:
		new_head[1] -= 1
	# if key is being clicked right we need to take the y position and add 1 to it
	if key == curses.KEY_RIGHT:
		new_head[1] += 1


	# diamond back snake
	w.addch(snake[0][0], snake[0][1], curses.ACS_DIAMOND)
	# insert new head of the snake
	snake.insert(0, new_head)

	# determining if the snake has ran into the food
	if snake[0] == food:
		food = None
		# if it's run into the food have to select a new piece of food
		while food is None:
		# new food location
			nf = [
				# height minus 1 to the height minus 1
				random.randint(1, sh-1),
				# 1 to the widght minus 1
				random.randint(1, sw-1)
			]
			# set food and check to see if none, it will redo this loop
			food = nf if nf not in snake else None
		# add that once the food has been selected
		w.addch(food[0], food[1], curses.ACS_PI)
	else:
		# get tail of the snake
		tail = snake.pop()
		# add a space in place of where the tail piece was
		w.addch(tail[0], tail[1], ' ')
	# add the head of the snake to the screen using ACS_CKBOARD)
	w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)