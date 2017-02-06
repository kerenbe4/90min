from controller import *

print('please enter your request in one of the following formats:')
print('/[team-id integer]/matches?match_status=[status<optional>]')
print('/[tournament-name string]/matches?match_status=[status<optional>]')
print('-----------------------------------------------------------------')

query_str = input()
#query_str = '/Premier League/matches?match_status=played'
#query_str = '/Premier League/matches?match_status=upcoming'
#query_str = '/9/matches?match_status='
#query_str = '/4/matches?match_status='

controller = Controller()
print(controller.parse(query_str))

