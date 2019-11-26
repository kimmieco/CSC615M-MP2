import re

s = "scan"
w = "write"
r = "read"
h = "halt"


class State:
  def __init__(self, number, action):
    self.number = number
    self.action = action
    self.transitions = []

  def add_transition(self,input, next_state):
    self.transitions.append(Transition(input, next_state))

class Transition:
  def __init__(self, input, next_state):
    self.input = input
    self.next_state = next_state

class Stack:
  def __init__(self):
    self.is_empty = False
    self.superscript = None
    self.token = None

'''
Creates program step in format:

<curr_state>]<action>(<input>, <next_state>)
'''
def make_step(curr_state, act, input, next_state):
  state = State(curr_state,act)
  if(input is not None or next_state is not None):
    state.add_transition(input, next_state)
  return state
  #return str(curr_state) + "] " + act + "(" + input + "," + str(next_state) + ")"

'''
Returns most recently added scan state in the program 
'''
def get_latest_scan_state(program):
  for i in range(len(program)-1,-1,-1):
    state = program[i]
    if(state.action == s):
      return state
  return None


def find_same_superscript(input_alphabet, superscript, place):
  for inp in input_alphabet:
    if(inp['superscript'] == superscript and inp['place'] != place):
      return inp
  return None

def print_program(program):
  for state in program:
    string = str(state.number) + "] " + state.action
    for transition in state.transitions:
      next_state = transition.next_state
      string += "(" + transition.input + "," + str(next_state.number)+ ")"
    print(string)



def generate_program(input_alphabet):
  
  program = [] #Set of program instructions

  curr_state = 1 #Current state in the program

  first_stack = Stack()
  second_stack = Stack()


  #Add first step
  state = make_step(curr_state,s,None,None)
  state.add_transition('#', state)
  next_state = State(curr_state+1,s)
  state.add_transition('#', next_state)
  program.append(state)
  curr_state+=1

  
  #Iterate through every token in the language
  for i in range(len(input_alphabet)):
    elem = input_alphabet[i]['element']
    superscript = input_alphabet[i]['superscript']
    superscript_amt = int(re.findall('\d+', input_alphabet[i]['condition'])[0])
    superscript_amt_condition = re.findall('[<>=!]=?', input_alphabet[i]['condition'])[0]
    place = input_alphabet[i]['place']


    #Add scan states depending on the number of the element's superscript (i.e. k >= 1)
    for j in range(0,superscript_amt):
      program.append(make_step(curr_state,s,elem,State(curr_state+1,s)))
      curr_state +=1
  
  #Retrieve latest scan state and add a transition going to the halt state
  latest_scan_state = get_latest_scan_state(program)
  latest_scan_state.add_transition('#', State(curr_state+1, s))
  curr_state+=1

  #Add halt state as the last state
  program.append(make_step(curr_state, h, None, None))
  print_program(program)

  '''
    if(i+1 < len(input_alphabet)):
      if(input_alphabet[i+1]['superscript'] == superscript):
  '''


  '''
    if(i+1 < len(input_alphabet)):
      if(find_same_superscript(input_alphabet,elem,place) is not None):
        program.append(make_step(curr_state,s,elem,curr_state+1))
        program.append(make_step(curr_state+1,w,elem,curr_state))
        if(not first_stack_full): 
          first_stack_full = True
        elif(first_stack_full and not second_stack_full):
          second_stack_full = True


      if(not first_stack_full):
        program.append(make_step(curr_state,s,elem,curr_state+1))
        program.append(make_step(curr_state+1,w,elem,curr_state))
        first_stack_full = True
  '''
      #elif(first_stack_full and not second_stack_full):
        #if(i > 0 and )

    #elif(i > 0 and i < len(input_alphabet)):
    
    #elif(i == len(input_alphabet)-1):

    




      


  



  return program

if __name__ == "__main__":
  input_alphabet = []
  generate_program(input_alphabet)