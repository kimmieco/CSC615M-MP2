import re

s = "scan"
w1 = "write 1"
r1 = "read 1"
h = "halt"
w2 = "write 2"
r1 = "read 2"


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
    self.is_empty = True
    self.used = False
    self.superscript = None
    self.symbol = None


'''
Creates a state in the PDA:

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
  for state in reversed(program):
    #print(i)
    #state = program[i]
    if(state.action == s):
      #print("Latest state: " + str(state.number))
      return state
  return None


def find_same_superscript(input_alphabet, superscript, start, dir):
  for i in range(dir,len(input_alphabet)):
    if(input_alphabet[i]['superscript'] == superscript):
      return input_alphabet[i]
  return None

def print_program(program):
  for state in program:
    string = str(state.number) + "] " + state.action
    for transition in state.transitions:
      next_state = transition.next_state
      string += "(" + transition.input + "," + str(next_state.number)+ ")"
    print(string)

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

    latest_scan_state = get_latest_scan_state(program)
    lss_num = latest_scan_state.number

    for j in range(0,superscript_amt):
      program.append(make_step(curr_state,s,elem,State(curr_state+1,s)))
      curr_state +=1

    if(i > 0): #If the element is not the first
      print("not first element")

      if(not first_stack.is_empty):
        #If the superscript of the element pushed into the stack is the same as the current superscript
        if(first_stack.superscript == superscript):
          #Make Read 1 state
          r = make_step(curr_state, r1,None,None)
          program.append(r)
          #Latest scan state goes to Read 1 state
          latest_scan_state.add_transition(elem,r)
          #If there are other succeeding elements ahead with the same superscript in input alphabet,
          if(find_same_superscript(input_alphabet,superscript,i+1,1)):
            #Make Write 2 state
            w = make_step(curr_state+1,w2,None,None)
            program.append(w)
            curr_state+=1
            #Read 1 state goes to Write 2 state
            r.add_transition(first_stack.symbol,w)
            #Make Scan state
            s = make_step(curr_state+1,s,None,None)
            program.append(s)
            curr_state+=1
            #Write 2 state goes to new Scan state
            w.add_transition(elem,s)
            #Scan state goes back to Read 1 state
            s.add_transition(elem,r)
          #If there are no other succeeding elements with the same superscript
          else:
            #Make Scan state
            s = make_step(curr_state+1,s,None,None)
            program.append(s)
            curr_state+=1
            #Read 1 state goes to Scan state
            r.add_transition(first_stack.symbol,s)
            #Scan state goes to Read 1 state
            s.add_transition(elem,r)
          pop_stack(first_stack)

      elif(not second_stack.is_empty):
         if(second_stack.superscript == superscript):
 
  
    else: #If the element is the first
      if(len(input_alphabet) > 1):
        if(find_same_superscript(input_alphabet,superscript,i+1,1)):
          push_stack(first_stack,superscript,elem)
          program.append(make_step(curr_state,s,elem,State(curr_state+1,w1)))
          curr_state+=1
          program.append(make_step(curr_state,w1,elem, State(curr_state-1,s)))
      else:
        program.append(make_step(curr_state,s,elem,State(curr_state,s)))
      

    '''

    #Add scan states depending on the number of the element's superscript (i.e. k >= 1)
    for j in range(0,superscript_amt):
      program.append(make_step(curr_state,s,elem,State(curr_state+1,s)))
      curr_state +=1

    if(i > 0): #If the element is not the first
      
      #Check if first stack empty
      if(not first_stack.is_empty):
        #If the superscript of the elem in the first stack match with the curr elem
        if(first_stack.superscript == superscript):
          
          #Make scan symbol
          program.append(make_step(lss_num, s, elem, State(curr_state+1,r1)))
          curr_state+=1
          #Make read 1 prev symbol
          program.append(make_step(curr_state, r1,first_stack.symbol,State(curr_state+1,w2)))
          curr_state+=1
          #Make write 2 symbol
          #Check if there is elements with the same superscript. if ther is, then make the write2 step
          program.append(make_step(curr_state, w2,elem,State(lss_num,s)))
          curr_state+=1
          #Pop from stack
          pop_stack(first_stack)

      #else check if second stack empty
      elif(not second_stack.is_empty):
        #If the superscript of the elem in the second stack match with the curr elem?
        if(first_stack.superscript == superscript):
          print("hackdog")
          #Pop from stack
          #Make scan symbol
          #Make read 1 prev symbol
          #Make write 2 symbol 

      else:
        print("1W2S is not doable!")

    else: #If the element is the first
      if(first_stack.is_empty):
        push_stack(first_stack,superscript,elem)
        program.append(make_step(lss_num,s,elem,State(curr_state+1,w1)))
        curr_state+=1
        program.append(make_step(curr_state,w1,elem, State(lss_num,s)))
    '''
  
  #Retrieve latest scan state and add a transition going to the halt state
  latest_scan_state = get_latest_scan_state(program)
  latest_scan_state.add_transition('#', State(curr_state+1, s))
  curr_state+=1

  #Add halt state as the last state
  program.append(make_step(curr_state, h, None, None))
  print_program(program)



  return program

if __name__ == "__main__":
  input_alphabet = []
  generate_program(input_alphabet)