input = "L={ak c bk|k>=1}"

input = input[3:-1]

string = input.split("|")

input_alphabet = []

conditions = string[1].split(",")
for cond in conditions:
	inputdict = { "superscript":cond[0],"elements":[],"condition": cond[1:]}
	input_alphabet.append(inputdict)
# print(input_alphabet)
input_alphabet.append({ "superscript":"1","elements":[]})
elements = string[0].split(" ")
for element in elements:
	for alpha in input_alphabet:

		if len(element) == 2:
			if alpha["superscript"] == element[1]:
				alpha["elements"].append({element[0]:0})
		else:
			if alpha["superscript"] == "1":
				alpha["elements"].append({element[0]:1})
	
print(input_alphabet)

