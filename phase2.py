from ReadFromJson import ReadFromJson
from WriteToJson import WriteToJson

def FindReachble(reachable_states, input_symbols, transitions, reachable_state):
    for alpha in input_symbols:
        state = transitions[reachable_state][alpha]
        if state not in reachable_states:
            reachable_states.add(state)
            FindReachble(reachable_states, input_symbols, transitions, state)


def DeleteUnreachableStates(states, input_symbols, transitions, initial_state, final_states):
    reachable_states = {initial_state}
    FindReachble(reachable_states, input_symbols, transitions, initial_state)
    unreachable_states = reachable_states.symmetric_difference(states)
    for state in unreachable_states:
        states.remove(state)
        transitions.pop(state)
        if state in final_states:
            final_states.remove(state)
    return (states, transitions, final_states)


def InTheSamePart(q0, q1, part):
    for i in part:
        qlist = part[i]
        if q0 in qlist and q1 in qlist:
            return True
    return False


def phase2(inputDFA, outputDFA):
    (states, input_symbols, transitions, initial_state, final_states) = ReadFromJson(inputDFA)
    (states, transitions, final_states) = DeleteUnreachableStates(states, input_symbols, transitions, initial_state, final_states)
    non_final_state = [x for x in states if x not in final_states]
    partition = {
        0: {
            0: states
        },
        1: {
            0: non_final_state,
            1: final_states
        }
    }
    deleted_states = []
    i = 1
    while len(partition[i - 1]) < len(partition[i]):
        partition[i + 1] = {}
        j = 0
        for part in partition[i]:
            for q in partition[i][part]:
                if q == partition[i][part][0]:
                    partition[i + 1][j] = [q,]
                    j += 1
                else:
                    mainflag = False
                    for p in partition[i + 1]:
                        flag = False      
                        for alpha in input_symbols:
                            q0 = transitions[partition[i + 1][p][0]][alpha]
                            q1 = transitions[q][alpha]

                            if InTheSamePart(q0, q1, partition[i]):
                                flag = True
                                continue
                            else:
                                flag = False
                                break
                        if flag:
                            partition[i + 1][p].append(q)
                            deleted_states.append(q)
                            mainflag = False
                            break
                        else:
                            mainflag = True
                    if mainflag:
                        partition[i + 1][j] = [q,]
                        j += 1
        i += 1
    ds = set(deleted_states)
    deleted_states = list(ds)
    new_states = {}
    for x in partition[i]:
        if len(partition[i][x]) > 1:  
            new_q = ""            
            for q in partition[i][x]:
                new_q += q
            for q in range(len(partition[i][x])):
                new_states[partition[i][x][q]] = new_q           
        else:
            new_states[partition[i][x][0]] = partition[i][x][0]
    new_transition = transitions.copy()
    for q in transitions:
        if q in deleted_states:
            new_transition.pop(q)
    for i in range(len(new_transition)):
        q = next(iter(new_transition))
        new_transition[new_states[q]] = new_transition.pop(q)
    for q in new_transition: 
        for alpha in input_symbols:
            new_transition[q][alpha] = new_states[new_transition[q][alpha]]
    for q in new_transition:
        if initial_state in q:
            initial_state = q
        else:
            for i in range(len(final_states)):
                if final_states[i] in q:
                    final_states[i] = q
    fs = set(final_states)
    final_states = list(fs)
    WriteToJson(new_transition, input_symbols, new_transition, initial_state, final_states, outputDFA)

phase2("input2.json", "output2.json")