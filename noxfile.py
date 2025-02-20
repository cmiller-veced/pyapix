# https://nox.thea.codes/en/stable/tutorial.html
# ^ The nox docs ^
# Here is a noxfile. >
# Pretty much follows the tutorial.

import os
import nox


def pyfiles(dirname):
    cwd = os.getcwd()
    fnames = [fn for fn in os.listdir('apis') if fn.endswith('.py')]
    return [os.path.join(cwd, dirname, fn) for fn in fnames]


@nox.session
def flake8(session):
    session.install('flake8')
    session.run('flake8', *pyfiles('apis'), *pyfiles('examples'))


# TODO: use ruff instead of flake8 + black + isort + ...
# It is made by the same group that made `uv`.
# Looks to be very nice.
@nox.session
def lint(session):
    session.install('ruff')
    cwd = os.getcwd()
    dir_names = ['apis', 'examples']
    dir_paths = [os.path.join(cwd, dn) for dn in dirs_names]
    session.run('ruff', 'check', *dir_paths)
# https://github.com/astral-sh/ruff
# TODO: NOTE ruff has a buncha configs to go in the pyproject.toml file.

@nox.session
def tests(session):
    session.install("-r", "requirements.txt")
    session.install(".")     # install the apis/ and examples/ directories.
    session.run("pytest")


@nox.session(tags=["fail", "fluff"])
@nox.parametrize("django", ["1.9", "2.0"])
def peps(session, django):
    print('yoohoo peps....... django ==', django)
#    session.install_and_run_script("peps.py")   # it fails.


#@nox.session(python=["3.11", "3.12"])
@nox.session(tags=["fluff"])
def foo(session):
    session.install("flake8")
    print('yoohoo foo')
#    session.run("flake8", env={"FLASK_DEBUG": "1"})  # bar never runs
    session.notify("bar", posargs=[1, 'a'])


@nox.session
def bar(session):
    session.install("flake8")
    print('yoohoo bar', *session.posargs)


