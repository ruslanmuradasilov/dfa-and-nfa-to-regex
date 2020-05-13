# import os
# os.environ["Path"] += os.pathsep + 'C:/Program Files (x86)/graphviz-2.38/release/bin/dot.exe'
from graphviz import Digraph
import numpy as np


class DFA:
    def __init__(self, nstates, final_states, next_states_by_0, next_states_by_1):
        self.nstates = nstates
        self.states = [i for i in range(nstates)]
        self.init_state = 0
        self.final_states = final_states
        self.next_states_by_0 = next_states_by_0
        self.next_states_by_1 = next_states_by_1
        self.transition_matrix = np.empty((nstates, nstates), dtype=object)
        self.set_transition_matrix()
        pass

    def set_transition_matrix(self):
        for i in range(self.transition_matrix.shape[0]):
            self.transition_matrix[i][self.next_states_by_0[i]] = '0'

        for i in range(self.transition_matrix.shape[0]):
            if self.transition_matrix[i][self.next_states_by_1[i]] == '0':
                self.transition_matrix[i][self.next_states_by_1[i]] = '0+1'
            else:
                self.transition_matrix[i][self.next_states_by_1[i]] = '1'

    def draw_graph(self, label, name):
        gr = Digraph(format='png')

        gr.attr('node', shape='point')  # точка входа
        gr.node('entrance')

        for i in self.states:
            if i in self.final_states:
                gr.attr('node', shape='doublecircle', color='blue', style='')
            # elif i == self.init_state:
            #     gr.attr('node', shape='circle', color='black', style='')
            else:
                gr.attr('node', shape='circle', color='black', style='')
            gr.node(str(i))
            if i == self.init_state:
                gr.edge('entrance', str(i), 'start')

        # for k1, v1 in self.transition_dict.items():
        #             for k2, v2 in v1.items():
        #                 if str(v2) != 'ϕ':
        #                     gr.edge(str(k1), str(k2), str(v2))

        gr.attr(label=label)
        # gr.render(name, view=True)

    def to_regex(self):
        pass


def main():
    # nstates = input('Enter the number of states in your DFA: ')
    # nstates = int(nstates)
    # final_states = list(map(int, input('Enter the final states: ').split()))
    # next_states_by_0 = list(map(int, input('Enter the next states by 0: ').split()))
    # next_states_by_1 = list(map(int, input('Enter the next states by 1: ').split()))

    nstates = 3
    final_states = [0, 2]
    next_states_by_0 = [0, 1, 2]
    next_states_by_1 = [0, 1, 2]

    dfa = DFA(nstates, final_states, next_states_by_0, next_states_by_1)
    dfa.draw_graph('00000', 'DFA')
    print(dfa.transition_matrix)


if __name__ == '__main__':
    main()
