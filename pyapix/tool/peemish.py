from types import SimpleNamespace
import typing
import time

from pyapix.tool.tools import parsed_file_or_url
from pyapix.osdu.working_with_postman import insert_params


count = 0  # for assigning sequential ID to service_request.

class PostTestFailure(Exception): pass


class Sequence:
    """A sequence of calls to one or more API services.
    Leaving `call` in the service_request instead of Sequence is a good move.  
    Makes calling multiple services trivial.
    """
    auth = None

    def __init__(self, rseq):
        self.rseq = rseq   # list of requests

    def run_seq(self, env):
        for req in self.rseq:
            req.run(1, env)    # passing 1 for auto-retry.

    def show_names(self):
        for req in self.rseq:
            msg = f'{req.name:<22} {req.endpoint} {req.verb}'
            print(f'{msg:<55} {req.tested}')


def request_for_service(client):
    # TODO: Much of auth goes here.
    def arequest(name='', endpoint='', verb='', args=(), post_test=lambda _:None):
      try:
        # Quick way to ensure a dict with only specific keys.
        global count
        count += 1
        secret_id = count
        tested = 'untested'
        self = SimpleNamespace(locals())

        def run(i, environment):
          try:
            print(f'=========== {i} running request... {name}')
            # TODO: optional validation here.
            # TODO: insert to args from environment here. DONE
            for (nom, value) in args.items():
                if (nom in environment.current) and all(c in value for c in '{}'):
                    ip = insert_params(value, environment.current)
                    if ip != value:
                        args[nom] = ip
            
            response = client.call(endpoint, verb, args)
            fna = response
            nonlocal self
            try:
                # TODO: this retry logic is ugly.  FIX.
#                f = lambda response, environment: post_test(response)
#                self.tested = f(response, environment)
                try:
                    post_test.requires
                except AttributeError:
                    pass
                self.tested = post_test(response, environment)
                # TODO: environment
                # is relevant here.
            except AssertionError as exc:   # sleep before retry
                if i < 7:
                    time.sleep(5*i)
                    run(i+1)
                else:
                    raise PostTestFailure(exc)
            return tested
          finally:
            globals().update(locals())

        self.run = run
        return self
      finally:
        globals().update(locals())
    return arequest


def sequence_creator(client):     
    # TODO: The whole thing is petstore-centric.
    # SOLUTION:  WORMS+OBIS+ProteinDB
    service_request = request_for_service(client)
    # TODO: problem.
    # This limits a sequence to a single service.
    # Which is maybe not such a problem.
    # Multi-service sequences can be made by adding multiple single-service
    # sequences.
    def create_sequence(sequence):
      try:
        out_seq = []
        i = 0
        for dct in sequence:
            i += 1
            requires = dct['post_test']['requires']
            raw_code = dct['post_test']['code']
#            for key in requires:
#                line = f'{key} = {dct[key]}\n'    # NO
#                 line = key + f'= {key}\n'
#                 # TODO: key needs to be substituted from Environment
#                 raw_code = line + raw_code
#            post_test.requires = {key:dct[key] for key in requires}
            exec(raw_code, locals=dct) # eek!
            # TODO: NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO
            # TODO: NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO
            # Rather than exec and keep the function object, simply execute in
            # the presence of an Environment.
            # ?????????????????????
            # TODO: NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO
            # TODO: NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO NO
            pr = service_request(**dct) 
            out_seq.append(pr)
        return Sequence(out_seq)
      finally:
        globals().update(locals())
    return create_sequence


def run_seq(seq, env):
    seq.show_names()
    seq.run_seq(env)
    seq.show_names()
    print('\n'.join(['*'*55]*4))
    print()


