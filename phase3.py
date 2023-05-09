from ReadFromJson import ReadFromJson
from WriteToJson import WriteToJson
import ast

def CheckString(transitions, final_states , inputstring , current , IsAccepting) :
    lambdalist = []
    IsVisited = []
    Find_Lambda_Transition(current  , transitions , lambdalist , IsVisited)
    if inputstring == "" :
        for x in lambdalist :
            if x in final_states:
                IsAccepting[0] = True
                return
        return
    for x in lambdalist :
        if inputstring[0] in transitions[x] :
            if '{' in transitions[x][inputstring[0]] :
                listOfStates = (list(ast.literal_eval(str(transitions[x][inputstring[0]]))))
            else :
                listOfStates = transitions[x][inputstring[0]]
            for c in listOfStates :
                CheckString(transitions , final_states , inputstring[1:] , c , IsAccepting)

    

def Find_Lambda_Transition(Current , Transitions : dict , output , IsVisited):
    IsVisited.append(Current)
    output.append(Current)
    Neighbours = []
    if "" in Transitions[Current] :
        Neighbours += (list(ast.literal_eval(str(Transitions[Current][""]))))
    else :
        return
    for x in Neighbours :
        if(x not in IsVisited):
            Find_Lambda_Transition(x , Transitions , output , IsVisited)

def phase3(inputAddress) :
    (states, input_symbols, transitions, initial_state, final_states) = ReadFromJson(inputAddress)
    while(True):
        String = str(input('Enter the string :(for exit enter Exit)'))
        if(String == 'Exit') :
            return
        else :
            IsAccepted = [False]
            CheckString(transitions ,final_states , String , initial_state , IsAccepted)
            if IsAccepted[0] :
                print('Accepted')
            else :
                print('Rejected')

phase3('samples\\phase3-sample\\in\\input2.json')