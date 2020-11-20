from pomidor.pomidor_init import BrowserInit, PomidorObjAndURL, Pom
from pomidor.actions import ForwardAction, BackwardAction

# pomi = BrowserInit("Chrome", 'https://pomidor-automation.com/')
# driver = pomi.define_browser()
# with driver as d:
#     d.get('https://pomidor-automation.com/practice/')

act = ForwardAction()
bact = BackwardAction()
backward_action_dict = bact.backward_actions_dictionary
forward_action_dict = act.forward_action_dictionary

d = backward_action_dict.keys()
print(d)

for item in forward_action_dict.values():
    print(item)

if "click()" in forward_action_dict.keys():
    print("yay!")


