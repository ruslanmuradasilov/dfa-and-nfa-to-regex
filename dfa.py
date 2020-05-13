from graphviz import Digraph


class DFA:
    def __init__(self, nstates, final_states, next_states_by_0, next_states_by_1):
        self.nstates = nstates
        self.states = [i for i in range(nstates)]
        self.init_state = 0
        self.final_states = final_states
        self.next_states_by_0 = next_states_by_0
        self.next_states_by_1 = next_states_by_1
        pass

    def draw_graph(self):
        pass

    def to_regex(self):
        pass


def main():
    nstates = input('Enter the number of states in your DFA: ')
    nstates = int(nstates)
    final_states = list(map(int, input('Enter the final states: ').split()))
    next_states_by_0 = list(map(int, input('Enter the next states by 0: ').split()))
    next_states_by_1 = list(map(int, input('Enter the next states by 1: ').split()))

    dfa = DFA(nstates, final_states, next_states_by_0, next_states_by_1)
    dfa.draw_graph()


if __name__ == '__main__':
    main()
