class ForwardAction:
    def __init__(self):
        self.forward_action_dictionary = {
            '*click': 'click()',
            '*type': 'send_keys("Yoyo!!!!")'
        }


class BackwardAction:
    def __init__(self):
        self.backward_actions_dictionary = {
            '*visible': 'is_displayed()',
            '*not visible': 'test'
        }


vector = 'forward_action_dictionary'

act = ForwardAction()

print(act.forward_action_dictionary)
