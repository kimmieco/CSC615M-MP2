s = "scan"
w = "write"
r = "read"

'''
Creates program step in format:

<curr_state>]<action>(<input>, <next_state>)
'''
def make_step(curr_state, action, input, next_state):
  return str(curr_state) + "] " + action + "(" + input + "," + str(next_state) + ")"

'''
Appends an additional (<input>, <next_state>) to a program step
'''
def add_to_step(step, input, next_state):
  step = step + "(" + input + "," + str(next_state) + ")"
  return step

def generate_program(input_alphabet):
  
  program = [] # Set of program instructions

  curr_state = 1 # Current state in the program

  step = make_step(curr_state, s, '#', curr_state)
  step = add_to_step(step, '#', curr_state+1)
  curr_state += 1 # Move to next state

  print(step)


if __name__ == "__main__":
	input_alphabet = []
	generate_program(input_alphabet)
