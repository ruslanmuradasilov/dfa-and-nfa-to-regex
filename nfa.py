from graphviz import Digraph
import numpy as np
import re


# https://qastack.ru/cs/2016/how-to-convert-finite-automata-to-regular-expressions - to_regex
# https://graphviz.readthedocs.io/en/stable/index.html# - draw_graph

class DFA:
    def __init__(self, nstates, final_states, transition_matrix):
        self.nstates = nstates
        self.states = [i for i in range(nstates)]
        self.init_state = 0
        self.final_states = final_states
        self.transition_matrix = transition_matrix

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

    def get_previous_states(self, state, trans_func):
        states = []
        for prev in self.states:
            if trans_func[prev][state] != '' and prev != state:
                states.append(prev)
        return states

    def get_next_states(self, state, trans_func):
        states = []
        for next in self.states:
            if trans_func[state][next] != '' and next != state:
                states.append(next)
        return states

    def get_loop(self, state, trans_func):
        expr = trans_func[state][state]
        expr = self.iterate(expr)
        return expr

    def set_braces(self, expr):
        new_expr = expr
        while ('(' in new_expr):
            new_expr = re.sub(r'\([0-1+$*]*\)', '', new_expr)
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

    def iterate(self, expr):
        if len(expr) > 1:
            expr = '(' + expr + ')' + '*'
        elif len(expr) == 1:
            expr = expr + '*'
        return expr

    def to_regex(self):
        inter_states = self.get_intermediate_states()
        trans_func = self.transition_matrix.copy()

        for inter in inter_states:
            previous_states = self.get_previous_states(inter, trans_func)
            following_states = self.get_next_states(inter, trans_func)

            for prev in previous_states:
                for foll in following_states:
                    inter_loop = self.get_loop(inter, trans_func)
                    inter_to_foll = self.concat([inter_loop, trans_func[inter][foll]])
                    prev_to_foll = self.concat([trans_func[prev][inter], inter_to_foll])
                    trans_func[prev][foll] = self.union([trans_func[prev][foll], prev_to_foll])
            for prev in previous_states:
                trans_func[prev][inter] = ''
            for foll in following_states:
                trans_func[inter][foll] = ''

        init_loop = self.get_loop(self.init_state, trans_func)
        init_to_final = trans_func[self.init_state][self.final_states[0]]
        final_loop = self.get_loop(self.final_states[0], trans_func)
        final_to_init = trans_func[self.final_states[0]][self.init_state]
        if self.final_states[0] == self.init_state:
            if init_loop == '':
                return '$'
            return init_loop
        regex = ''
        if len(init_to_final) > 0:
            regex = self.concat([init_loop, init_to_final, final_loop])
        else:
            return ''
        if len(final_to_init) > 0:
            regex = self.union([regex, self.concat(
                [self.iterate(self.concat([init_loop, init_to_final, final_loop, final_to_init, init_loop])),
                 init_to_final, final_loop])])
        return regex


def main():
    fin = open("in")
    nstates = int(fin.readline())
    final_states = list(map(int, fin.readline().split()))

    transition_matrix = np.empty((nstates, nstates), dtype=object)
    for i in range(transition_matrix.shape[0]):
        for j in range(transition_matrix.shape[1]):
            transition_matrix[i][j] = ''

    for line in fin:
        line = line.split()
        if (transition_matrix[int(line[0])][int(line[1])] != ''):
            transition_matrix[int(line[0])][int(line[1])] += '+' + line[2]
        else:
            transition_matrix[int(line[0])][int(line[1])] = line[2]
    fin.close()

    regex = ''
    for f in final_states:
        dfa = DFA(nstates, [f], transition_matrix)
        reg = dfa.to_regex()
        if reg != '':
            regex += '+' + reg

    dfa = DFA(nstates, final_states, transition_matrix)
    dfa.draw_graph(regex[1:], 'NFA')

    # print(regex[1:])


if __name__ == '__main__':
    main()
