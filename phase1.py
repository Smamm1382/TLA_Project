from ReadFromJson import ReadFromJson
from WriteToJson import WriteToJson
import ast

def Find_Landa_Transition(Current , Transitions : dict , output , IsVisited):
    IsVisited.append(Current)
    output.append(Current)
    Neighbours = []
    if "" in Transitions[Current] :
        Neighbours += (list(ast.literal_eval(str(Transitions[Current][""]))))
    else :
        return
    for x in Neighbours :
        if(x not in IsVisited):
            Find_Landa_Transition(x , Transitions , output , IsVisited)


def phase1(input):
    (states, input_symbols, transitions, initial_state, final_states) = ReadFromJson(input)
    ListOfNodes = []
    IsVisited = []
    templist = []
    unclearNode = []
    Find_Landa_Transition(initial_state , transitions , templist , IsVisited)
    templist.sort()
    newinitialstate = "".join(templist)
    ListOfNodes.append(templist)
    unclearNode.append(templist)
    Transitions = {}
    while(len(unclearNode) > 0) :
        for alphabet in input_symbols :
            tempstate = []
            for states in unclearNode[0] :
                Landalist = []
                IsVisited.clear()
                Find_Landa_Transition(states , transitions , Landalist , IsVisited)
                for s in Landalist :
                    if alphabet in transitions[s] :
                        Landalist2 = list(ast.literal_eval(str(transitions[s][alphabet])))
                        templist2 = []
                        for l in Landalist2 :
                            templist3 = []
                            IsVisited.clear()
                            Find_Landa_Transition(l , transitions , templist3 , IsVisited)
                            templist2 += templist3
                        tempstate += templist2
            if len(tempstate) == 0 :
                tempstate = ["trap"]
            tempstate = list(dict.fromkeys(tempstate))
            tempstate.sort()
            if tempstate not in ListOfNodes :
                ListOfNodes.append(tempstate)
                if "trap" not in tempstate :
                    unclearNode.append(tempstate)
            dictkey = "".join(unclearNode[0])
            if dictkey not in Transitions :
                Transitions[dictkey] = { alphabet : str("".join(tempstate))}
            else :
                Transitions[dictkey][alphabet] = str("".join(tempstate))
        unclearNode.pop(0)
    for i in range(len(ListOfNodes)-1, -1, -1) :
        if isinstance(ListOfNodes[i] , list) :
            ListOfNodes[i].sort()
            ListOfNodes.append("".join(ListOfNodes[i]))
            ListOfNodes.remove(ListOfNodes[i])
    if "trap" in ListOfNodes :
        for x in input_symbols :
            if "trap" not in Transitions :
                Transitions["trap"] = { x : "trap"}
            else :
                Transitions["trap"][x] = "trap"
    ListOfFinalStates = []
    for x in final_states : 
        for y in ListOfNodes :
            if x in y :
                ListOfFinalStates.append(y)
    ListOfNodes.sort()
    WriteToJson(ListOfNodes , input_symbols , Transitions , newinitialstate , ListOfFinalStates , "samples\\phase1-sample\\in\\output2.json")





phase1("samples\\phase1-sample\\in\\input2.json")
