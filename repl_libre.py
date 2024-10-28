# Interactive repl
# #########################################################################

from api_libre import *
import cmd, sys
from turtle import *
import readline
import os
import httpx

# TODO: try cmd2 in place of cmd.
#import cmd2
#import gnureadline

histfile = os.path.expanduser('~/.trans_history')
histfile_size = 1000000


def translate(params):
    endpoint = '/translate'
    api_base = local.api_base.libre
    with httpx.Client(base_url=api_base) as client:
        r = client.post(endpoint, params=params)
        assert r.status_code == 200
    return r.json()


def es2ingles(phrase):
    params = {'q': phrase, 'source': 'es', 'target': 'en'}
    endpoint = '/translate'
    api_base = local.api_base.libre
    with httpx.Client(base_url=api_base) as client:
        r = client.post(endpoint, params=params)
    return r.json()['translatedText']

def en2spanish(phrase):
    params = {'q': phrase, 'source': 'en', 'target': 'es'}
    endpoint = '/translate'
    api_base = local.api_base.libre
    with httpx.Client(base_url=api_base) as client:
        r = client.post(endpoint, params=params)
    return r.json()['translatedText']


class TurtleShell(cmd.Cmd):
    intro = 'Welcome to the trans shell.   Type help or ? to list commands.\n'
    prompt = '(trans) '
    file = None
    mode = 'es'
    mode_map = dict(es=es2ingles, en=en2spanish)

    
# TODO: how to save cmd.Cmd history separate from ordinary python history.
#     # Saves regular python in addition to the cmd loop.
#     def preloop(self):
#         if readline and os.path.exists(histfile):
#             readline.read_history_file(histfile)
#  
#     def postloop(self):
#         if readline:
#             readline.set_history_length(histfile_size)
#             readline.write_history_file(histfile)


    # ----- commands -----
    def do_mode(self, arg):
        if arg:
            self.mode = arg
        msg = f'the current mode is : {self.mode}'
        print(msg)

    def default(self, arg):
        func = self.mode_map[self.mode]
        print(func(arg))

    def do_exit(self,*args):
        return True


if __name__ == '__main__': 
    TurtleShell().cmdloop()


# ['/detect', '/frontend/settings', '/languages', '/suggest', '/translate', '/translate_file'])

# def get_component_schemas_libre():    #  # TODO: rename func
#     rs = raw_swagger(local.swagger.libre)
#     with_refs = jsonref.loads(json.dumps(rs))
#     return with_refs['definitions']

def languages():
    endpoint = '/languages'
    api_base = local.api_base.libre
    with httpx.Client(base_url=api_base) as client:
        r = client.get(endpoint, params=params)
        assert r.status_code == 200
    return r.json()


