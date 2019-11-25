def onewayonestack(input):
	

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
				inputdict = {"superscript":"1", "element":element[0]} #one character
				input_alphabet.append(inputdict)
		print(input_alphabet)

		result = []
		

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
		if error == True:
			print("Sorry! Can't be solved using 1 way 1 stack")
		else:
			######################GENERATE DENNING NOTATION for >= HERE
			pass

	#######element checker for ∈
	else: 
		error = False
		string = input.split("|")

		input_alphabet = []

		condition = string[1].split("E")[1]
		
		elements = string[0].split(" ")
		if len(elements) > 3:
			error = True
		else:
			i = 0
			while i < len(elements) and i+1 != len(elements):
				if elements[i][0] == 'w' and elements[i+1][0] == 'w' :
					error = True
				i+=1

		if error == True:
			print("Sorry! Can't be solved using 1 way 1 stack")
		else:
			######################GENERATE DENNING NOTATION for ∈ HERE
			pass
#input = "L={ak bm dk|k>=1,m>2}"
input = "L={ax by cz by|x>=1,y>=1,z>=1}"
onewayonestack(input)