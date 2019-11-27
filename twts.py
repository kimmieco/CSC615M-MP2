import re

# define constants
sr = "scan R"
sl = "scan L"
w1 = "write 1"
w2 = "write 2"
r1 = "read 1"
r2 = "read 2"
h = "halt"

# define classes
class State:
	def __init__(self, number, action):
		self.number = number
		self.action = action
		self.transitions = []

	def add_transition(self, input, next_state):
		self.transitions.append(Transition(input, next_state))

class Transition:
	def __init__(self, input, next_state):
		self.input = input
		self.next_state = next_state

class Stack:
	def __init__(self):
		self.is_empty = True
		self.used = False
		self.superscript = None
		self.symbol = None


'''
Creates a state in the PDA:

<curr_state>]<action>(<input>, <next_state>)
'''
def make_step(curr_state, action, input, next_state):
	state = State(curr_state, action)
	if(input is not None and next_state is not None):
		state.add_transition(input, next_state)
	return state

'''
Returns most recently added scan state in the program 
'''
def get_latest_scan_state(program):
	for state in reversed(program):
		#print(i)
		#state = program[i]
		if(state.action[0] == s):
			#print("Latest state: " + str(state.number))
			return state
	return None

def find_same_superscript(input_alphabet, superscript, start, dir):
	for i in range(dir, len(input_alphabet)):
		if(input_alphabet[i]['superscript'] == superscript):
			return input_alphabet[i]
	return None

def print_program(program):
	for state in program:
		line = str(state.number) + "]" + state.action
		for transition in state.transitions:
			next_state = transition.next_state
			line += "(" + transition.input + "," + str(next_state.number) + ")"
		print(line)

def push_stack(stack, superscript, symbol):
	stack.is_empty = False
	stack.used = True
	stack.superscript = superscript
	stack.symbol = symbol

def pop_stack(stack):
	stack.is_empty = True
	stack.superscript = None
	stack.symbol = None

def generate_program(input_alphabet):
	
	program = [] # Set of program instructions

	curr_state = 1 # Current state in the program

	# Instantiate stacks
	stack1 = Stack()
	stack2 = Stack()

	# Add first step in program
	state = make_step(curr_state, sr, None, None)
	curr_state += 1
	state.add_transition('#', state)
	next_state = State(curr_state, sr)
	curr_state += 1
	state.add_transition('#', next_state)
	program.append(state)

	# Iterate through every token in the language

	print_program(program)
	return program


if __name__ == "__main__":
	input_alphabet = []
	generate_program(input_alphabet)
