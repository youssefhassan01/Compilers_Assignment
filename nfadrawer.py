from automata.fa.nfa import NFA
from visual_automata.fa.nfa import VisualNFA
from automata.fa.dfa import DFA
from visual_automata.fa.dfa import VisualDFA

# { S0 :
# {'isTerminalState': False, 'S1': 'a-c'}
# }
# { S1 :
# {'isTerminalState': False, 'epsilon': ['S5']}
# }

# { S2 :
# {'isTerminalState': False, 'S3': 'd'}
# }

# { S3 :
# {'isTerminalState': False, 'epsilon': ['S5']}
# }

# { S4 :
# {'isTerminalState': False, 'epsilon': ['S0', 'S2']}
# }

# { S5 :
# {'isTerminalState': False, 'epsilon': ['S6', 'S7']}
# }
# { S6 :
# {'isTerminalState': False, 'isStartState': True, 'epsilon': ['S4', 'S7']}
# }

# { S7 :
# {'isTerminalState': True}
# }


class NFAdrawer:

    @staticmethod
    def drawNFA(allStates):
        nfa_states = set(allStates.keys())
        nfa_input_symbols = {
            value for key, value in allStates.values().items() if key != 'isTerminalState' and key != 'isStartState' and key != 'epsilon'}
        nfa_initial_state = {item for item, value in allStates.items(
        ) if value.get('isStartState') and value['isStartState'] == True}
        nfa_final_states = {item for item, value in allStates.items(
        ) if value.get('isTerminalState') and value['isTerminalState'] == True}
        nfa_transitions = {}
        for state, stateinfo in allStates.items():
            for key, value in stateinfo.items():
                if key != 'isTerminalState' and key != 'isStartState' and key != 'epsilon':
                    nfa_transitions[state][value] = key
                if key == 'epsilon':
                    nfa_transitions[state][""] = key

        mynfa = VisualNFA(
            states=nfa_states,
            input_symbols=nfa_input_symbols,
            transitions=1,
            initial_state=nfa_initial_state,
            final_states=nfa_final_states,
        )
        mynfa.show_diagram(None, 'loldiag')
        # pass
        # nfa = VisualDFA(
        #     states={"q0", "q1", "q2", "q3", "q4"},
        #     input_symbols={"0", "1"},
        #     transitions={
        #         "q0": {"0": "q3", "1": "q1"},
        #         "q1": {"0": "q3", "1": "q2"},
        #         "q2": {"0": "q3", "1": "q2"},
        #         "q3": {"0": "q4", "1": "q1"},
        #         "q4": {"0": "q4", "1": "q1"},
        #     },
        #     initial_state="q0",
        #     final_states={"q2", "q4"},
        # )

        # nfa.show_diagram(None, 'loldiag')
