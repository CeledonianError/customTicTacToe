from tkinter import *
from tkinter import messagebox
from functools import partial
from copy import deepcopy

board = []
turn = True # True = x, False = o

def update(window):
	for widget in window.grid_slaves(): # Delete old tiles
		widget.destroy()
	for row in range(len(board)): # Generate visual board
		for col in range(len(board[row])):
			tile = Button(window, text = board[row][col],\
						command=partial(playerMove, row, col, board, window), 
						relief = "flat",
						bg = "#112233", fg = "#FFFFFF",
						activebackground = "#223344",
						activeforeground = "#FFFFFF",
						highlightbackground = "#556677",
						font = ("Monospace", 17))
			tile.grid(row = row, column = col)
	atkinson = ("Atkinson Hyperlegible", 12)
	if turn:
		turnLbl = Label(text="Current turn: x", font = atkinson,\
						bg = "#112233", fg="#FFFFFF")
	else:
		turnLbl = Label(text="Current turn: o", font = atkinson,\
						bg = "#112233", fg="#FFFFFF")
	turnLbl.grid(row = len(board), column = 0,\
				rowspan = len(board), columnspan = len(board))

def checkWin(board, player):
	# Check rows
	for checkRow in range(len(board)):
		if all(i == player for i in board[checkRow]):
			return True
	# Check columns
	for row in range(len(board)):
		checkColList = []
		for checkCol in range(len(board[row])):
			checkColList.append(board[checkCol][row])
		if all(j == player for j in checkColList):
			return True
	# Check diagonals
	# Top left to bottom right
	checkDiagList = [] 
	for checkDiag in range(len(board)):
		if board[checkDiag][checkDiag] == player:
			checkDiagList.append(True)
		else:
			checkDiagList.append(False)
	if all(checkDiagList):
		return True
	# Top right to bottom left
	checkDiagList = [] 
	refDict = {} 
	# Make a dict of ascending:descending values: 0:4, 1:3, 2:2, etc.
	for n in range(len(board)):
		refDict[[i for i in range(len(board))][n]] = \
				[j for j in range(len(board) - 1, -1, -1)][n]
	for key in refDict: # Oh my god I love dictionaries
		if board[key][refDict[key]] == player:
			checkDiagList.append(True)
		else:
			checkDiagList.append(False)
	if all(checkDiagList):
		return True

def playerMove(row, col, board, window):
	global turn
	atkinson = ("Atkinson Hyperlegible", 12)
	if turn and board[row][col] == " ":
		board[row][col] = "𝖷"
		turn = not turn
	elif not turn and board[row][col] == " ":
		board[row][col] = "◯"
		turn = not turn

	if checkWin(board, "𝖷") == True:
		update(window)
		prompt = messagebox.askyesno(title="Win", message="x has won!\n Go again?")
		if prompt:
			for widget in window.grid_slaves(): # Delete old tiles
				widget.destroy()
			start(window)
		else:
			window.destroy()
		return None
	elif checkWin(board, "◯") == True:
		update(window)
		prompt = messagebox.askyesno(title="Win", message="o has won!\n Go again?")
		if prompt:
			for widget in window.grid_slaves(): # Delete old tiles
				widget.destroy()
			start(window)
		else:
			window.destroy()
		return None
	else: # Check for a tie
		tieList = []
		for rowCheck in range(len(board)):
			if not any(tile == " " for tile in board[rowCheck]):
				tieList.append(True)
			else:
				tieList.append(False)
		if all(tieList):
			update(window)
			prompt = messagebox.askyesno(title="Tie", message="It's a tie!\n Go again?")
			if prompt:
				for widget in window.grid_slaves(): # Delete old tiles
					widget.destroy()
				start(window)
			else:
				window.destroy()
			return None
	update(window)

def start(window):
	global board
	board = []

	def getSize():
		global board
		try:
			size = int(sizeEntry.get())
			sizeEntry.delete(0, "end")
			if 3 <= size and size <= 10:
				board = [[" "] * size for _ in range(size)]
				update(window)
				return None
			else:
				sizeEntry.delete(0, "end")
				instruction.configure(text="Invalid input! Size must be minimum 3, maximum 10")
		except ValueError:
			instruction.configure(text="Invalid input! Size can only be an integer.")

	atkinson = ("Atkinson Hyperlegible", 12)

	title = Label(text="Welcome to Tic Tac Toe!", font = ("Atkinson Hyperlegible",\
				15, "bold"), fg="white", bg="#112233")
	title.grid()
	enterLabel = Label(text="Please enter the size of board you would like to play on.",\
				font = atkinson, fg = "white", bg="#112233")
	enterLabel.grid()
	instruction = Label(text="Size must be minimum 3, maximum 10",\
					font = atkinson, fg="white", bg="#112233")
	instruction.grid()

	sizeEntry = Entry(window, width = 10)
	sizeEntry.grid()
	sizeEntry.focus()
	enterBtn = Button(window, text="Ok", command=getSize)
	enterBtn.grid()

def main():
	window = Tk()
	window.title("Tic Tac Toe")
	window.configure(bg="#112233")
	window.resizable(False, False)

	start(window)

	window.mainloop()

if __name__ == "__main__":
	main()
