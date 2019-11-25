result = []
scanL = False

def minimum_required(element, state_number):
    global result
    # print("min ", str(state_number))
    
    minimum = int(element['condition'][2])
    for i in range (0, minimum):
        scan = -1
        while "scan" not in result[scan]:
            scan -= 1
        result.append(str(state_number) + "] scanR( " + element['element'] + ", " + str(state_number + 1) + " )")
        state_number += 1
        result.append(str(state_number) + "] write( " + element['element'] + ", " + str(state_number + 1) + " )")
        state_number += 1
        
    return state_number


def connect(element, state_number, read, conn):
    global result
    # print("connect ", str(state_number))
    
    temp = result[conn]
    temp = temp + " ( " + element['element'] + ", " + str(state_number) + " )"
    result[conn] = temp
    result.append(str(state_number) + "] read( " + read + ", " + str(state_number + 1) + " )")

    return state_number + 1

def loop(scan, action_letter, state_number, action):
    global result
    # print("loop ", str(state_number))
    
    result.append(str(state_number) + "] scanR( " + scan + ", " + str(state_number + 1) + " )")
    state_number += 1
    result.append(str(state_number) + "] " + action + "( " + action_letter + ", " + str(state_number - 1) + " )")
    
    return state_number + 1

def ignoreR(input_alphabet, current, next, state_number):
    global result
    # print("ignoreR ", str(state_number))
    
    temp = result[-2]
    temp = temp + " ( " + input_alphabet[current]['element'] + ", " + str(state_number-2) + " )"
    for i in range(current + 1, next):
        temp = temp + " ( " + input_alphabet[i]['element'] + ", " + str(state_number-2) + " )"
    result[-2] = temp

def ignoreL(input_alphabet, current, end, state_number):
    global result, scanL
    # print("ignoreL ", str(state_number))
    
    scanL = True
    temp = str(state_number) + "] scanL( " + input_alphabet[current]['element'] + ", " + str(state_number) + " )"
    for i in range(end + 1, current):
        temp = temp + " ( " + input_alphabet[i]['element'] + ", " + str(state_number) + " )"
    temp = temp + " ( " + input_alphabet[end]['element'] + ", " + str(state_number + 1) + " )"
    
    result.append(temp)

def reverse(state_number, prev, scan, write):
    global result, scanL
    # print("reverse ", str(state_number))
    
    scanL = True
    result.append(str(state_number) + "] scanL( " + scan + ", " + str(state_number) + " ) ( " + prev + ", " + str(state_number + 1) + " )")
    state_number += 1
    result.append(str(state_number) + "] scanR( " + scan + ", " + str(state_number + 1) + " )")
    state_number += 1
    result.append(str(state_number) + "] write( " + write + ", " + str(state_number - 1) + " )")
    
    return state_number + 1

def two_way_one_stack(input):
    global result
    original = input
    input = input[3:-1]

    if input.find("E") == -1: 
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
                inputdict = {"superscript":"1", "element":element[0],  "condition": "==1", "place":place} #one character
                input_alphabet.append(inputdict)
        print(input_alphabet) # TODO: remove this after testing

        state_number = 2

        result.append("1] scanR( #, 2 )")
        
        for current in range (0, len(input_alphabet)):
            if input_alphabet[current]['place'] != "0":
                if input_alphabet[current]['condition'] == "==1":
                    result.append(str(state_number) + "] scanR( " +input_alphabet[current]['element'] + ", " + str(state_number + 1) + " )")
                    state_number += 1

                else:
                    state_number = minimum_required(input_alphabet[current], state_number)
                    state_number = loop(input_alphabet[current]['element'], input_alphabet[current]['element'], state_number, 'write')
                    input_alphabet[current]['place'] = "0"
                    flag = current

                    for skip in range(current + 1, len(input_alphabet)):
                        if input_alphabet[skip]['superscript'] == input_alphabet[current]['superscript'] and input_alphabet[skip]['place'] != "0":
                            if flag != current:
                                temp = result[-2]
                                temp = temp + " ( " + input_alphabet[flag + 1]['element'] + ", " + str(state_number) + " )"
                                result[-2] = temp
                                state_number = reverse(state_number, input_alphabet[flag-1]['element'], input_alphabet[flag]['element'], input_alphabet[current]['element'])

                            conn = -2
                            if skip > flag + 1:
                                ignoreR(input_alphabet, flag + 1, skip, state_number)
                            state_number = connect(input_alphabet[skip], state_number, input_alphabet[current]['element'], conn)
                            state_number = loop(input_alphabet[skip]['element'], input_alphabet[current]['element'], state_number, 'read')
                            input_alphabet[skip]['place'] = "0"
                            flag = skip
                    next = 1
                    if flag == current:
                        if "write" in result[-1]:
                            s = -3
                            if state_number > 9:
                                s = -4
                            if current + 1 < len(input_alphabet):
                                if input_alphabet[current + 1]['place'] == "0":
                                    result[-2] = result[-2] + " ( " + input_alphabet[current + 1]['element'] + ", " + str(state_number - 2) + " )"
                                else:
                                    result[-2] = result[-2] + " ( " + input_alphabet[current + 1]['element'] + ", " + str(state_number+1) + " )"
                            else:
                                result[-2] = result[-2] + " ( #, " + str(state_number+1) + " )"
                            result[-1] = result[-1][:s] + str(state_number) + " )"
                            result.append(str(state_number) + "] read( " + input_alphabet[current]['element'] + ", " + str(state_number - 2) + " )")
                            state_number += 1
                            result.append(str(state_number) + "] read( " + input_alphabet[current]['element'] + ", " + str(state_number + 1) + " )")
                            state_number += 1
                            if current + 1 < len(input_alphabet) and input_alphabet[current + 1]['place'] != "0":
                                result.append(str(state_number) + "] write( " + input_alphabet[current + 1]['element'] + ", " + str(state_number + 1) + " )")
                                state_number += 1
                                input_alphabet[current + next]['condition'] = input_alphabet[current + 1]['condition'][:-1] + str(int(input_alphabet[current + 1]['condition'][-1])-1)
                                

                    else:
                        while current + next < len (input_alphabet) and input_alphabet[current + next]['place'] == "0":
                            next += 1
                        if current + next < len(input_alphabet):
                            if current + next < flag and input_alphabet[current + next]['place'] != "0":
                                if flag + 1 == len(input_alphabet):
                                    letter = "#"
                                else:
                                    letter = input_alphabet[flag+1]['element']
                                result[-2] = result[-2] + " ( " + letter + ", " + str(state_number) + " )"
                                ignoreL(input_alphabet, flag, current + next - 1, state_number)
                                state_number += 1
                            elif current + next > flag and input_alphabet[current + next]['place'] != "0":
                                result[-2] = result[-2] + " ( " + input_alphabet[current + next]['element'] + ", " + str(state_number) + " )"
                                if "read" in result[-1]:
                                    action = "write"
                                else:
                                    action = "read"
                                result.append(str(state_number) + "] " + action + "( " + input_alphabet[current + next]['element'] + ", " + str(state_number + 1) + " )")
                                state_number += 1
                                input_alphabet[current + next]['condition'] = input_alphabet[current + next]['condition'][:-1] + str(int(input_alphabet[current + next]['condition'][-1])-1)

        last = -1
        while "scan" not in result[last]:
            last -= 1
        if " #, " not in result[last]:
            print(last)
            if last < -2:
                result[last] = result[last] + " ( #, " + str(state_number - 1) + " )"
            else:
                result[last] = result[last] + " ( #, " + str(state_number) + " )"

        if not scanL:
            if len(input_alphabet) > 1:
                result.append(str(state_number) + "] scanL( " + input_alphabet[-1]['element'] + ", " + str(state_number) + " ) ( " + input_alphabet[-2]['element'] + ", " + str(state_number + 1) + " )")
            else:
                result.append(str(state_number) + "] scanL( " + input_alphabet[-1]['element'] + ", " + str(state_number) + " ) ( #, " + str(state_number + 1) + " )")
            state_number += 1
            result.append(str(state_number) + "] scanR( " + input_alphabet[-1]['element'] + ", " + str(state_number) + " ) ( #, " + str(state_number + 1) + " )")
            state_number += 1

        result.append(str(state_number) + "] HALT")

        print(original)
        for x in result:
            print(x)
        
    else:
        string = input.split("|")
        input_alphabet = []
        elements = string[0].split(" ")
        condition = string[1].split("E")[1]
        condition = condition[1:-2].split("∪")

        print(elements)
        print(condition)
        
# input = "L={w c wR c w|wE(a∪b∪c∪d)*}"
# input = "L={ax bx p d cx|x>=1}"
# input = "L={an bm cm dn|n>=1,m>=1}"
input = "L={w e w|wE(a∪b)*}"

two_way_one_stack(input)