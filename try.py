from PySimpleAutomata import DFA, automata_IO

dfa_example = automata_IO.dfa_json_importer('input.json')

DFA.dfa_completion(dfa_example)
# new_dfa = DFA.dfa_minimization(dfa_example)

automata_IO.dfa_to_dot(dfa_example, 'lol', './')
