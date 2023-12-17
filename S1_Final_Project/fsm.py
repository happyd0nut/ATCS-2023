"""
@author: Ms. Namasivayam
"""

class FSM:
    def __init__(self, initial_state):
        # Dictionary (input_symbol, current_state) --> (action, next_state).
        self.state_transitions = {}
        self.current_state = initial_state

    def add_transition(self, input_symbol, state, action=None, next_state=None):
        self.state_transitions[input_symbol, state] = (action, next_state)

    def get_transition(self, input_symbol, state):
        return self.state_transitions[input_symbol, state]

    def process(self, input_symbol):
        action, new_state = self.get_transition(input_symbol, self.current_state)
        if new_state != None:
            self.current_state = new_state
        
        if action != None:
            action()