# Grab code from example/test and insert into documentation template.
# This way we know that the code appearing in documentation is correct.
#

import inspect
from jinja2 import Environment, select_autoescape 
from pyapix.examples import test_worms

def go():
    # TODO: 
    # Execute the test code.

    # Get test code.
    sc = inspect.getsource(test_worms.test_examples)
    test_code = '\n'.join(sc.split('\n')[1:])

    # Get the template.
    other = 'docs/using_template.md'
    with open(other) as fh:
        raw_other = fh.read()

    # Insert code into template.
    env = Environment(autoescape=select_autoescape())
    template = env.from_string(raw_other)
    stuffs = dict(worms_example=test_code)
    foo = template.render(**stuffs)
    bar = foo.replace('&#39;', '"')

    # Write documentation.
    with open('docs/using_it.md', 'w') as fh:
        fh.write(bar)

    # TODO: 
    # Generate using mkdocs.

go()


