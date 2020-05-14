from graphviz import Digraph
import numpy as np
import re


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

    def set_transition_matrix(self):
        for i in range(self.transition_matrix.shape[0]):
            for j in range(self.transition_matrix.shape[1]):
                self.transition_matrix[i][j] = ''

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

        for i in self.states:
            for j in self.states:
                if self.transition_matrix[i][j] != '':
                    gr.edge(str(i), str(j), self.transition_matrix[i][j])

        gr.attr(label=f'\n\n{label}')
        gr.render(name, view=True)

    def get_intermediate_states(self):
        return [state for state in self.states if state != self.init_state and state not in self.final_states]

    def get_previous_states(self, state):
        states = []
        for pred in self.states:
            if self.transition_matrix[pred][state] != '' and pred != state:
                states.append(pred)
        return states

    def get_next_states(self, state):
        states = []
        for foll in self.states:
            if self.transition_matrix[state][foll] != '' and foll != state:
                states.append(foll)
        return states

    def iterate(self, expr):
        if len(expr) > 1:
            expr = '(' + expr + ')' + '*'
        elif len(expr) == 1:
            expr = expr + '*'
        return expr

    def get_loop(self, state):
        expr = self.transition_matrix[state][state]
        expr = self.iterate(expr)
        return expr

    def set_braces(self, expr):
        new_expr = expr
        while ('(' in new_expr):
            new_expr = re.sub(r'\([0-1+*]*\)', '', new_expr)
        if '+' in new_expr and new_expr != '':
            expr = '(' + expr + ')'
        return expr

    def concat(self, exprs):
        for i in range(len(exprs)):
            exprs[i] = self.set_braces(exprs[i])
        expr = ''.join(exprs)
        return expr

    def union(self, exprs):
        exprs = [expr for expr in exprs if expr != '']
        return '+'.join(exprs)

    def to_regex(self):
        inter_states = self.get_intermediate_states()
        trans_func = self.transition_matrix.copy()

        for inter in inter_states:
            previous_states = self.get_previous_states(inter)
            following_states = self.get_next_states(inter)

            for prev in previous_states:
                for foll in following_states:
                    inter_loop = self.get_loop(inter)
                    inter_to_foll = self.concat([inter_loop, trans_func[inter][foll]])
                    prev_to_foll = self.concat([trans_func[prev][inter], inter_to_foll])
                    trans_func[prev][foll] = self.union([trans_func[prev][foll], prev_to_foll])
            for prev in previous_states:
                trans_func[prev][inter] = ''
            for foll in following_states:
                trans_func[inter][foll] = ''

        init_loop = self.get_loop(self.init_state)
        init_to_final = trans_func[self.init_state][self.final_states[0]]
        final_loop = self.get_loop(self.final_states[0])
        final_to_init = trans_func[self.final_states[0]][self.init_state]
        if self.final_states[0] == self.init_state:
            return init_loop
        regex = ''
        if len(init_to_final) > 0:
            regex = self.concat([init_loop, init_to_final, final_loop])
        else:
            return ''
        if len(final_to_init) > 0:
            regex = self.union([regex, self.concat(
                [self.iterate(self.concat([init_loop, init_to_final, final_loop, final_to_init])), init_to_final,
                 final_loop])])
        return regex


def main():
    nstates = input('Enter the number of states in your DFA: ')
    nstates = int(nstates)
    final_states = list(map(int, input('Enter the final states: ').split()))
    next_states_by_0 = list(map(int, input('Enter the next states by 0: ').split()))
    next_states_by_1 = list(map(int, input('Enter the next states by 1: ').split()))

    # nstates = 3
    # final_states = [2]
    # next_states_by_0 = [1, 1, 0]
    # next_states_by_1 = [2, 2, 2]

    regex = ''
    for f in final_states:
        dfa = DFA(nstates, [f], next_states_by_0, next_states_by_1)
        reg = dfa.to_regex()
        if reg != '':
            regex += '+' + reg

    dfa = DFA(nstates, final_states, next_states_by_0, next_states_by_1)
    dfa.draw_graph(regex[1:], 'DFA')

    #print(regex[1:])


if __name__ == '__main__':
    main()
