import json
import ast

def ReadFromJson(filePath):
    
    jsonFile=open(filePath)
    jsonData=json.load(jsonFile)

    states = list(ast.literal_eval(str(jsonData["states"])))
    states.sort()

    input_symbols = list(ast.literal_eval(str(jsonData["input_symbols"])))
    input_symbols.sort()

    transitions = ast.literal_eval(str(jsonData["transitions"]))

    initial_state = str(jsonData["initial_state"])

    final_states = list(ast.literal_eval(str(jsonData["final_states"])))
    final_states.sort()

    return (states , input_symbols , transitions , initial_state , final_states)
