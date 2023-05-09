from ReadFromJson import ReadFromJson
from WriteToJsonNFA import WriteToJsonNFA


def phase4_star(inputFA, outputRFA):

    (states, input_symbols, transitions, initial_state, final_states) = ReadFromJson(inputFA)

    state_NO = [sub.replace('q', '') for sub in states]
    for i in range(len(state_NO)):
        state_NO[i] = int(state_NO[i])
    max_No = max(state_NO)

    new_initial_state = 'q' + str(max_No + 1)
    new_final_state = 'q' + str(max_No + 2)

    new_states = states
    new_states.append(new_initial_state)
    new_states.append(new_final_state)

    transitions[new_initial_state] = {}
    transitions[new_initial_state][""] = "{'" + str(initial_state) + "','" + str(new_final_state) + "'}"
    transitions[new_final_state] = {}
    transitions[new_final_state][""] = "{'" + str(new_initial_state) + "'}"
    for fs in final_states:
        transitions[fs][""] = "{'" + str(new_final_state) + "'}"
         
    new_final_state = "{'" + str(new_final_state) + "'}" 
    
    WriteToJsonNFA(new_states, input_symbols, transitions, new_initial_state, new_final_state, outputRFA)


def phase4_union(inputFA1, inputFA2, outputRFA):

    (states1, input_symbols1, transitions1, initial_state1, final_states1) = ReadFromJson(inputFA1)

    state_NO = [sub.replace('q', '') for sub in states1]
    for i in range(len(state_NO)):
        state_NO[i] = int(state_NO[i])
    max_No = max(state_NO)
    i = max_No + 1

    (states2, input_symbols2, transitions2, initial_state2, final_states2) = ReadFromJson(inputFA2)

    maping = {}
    for q in states2:
        maping[q] = 'q' + str(i)
        i += 1
    for j in range(len(states2)):
        states2[j] = maping[states2[j]]

    new_initial_state = 'q' + str(i)
    i += 1

    new_final_state = 'q' + str(i)

    new_states = states1
    for q in states2:
        new_states.append(q)
    new_states.append(new_initial_state)
    new_states.append(new_final_state)

    initial_state2 = maping[initial_state2]
    for j in range(len(final_states2)):
        final_states2[j] = maping[final_states2[j]]
    
    new_transitions = transitions1
    for q in transitions2:
        tempstr = ""
        for alpha in input_symbols2:
            if alpha in transitions2[q]:
                for p in maping:
                    if p in transitions2[q][alpha]:
                        tempstr = transitions2[q][alpha].replace(p, maping[p])
                transitions2[q][alpha] = tempstr
        if "" in transitions2[q]:
            for p in maping:
                if p in transitions2[q][""]:
                    tempstr = transitions2[q][""].replace(p, maping[p])
            transitions2[q][""] = tempstr
    for q in transitions2:
        new_transitions[maping[q]] = transitions2[q]

    new_transitions[new_initial_state] = {}
    new_transitions[new_initial_state][""] = "{'" + str(initial_state1) + "','" + str(initial_state2) + "'}"

    new_transitions[new_final_state] = {}
    for fs in final_states1:
        if "" in new_transitions[fs]:
            new_transitions[fs][""] = new_transitions[fs][""].replace("}", "")
            new_transitions[fs][""] = new_transitions[fs][""] + ",'" + str(new_final_state) + "'}"
        else:
            new_transitions[fs][""] = "{'" + str(new_final_state) + "'}"
    for fs in final_states2:
        if "" in new_transitions[fs]:
            new_transitions[fs][""] = new_transitions[fs][""].replace("}", "")
            new_transitions[fs][""] = new_transitions[fs][""] + ",'" + str(new_final_state) + "'}"
        else:
            new_transitions[fs][""] = "{'" + str(new_final_state) + "'}"

    new_final_state = "{'" + str(new_final_state) + "'}" 

    new_input_symbols = input_symbols1 + input_symbols2

    WriteToJsonNFA(new_states, new_input_symbols, new_transitions, new_initial_state, new_final_state, outputRFA)


def phase4_concat(inputFA1, inputFA2, outputRFA):

    (states1, input_symbols1, transitions1, initial_state1, final_states1) = ReadFromJson(inputFA1)
    
    state_NO = [sub.replace('q', '') for sub in states1]
    for i in range(len(state_NO)):
        state_NO[i] = int(state_NO[i])
    max_No = max(state_NO)
    i = max_No + 1
    
    (states2, input_symbols2, transitions2, initial_state2, final_states2) = ReadFromJson(inputFA2)
    
    maping = {}
    for q in states2:
        maping[q] = 'q' + str(i)
        i += 1
    for j in range(len(states2)):
        states2[j] = maping[states2[j]]

    new_initial_state = initial_state1

    new_final_state = 'q' + str(i)

    new_states = states1
    for q in states2:
        new_states.append(q)
    new_states.append(new_final_state)

    initial_state2 = maping[initial_state2]
    for j in range(len(final_states2)):
        final_states2[j] = maping[final_states2[j]]

    new_transitions = transitions1
    for q in transitions2:
        tempstr = ""
        for alpha in input_symbols2:
            if alpha in transitions2[q]:
                for p in maping:
                    if p in transitions2[q][alpha]:
                        tempstr = transitions2[q][alpha].replace(p, maping[p])
                transitions2[q][alpha] = tempstr
        if "" in transitions2[q]:
            for p in maping:
                if p in transitions2[q][""]:
                    tempstr = transitions2[q][""].replace(p, maping[p])
            transitions2[q][""] = tempstr
    for q in transitions2:
        new_transitions[maping[q]] = transitions2[q]

    new_transitions[new_final_state] = {}
    for fs in final_states1:
        if "" in new_transitions[fs]:
            new_transitions[fs][""] = new_transitions[fs][""].replace("}", "")
            new_transitions[fs][""] = new_transitions[fs][""] + ",'" + str(initial_state2) + "'}"
        else:
            new_transitions[fs][""] = "{'" + str(initial_state2) + "'}"
    for fs in final_states2:
        if "" in new_transitions[fs]:
            new_transitions[fs][""] = new_transitions[fs][""].replace("}", "")
            new_transitions[fs][""] = new_transitions[fs][""] + ",'" + str(new_final_state) + "'}"
        else:
            new_transitions[fs][""] = "{'" + str(new_final_state) + "'}"

    new_final_state = "{'" + str(new_final_state) + "'}" 

    new_input_symbols = input_symbols1 + input_symbols2   

    WriteToJsonNFA(new_states, new_input_symbols, new_transitions, new_initial_state, new_final_state, outputRFA)

        

#phase4_star("FA.json", "out_star.json")

#phase4_union("FA1.json", "FA2.json", "out_union.json")

#phase4_concat("FA1.json", "FA2.json", "out_concat.json")