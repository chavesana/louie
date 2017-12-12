import os
import sys
import random
import louie

def interactive(witclient, bot_name = 'louie_events'):
    # input/raw_input are not interchangeable between Python 2 and 3
    try:
        input_function = raw_input
    except NameError:
        input_function = input

    history = InMemoryHistory()
    while True:
        try:
            message = prompt('You >> ', history=history, mouse_support=True).rstrip()
        except (KeyboardInterrupt, EOFError):
            return

        wit_response = witclient.message(message, {})
        print(wit_response)
        print()
        print('{} >> '.format(bot_name), process_nlp(wit_response))

if __name__ == '__main__':
        interactive(louie.witclient, bot_name='Louie')
