from types import SimpleNamespace
import typing

from pyapix.apis.tools import parsed_file_or_url

count = 0  # for assigning sequential ID to service_request.


class Sequence:
    """A sequence of calls to one or more API services.
    It turns out that leaving `call` in the service_request instead of Sequence
    is a good move.  
    Makes calling multiple services trivial.
    And is an advantage over Postman.
    """
    local = {}
    auth = None

    def __init__(self, rseq):
        self.rseq = rseq   # list of requests

    def run_seq(self):
        for req in self.rseq:
            req.run()

    def show_names(self):
        for req in self.rseq:
            msg = f'{req.name:<22} {req.endpoint} {req.verb}'
            print(f'{msg:<55} {req.tested}')


def request_for_service(call, _validator):
    # TODO: NOTE _validator is unused.
    # Options...
    #       - rm _validator
    #       - use _validator  (optionally)
    # TODO: btw.   Much of auth goes here.
    # Quick way to ensure a dict with only specific keys.
    # def arequest(name, endpoint, verb, args, post_test=lambda _:None):
    # Originally required parameters in particular order.
    # Changing to all keyword args fixed that.
    def arequest(name='', endpoint='', verb='', args=(), post_test=lambda _:None):
        global count
        count += 1
        secret_id = count
        tested = 'untested'
        self = SimpleNamespace(locals())
        def run():
            print(f'=========== running request... {name}')
            # TODO: optional validation here.
            response = call(endpoint, verb, args)
            nonlocal self
            self.tested = post_test(response)
            return tested
        self.run = run
        return self
    return arequest


def sequence_creator(call, _validator, fname):
    # TODO: fname does NOT belong here!
    # And maybe call and _validator can be eliminated.
    # 
    # The whole thing is petstore-centric.
    # SOLUTION:  WORMS+OBIS+ProteinDB
    def create_sequence(pet_seq_name):
        service_request = request_for_service(call, _validator)
        # TODO: problem.
        # This here limits a sequence to a single service.
        # Which is maybe not such a problem.
        # Multi-service sequences can be made by adding multiple single-service
        # sequences.
        info = parsed_file_or_url(fname)
        seq = []
        i = 0
        for dct in info[pet_seq_name]:
            i += 1
            requires = dct['post_test']['requires']
            globs = {key: info[key] for key in requires}
            exec(dct['post_test']['code'], locals=dct, globals=globs) # eek!
            pr = service_request(**dct) 
            seq.append(pr)
    #        if i > 3: break
        return Sequence(seq)
    return create_sequence


def test_seq(sequences):
    for seq in sequences:
        seq.show_names()
        seq.run_seq()
        seq.show_names()
        print('\n'.join(['*'*55]*4))
        print()



