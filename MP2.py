
input_alphabet_global = []

def set_input_alphabet_global(input_alphabet):
	global input_alphabet_global
	input_alphabet_global = input_alphabet

def get_input_alphabet_global():
	return input_alphabet_global


def onewayonestack(input):
	
	result = []
	#build element checker for >= symbols lng muna#############
	if input.find("E") == -1: 
		error = False
		string = input.split("|")

		input_alphabet = []

		conditions = string[1].split(",")

		elements = string[0].split(" ")
		place = 0
		for element in elements:
			place += 1
			for cond in conditions:
				if len(element) == 2:
					if element[1] == cond[0]:
						inputdict = {"superscript":element[1], "element":element[0], "condition": cond[1:], "place":place} #superscript:character
						input_alphabet.append(inputdict)
			if len(element) == 1:
				inputdict = {"superscript":"1", "element":element[0], "place":place} #one character
				input_alphabet.append(inputdict)

		set_input_alphabet_global(input_alphabet)

		elemcount = 0
		for elem in input_alphabet:
			if elem["superscript"] != "1":
				elemcount += 1
		if elemcount == 3:
			first = input_alphabet[0]
			second = input_alphabet[1]
			third = input_alphabet[2]
			if first["superscript"] == second["superscript"] and second["superscript"] == third["superscript"]:
				error = True
			for cond in conditions:
				if int(cond[-1]) != 1:
					error = True 
		if elemcount >= 4:
			i = 0
			while i < len(input_alphabet) and i+2 != len(input_alphabet):
				first = input_alphabet[i]
				second = input_alphabet[i+1]
				third = input_alphabet[i+2]
				if first["superscript"] == second["superscript"] and second["superscript"] == third["superscript"]:
					error = True
				if not (first["superscript"] == second["superscript"] or second["superscript"] == third["superscript"]):
					error = True
				if first["superscript"] != second["superscript"] and second["superscript"] != third["superscript"]:
					error = False
				i+=1
			for cond in conditions:
				if int(cond[-1]) != 1:
					error = True 
		if error == True:
			result.append("Sorry! Can't be solved using 1 way 1 stack")
		else:
			######################GENERATE DENNING NOTATION for >= HERE
			if elemcount == 1:
				state = 1
				result.append("1]scan(#,1)(#,2)")
				state+= 1
				prev = None
				for elem in input_alphabet:
					if elem['superscript'] != "1":
						for i in range(0, int(elem['condition'][-1])):
							result.append(str(state)+"]scan("+elem['element']+","+str(state+1)+")")
							state+=1

						result.append(str(state)+"]scan("+elem['element']+","+str(state)+")")
						if elem['place'] == len(input_alphabet):
							result[state-1]+="(#,"+str(state+1)+")"
							state+=1
							result.append(str(state)+"]write(#,"+str(state+1)+")")
							state +=1
							result.append(str(state)+"]read(#,"+str(state+1)+")")
							state +=1
							result.append(str(state)+"]Halt")
					else:
						if prev != None:
							
							if prev['superscript'] != "1":
								result[state-1] = result[state-1] + "("+elem['element']+","+str(state+1)+")"
							else:
								result.append(str(state)+"]scan("+elem['element']+","+str(state+1)+")")
							state+=1
							if elem['place'] == len(input_alphabet):
								result.append(str(state)+"]write(#,"+str(state+1)+")")
								state +=1
								result.append(str(state)+"]read(#,"+str(state+1)+")")
								state +=1
								result.append(str(state)+"]Halt")

						else:
							result.append(str(state)+"]scan("+elem['element']+","+str(state+1)+")")
							state+=1

					prev = elem

			elif elemcount == 2:
				elem1 = None
				elem2 = None
				for elem in input_alphabet:
					if elem["superscript"] != "1":
						if elem1 == None:
							elem1 = elem
						else:
							elem2 = elem

				if elem1['superscript'] == elem2['superscript']:#for k, k

					state = 1
					result.append(str(state)+"]scan(#,1)(#,2)")
					second = None
					prev = None
					indexwrite = []
					consecutive = False
					for elem in input_alphabet:
						if elem["superscript"] != "1" and elem["place"] >= 1:
							
							if prev is None:
								result.append(result[-1][-2:-1]+"]scan("+ elem["element"] + ","+str(int(result[-1][-2:-1])+1)+")")
								prev = elem
							indexwrite = [i for i, s in enumerate(result) if 'write' in s]
							if indexwrite == []:
								result.append(result[-1][-2:-1]+"]write("+ elem["element"] + ","+str(int(result[-1][-2:-1])-1)+")")
								
							if prev['place']+1 == elem['place']: ##consecutive element
								result[-2] = result[-2] +"("+ elem["element"] +","+str(int(result[-1][-2:-1])+2)+")"
								result.append(result[-2][-2:-1]+"]"+"read("+ prev['element'] +","+ str(int(result[-2][-2:-1])+1)+")" )
								consecutive = True
								if elem["place"] == len(input_alphabet):
									result.append(result[-1][-2:-1]+"]scan("+elem['element']+","+result[-1][0]+")(#,"+str(int(result[-1][-2:-1])+1)+")")
									result.append(result[-1][-2:-1]+"]Halt")
								else:
									result.append(result[-1][-2:-1]+"]scan("+elem['element']+","+result[-1][0]+").")
							if consecutive == False:
								second = elem
								if elem['place'] == len(input_alphabet):
									result.append(result[-1][-2:-1]+"]scan("+elem['element']+","+str(int(result[-1][-2:-1])+1)+")")
									result.append(result[-1][-2:-1]+"]"+"read("+ prev['element'] +","+ str(int(result[-1][-2:-1])+1)+")")
									result.append(result[-1][-2:-1]+"]scan("+elem['element']+","+str(int(result[-1][-2:-1])-1)+")(#,"+str(int(result[-1][-2:-1])+1)+")")
									result.append(result[-1][-2:-1]+"]Halt")

						else:
							
							try:
								if prev['place']+1 == elem['place']:
									result[-2] = result[-2] +"("+ elem["element"] +","+str(int(result[-1][-2:-1])+2)+")"
							except:
								pass
							if prev != None and result[-1].find("write") != -1:
								result.append(result[-2][-2:-1]+"]scan("+ elem["element"] + ","+str(int(result[-2][-2:-1])+1)+")")
							if prev == None or prev != None and second != None :
								if result[-1].find(".") != -1:
									result[-1] = result[-1][:-1]+"("+ elem["element"] + ","+str(int(result[-1][0])+1)+")"
								else:
									result.append(result[-1][-2:-1]+"]scan("+ elem["element"] + ","+str(int(result[-1][-2:-1])+1)+")")
								
							if elem['place'] == len(input_alphabet):
								if result[-1].find("scan") != -1:
									result[-1] = result[-1]+"(#," + str(int(result[-1][0])+1)+")"
								else:
									result.append(str(int(result[-1][0])+1)+"]scan(#,"+str(int(result[-1][0])+2)+")")
								result.append(str(int(result[-1][0])+1)+"]Halt")
				else: #n,m 2 elem
					state = 1
					criticalscan = None
					result.append("1]scan(#,1)(#,2)")
					prev = None
					for elem in input_alphabet:
						if elem["superscript"] != "1":
							if criticalscan == None:
								for i in range(0,int(elem["condition"][-1])):
									result.append(str(state+1)+"]scan("+elem["element"]+","+str(state+2)+")")
									state+=1
								state+=1
								result.append(str(state)+"]scan("+elem["element"]+","+str(state)+")") 
								criticalscan = state
							else:
								if prev['superscript'] != "1":
									result[state-1] = result[state-1]+"("+elem['element']+","+str(state+1)+")"
									for i in range(0,int(elem["condition"][-1])-1):
										result.append(str(state+1)+"]scan("+elem["element"]+","+str(state+2)+")")
										state+=1
									
								else:
									
									for i in range(0,int(elem["condition"][-1])):
										result.append(str(state+1)+"]scan("+elem["element"]+","+str(state+2)+")")
										state+=1

								
								state+=1
								result.append(str(state)+"]scan("+elem["element"]+","+str(state)+")") 
								criticalscan = state
								if elem['place'] == len(input_alphabet):
									result[state-1] = result[state-1]+"(#,"+str(state+1)+")"
									state+=1
									result.append(str(state)+"]write(#,"+str(state+1)+")")
									state +=1
									result.append(str(state)+"]read(#,"+str(state+1)+")")
									state +=1
									result.append(str(state)+"]Halt")
						else:	
							if prev != None:
								if prev['superscript'] != "1":
									result[criticalscan-1] = result[criticalscan-1]+"("+elem['element']+","+str(state+1)+")"
									if elem['place'] == len(input_alphabet):
										result.append(str(state)+"]scan(#,"+str(state+1)+")")
										state+=1
										result.append(str(state)+"]write(#,"+str(state+1)+")")
										state +=1
										result.append(str(state)+"]read(#,"+str(state+1)+")")
										state+=1
										result.append(str(state)+"]Halt")
								else:
									
									result[criticalscan-1] = result[criticalscan-1]+"("+elem['element']+","+str(state+1)+")"
									
							else:
								state+=1
								result.append(str(state)+"]scan("+elem["element"]+","+str(state+1)+")") 
								
								pass
						prev = elem
					
			else: #more than 2 
				if elemcount == len(conditions):
					state = 1
					result.append("1]scan(#,1)(#,2)")
					state+= 1
					criticalscan = None
					prev = None
					for elem in input_alphabet:
						if prev != None:
							result[-1]+="("+elem['element']+","+ str(state)+")"
							for i in range(0, len(elem['condition'][-1])):
								result.append(str(state)+"]scan("+elem["element"]+","+str(state+1)+")")
								state+=1
						else:

							for i in range(0, len(elem['condition'][-1])):
								result.append(str(state)+"]scan("+elem["element"]+","+str(state+1)+")")
								state+=1

						result.append(str(state)+"]scan("+elem["element"]+","+str(state)+")")
						state+=1
						
						if elem['place'] == len(input_alphabet):
							result[-1]+="(#,"+str(state+1)+")"
							state+=1
							result.append(str(state)+"]write(#,"+str(state+1)+")")
							state +=1
							result.append(str(state)+"]read(#,"+str(state+1)+")")
							state +=1
							result.append(str(state)+"]Halt")
						prev = elem
				if elemcount == 3:
					first =  input_alphabet[0]
					second = input_alphabet[1]
					third = input_alphabet[2]
					stacksuperscript = None
					save = False
					state = 1
					result.append("1]scan(#,1)(#,2)")
					state+= 1
					criticalscan = None
					if first['superscript'] == second['superscript']:
						stacksuperscript = first['superscript']
						for elem in input_alphabet:
							if elem['superscript'] == stacksuperscript:
								if save == False:
									save = True
									criticalscan = state
									result.append(str(state)+"]scan("+elem["element"]+","+str(state+1)+")")
									state+=1
									result.append(str(state)+"]write("+elem["element"]+","+str(criticalscan)+")")
									state+=1
									result.append(str(state)+"]read("+elem["element"]+","+str(criticalscan)+")")
									state+=1

								else:
									result[criticalscan-1]+= "("+elem['element']+","+ str(state-1)+")"
							else:
								result[criticalscan-1]+= "("+elem['element']+","+ str(criticalscan)+")"
								result[criticalscan-1]+= "(#,"+ str(state)+")"
								result.append(str(state)+"]Halt")


					elif first['superscript'] == third['superscript'] :
						stacksuperscript = first['superscript']
						for elem in input_alphabet:
							if elem['superscript'] == stacksuperscript:
								if save == False:
									save = True
									criticalscan = state
									result.append(str(state)+"]scan("+elem["element"]+","+str(state+1)+")")
									state+=1
									result.append(str(state)+"]write("+elem["element"]+","+str(criticalscan)+")")
									state+=1
									result.append(str(state)+"]read("+elem["element"]+","+str(criticalscan)+")")
									state+=1

								else:
									result[criticalscan-1]+= "("+elem['element']+","+ str(state-1)+")"
									result[criticalscan-1]+= "(#,"+ str(state)+")"
									result.append(str(state)+"]Halt")
							else:
								result[criticalscan-1]+= "("+elem['element']+","+ str(criticalscan)+")"
								
					else : #second['superscript'] == third
						stacksuperscript = second['superscript']
						for elem in input_alphabet:
							if elem['superscript'] == stacksuperscript:
								if save == False:
									save = True									
									result[criticalscan-1]+= "("+elem['element']+","+ str(state)+")"
									result.append(str(state)+"]write("+elem["element"]+","+str(criticalscan)+")")
									state+=1
									result.append(str(state)+"]read("+elem["element"]+","+str(criticalscan)+")")
									state+=1

								else:
									result[criticalscan-1]+= "("+elem['element']+","+ str(state-1)+")"
									result[criticalscan-1]+= "(#,"+ str(state)+")"
									result.append(str(state)+"]Halt")
							else:
								criticalscan = state
								result.append(str(state)+"]scan("+elem["element"]+","+str(criticalscan)+")")
								state+=1
								print(result)
				if elemcount == 4:
					first = input_alphabet[0]
					second = input_alphabet[1]
					third = input_alphabet[2]
					fourth = input_alphabet[3]
					state = 1
					result.append("1]scan(#,1)(#,2)")
					state+= 1
					criticalscan = None
					if first['superscript'] == fourth['superscript'] and second['superscript'] == third['superscript']:
						for elem in input_alphabet:

							if elem != third and elem != fourth:
								
								if criticalscan == None:
									criticalscan = state
									result.append(str(state)+"]scan("+elem['element']+","+str(state+1)+")")
									state+=1
									result.append(str(state)+"]write("+elem['element']+","+str(criticalscan)+")")
									state+=1
								else:
									result[criticalscan-1]+="("+elem['element']+","+str(state)+")"
									result.append(str(state)+"]write("+elem['element']+","+str(criticalscan)+")")
									state+=1
							elif elem == third:
								result[criticalscan-1]+="("+elem['element']+","+str(state)+")"
								result.append(str(state)+"]read("+second['element']+","+str(criticalscan)+")")
								state+=1
							else:
								result[criticalscan-1]+="("+elem['element']+","+str(state)+")"
								result.append(str(state)+"]read("+first['element']+","+str(criticalscan)+")")
								state+=1
							if elem['place'] == len(input_alphabet):
								result[criticalscan-1]+= "(#,"+ str(state)+")"
								result.append(str(state)+"]Halt")

					
				else:
					result.append("Sorry! Can't be solved using 1 way 1 stack")





				
						
	#######element checker for ∈
	else: 
		error = False
		string = input.split("|")

		input_alphabet = []



		condition = string[1].split("E")[1]
		condition = condition[1:-2]
		alphanumeric= condition.split("U") 
		elements = string[0].split(" ")
		inputdict = None
		place = 0
		elemcount = 0
		for e in elements:
			place += 1
			
			if e == 'wR':
				inputdict = {"superscript":"R", "element":e, "place":place}
				elemcount+=1
				
			elif e == 'w':
				inputdict = {"superscript":"0", "element":e, "place":place}
				elemcount+=1
				
			else:
				inputdict = {"superscript":"1", "element":e, "place":place}
			input_alphabet.append(inputdict)

		if elemcount > 3:
			error = True
		else:

			if input.find("R") != -1 and len(alphanumeric):
				error = True
			i = 0
			while i < len(elements) and i+1 != len(elements):
				if elements[i][0] == 'w' and elements[i+1][0] == 'w' :
					error = True
				i+=1
			if len(alphanumeric) == 1:
				error = False
		if error == True:
			result.append("Sorry! Can't be solved using 1 way 1 stack")
		else:
			######################GENERATE DENNING NOTATION for ∈ HERE
			
			result.append("1]scan(#,1)(#,2)")
			if input.find("R") != -1:  #case reverse
				prev = None
				criticalscan = None
				for elem in input_alphabet:
					
					if elem['superscript'] == "1":
						if prev != None:
							
							if prev['superscript'] == "1":
								if result[-1].find('write') == -1:
									result.append(result[-1][-2:-1]+"]scan("+elem['element']+","+str(int(result[-1][-2:-1])+1)+")")
								else:
									result.append(str(int(result[-1][0])+1)+"]scan("+elem['element']+","+str(int(result[criticalscan][-2:-1])+1)+")")
								
							else:#if prev['superscript'] == "0" or  prev['superscript'] == "R":
								result[criticalscan] = result[criticalscan] + "(" + elem['element']+","+ str(int(result[criticalscan][-2:-1])+1)+")"
								
						else:
							result.append(result[-1][-2:-1]+"]scan("+elem['element']+","+str(int(result[-1][-2:-1])+1)+")")
					else:# elem['superscript'] == 'R' or elem['superscript'] == '0':
						if criticalscan == None:
							state = int(result[-1][-2:-1])
							criticalscan = int(result[-1][-2:-1])-1							
							result.append(result[-1][-2:-1]+"]scan")
							for alpha in alphanumeric:
								result[criticalscan] = result[criticalscan] + "("+alpha+","+str(state+1)+")"
								result.append(str(state+1)+"]write("+alpha+","+str(criticalscan+1)+")")
								state+=1

						else:
							if result[-1].find("write") == -1:
								criticalscan = int(result[-1][0])-1
								state = int(result[-1][-2:-1])	
								for alpha in alphanumeric:
									result[criticalscan] = result[criticalscan] + "("+alpha+","+str(state+1)+")"
									result.append(str(state+1)+"]read("+alpha+","+str(criticalscan+1)+")")
									state+=1

							else:
								result.append(str(int(result[-1][0])+1)+"]scan")
								criticalscan = int(result[-1][0])-1
								state = int(result[-1][0])	
								for alpha in alphanumeric:
									result[criticalscan] = result[criticalscan] + "("+alpha+","+str(state+1)+")"
									result.append(str(state+1)+"]read("+alpha+","+str(criticalscan+1)+")")
									state+=1
							
							
					if elem['place'] == len(input_alphabet):
						if result[-1].find("scan") != -1:
							result[-1] = result[-1]+"(#," + str(int(result[-1][0])+1)+")"
						else:
							result.append(str(int(result[-1][0])+1)+"]scan(#,"+str(int(result[-1][0])+2)+")")
						result.append(str(int(result[-1][0])+1)+"]Halt")
					prev = elem
			else:# case no reverse
				print("DED")
				prev = None
				criticalscan = None
				state = 2
				for elem in input_alphabet:
					if elem['superscript'] != "1":
						if criticalscan == None:
							result.append(str(state)+"]scan")
							criticalscan = state
							for alpha in alphanumeric:
								result[criticalscan-1] += "("+alpha+","+str(state+1)+")"
								result.append(str(state+1)+"]write("+alpha+","+str(criticalscan)+")")
								state+=1 
						else:
							result.append(str(state)+"]scan")
							criticalscan = state
							result[criticalscan-1] += "("+alphanumeric[0]+","+str(state+1)+")"
							result.append(str(state+1)+"]read("+alphanumeric[1]+","+str(criticalscan)+")")
							state+=1 
							result[criticalscan-1] += "("+alphanumeric[1]+","+str(state+1)+")"
							result.append(str(state+1)+"]read("+alphanumeric[0]+","+str(criticalscan)+")")
							state+=1 
							if elem['place'] == len(input_alphabet):
								result.append(str(state+1)+"]scan(#,"+str(state+1)+")")
								state+=1
								result.append(str(state+1)+"]Halt")
								state+=1


					else:
						if prev['superscript'] != "1":
							result[criticalscan-1] += "("+elem['element']+","+str(state+1)+")"
							state+=1
						else:
							result.append(result[-1][0]+"]scan("+elem['element']+","+str(state+1)+")")
							state+=1
						
				
					prev = elem
			
	return result
#input = "L={ak bk|k>=1}"
#input = "L={0n 1m|n>=1,m>=1}"
#input = "L={ak c c bk|k>=1}"
#input = "L={c c ak bk|k>=1}"
#input = "L={ax by cz bc|x>=2,y>=4,z>=3,c>=3}"
#input = "L={w e wR|wE(aUbUcUd)*}"
#input = "L={c c ak c c|k>=3}"
#input = "L={w e w|wE(aUb)*}"
input = "L={an bm cm dn|n>=1,m>=1}"
input = input[3:-1]
print(onewayonestack(input))	