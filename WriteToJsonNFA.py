import json

def WriteToJsonNFA(states, input_symbols, transitions, initial_state, final_states, filePath):

    states = str(set(states))
    input_symbols = str(set(input_symbols))

    output = {
        "states": states,
        "input_symbols": input_symbols,
        "transitions": transitions,
        "initial_state": initial_state,
        "final_states": final_states
    }
    with open(filePath, "w") as outfile:
        jsonObj = json.dump(output, outfile, indent=4)