input = "L={ak c bm d|k>=1,m>2}"

input = input[3:-1]

string = input.split("|")

input_alphabet = []

conditions = string[1].split(",")

elements = string[0].split(" ")

for element in elements:
	for cond in conditions:
		if len(element) == 2:
			print(element[0])
			if element[1] == cond[0]:
				inputdict = {"superscript":element[1], "element":element[0], "condition": cond[1:]} #superscript:character
				input_alphabet.append(inputdict)
	if len(element) == 1:
		inputdict = {"superscript":"1", "element":element[0]} #one character
		input_alphabet.append(inputdict)
print(input_alphabet)

