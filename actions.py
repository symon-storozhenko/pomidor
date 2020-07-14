class ForwardAction:
    def __init__(self, action):
        self.forward_action_dictionary = {
            '*click': 'click()',
            '*type': 'send_keys()'
        }[action]

class BackwardAction:
    def __init__(self, action):
        self.backward_actions_dictionary = {
            '*visible': 'is_displayed()',
            '*not visible': 'test'
        }[action]


vector = 'forward_action_dictionary'

act = ForwardAction('*click')

print(act.forward_action_dictionary)
