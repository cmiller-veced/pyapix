from types import SimpleNamespace
import typing

from pyapix.tool.tools import parsed_file_or_url

count = 0  # for assigning sequential ID to service_request.


class Sequence:
    """A sequence of calls to one or more API services.
    Leaving `call` in the service_request instead of Sequence is a good move.  
    Makes calling multiple services trivial.
    """
    auth = None

    def __init__(self, rseq):
        self.rseq = rseq   # list of requests

    def run_seq(self):
        for req in self.rseq:
            req.run(1)

    def show_names(self):
        for req in self.rseq:
            msg = f'{req.name:<22} {req.endpoint} {req.verb}'
            print(f'{msg:<55} {req.tested}')


import time
class PostTestFailure(Exception): pass


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

        def run(i):
          try:
            print(f'=========== {i} running request... {name}')
            # TODO: optional validation here.
            response = client.call(endpoint, verb, args)
            nonlocal self
            try:
                # TODO: this retry logic is ugly.  FIX.
                self.tested = post_test(response)
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


def sequence_creator(client, test_data):
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
            globs = {key: test_data[key] for key in requires}
            raw_code = dct['post_test']['code']
            exec(dct['post_test']['code'], locals=dct, globals=globs) # eek!
            pr = service_request(**dct) 
            out_seq.append(pr)
        return Sequence(out_seq)
      finally:
        globals().update(locals())
    return create_sequence


def run_seq(sequences):
    for seq in sequences:
        seq.show_names()
        seq.run_seq()
        seq.show_names()
        print('\n'.join(['*'*55]*4))
        print()

