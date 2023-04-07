from automathon import NFA


class utils:

    # converts all states to the required format
    @staticmethod
    def convertAllstatestoReg(allStates):
        newStatesDict = {}
        print(allStates['startingState'])

        newStatesDict['startingState'] = allStates['startingState']
        # print(newStatesDict)
        for state in allStates:
            if (state != 'startingState'):
                stateInfo = allStates[state]
                newstate = dict()
                for key, value in stateInfo.items():
                    if key == 'isTerminalState' or key == 'epsilon':
                        newstate[key] = value
                    else:
                        # stateInfo[key] = list(value)
                        newstate[value] = key
                    # print('new state info', newstate)
                newStatesDict[state] = newstate
            # else:
            #     print('found starting state, its value is ', allStates[state])

        return newStatesDict

    # converts all states to an intermediate format
    @ staticmethod
    def convertAllstates(allStates):
        allStatesDict = {}
        for state in allStates:
            if state.stateDict.get('isStartState') != None:
                if state.stateDict['isStartState'] == True:
                    allStatesDict['startingState'] = state.name
                del state.stateDict['isStartState']
            allStatesDict[state.name] = state.stateDict

        return allStatesDict

    @ staticmethod
    def drawNFA(allStatesJSON, drawingName="NFA Visualization"):
        nfa_states = set(
            mystate for mystate in allStatesJSON if (mystate != "startingState"))

        statesTuples = [mystate for mystate in allStatesJSON.items() if (
            mystate[0] != "startingState")]
        nfa_input_symbols = set()
        for _, stateinfo in statesTuples:
            for key, value in stateinfo.items():
                if key != 'isTerminalState' and key != 'epsilon':
                    nfa_input_symbols.add(value)
        nfa_final_states = {item for item, value in allStatesJSON.items(
        ) if item != "startingState" and value.get('isTerminalState') and value['isTerminalState'] == True}

        # remove isTerminalState from stateTuples
        for statename, stateinfo in statesTuples:
            if (stateinfo.get('isTerminalState') != None):
                del stateinfo['isTerminalState']
        nfa_initial_state = allStatesJSON["startingState"]
        nfa_transitions = {}
        # print('statesTuples before ', statesTuples)
        for statename, stateinfo in statesTuples:
            # print('statename and stateinfo are')
            # print(statename, stateinfo)
            nfa_transitions[statename] = {
                value: {key} for key, value in stateinfo.items() if key != 'epsilon'}
            for key, value in stateinfo.items():
                if key == 'epsilon':
                    for epsilonState in value:
                        if (nfa_transitions[statename].get("") == None):
                            nfa_transitions[statename][""] = {epsilonState}
                        else:
                            nfa_transitions[statename][""].add(epsilonState)

        # print('state tuples ', statesTuples)
        # print('nfa_states', nfa_states)
        # print('nfa_inputs', nfa_input_symbols)
        # print('nfa_trans', nfa_transitions)
        # print('nfa_init', nfa_initial_state)
        # print('nfa_finals', nfa_final_states)

        automata2 = NFA(nfa_states, nfa_input_symbols,
                        nfa_transitions, nfa_initial_state, nfa_final_states)
        # automata2.view("NFA Visualization")
        automata2.view(drawingName)
        # state tuples  [('S0', {'S1': 'a-c'}), ('S1', {'epsilon': ['S5']}), ('S2', {'S3': 'd'}), ('S3', {'epsilon': ['S5']}), ('S4', {'epsilon': ['S0', 'S2']}), ('S5', {'epsilon': ['S6', 'S7']}), ('S6', {'epsilon': ['S4', 'S7']}), ('S7', {})]
        # nfa_states {'S5', 'S7', 'S6', 'S1', 'S3', 'S0', 'S4', 'S2'}
        # nfa_inputs {'a-c', 'd'}
        # nfa_trans {'S0': {'a-c': 'S1'}, 'S1': {'': {'S5'}}, 'S2': {'d': 'S3'}, 'S3': {'': {'S5'}}, 'S4': {'': {'S0', 'S2'}}, 'S5': {'': {'S7', 'S6'}}, 'S6': {'': {'S7', 'S4'}}, 'S7': {}}
        # nfa_init S6
        # nfa_finals {'S7'}
        # mynfa.show_diagram(None, 'loldiag')
        # mynfa = VisualNFA(
        #     states={'S5', 'S7', 'S6', 'S1', 'S3', 'S0', 'S4', 'S2'},
        #     input_symbols={'a-c', 'd'},
        #     transitions={
        #         'S0': {'a-c': 'S1'},
        #         'S1': {'': {'S5'}},
        #         'S2': {'d': 'S3'},
        #         'S3': {'': {'S5'}},
        #         'S4': {'': {'S0', 'S2'}},
        #         'S5': {'': {'S7', 'S6'}},
        #         'S6': {'': {'S7', 'S4'}},
        #         'S7': {}},
        #     initial_state='S6',
        #     final_states={'S7'},
        # )
        # mynfa.show_diagram(None, 'loldiag')


# states = {'s5', 's7', 's6', 's1', 's3', 's0', 's4', 's2'}
# input_symbols = {'a-c', 'd'}
# transitions = {
#     's0': {'a-c': {"s1"}},
#     's1': {'': {'s5'}},
#     's2': {'d': {'s3'}},
#     's3': {'': {'s5'}},
#     's4': {'': {'s0', 's2'}},
#     's5': {'': {'s7', 's6'}},
#     's6': {'': {'s7', 's4'}},
#     's7': {}
# }
# initial_state = "s6"
# final_states = {"s7"}
# automata2 = NFA(states, input_symbols,
#                 transitions, initial_state, final_states)
# # automata2.view("NFA Visualization")
# automata2.view("NFA Visualization")
