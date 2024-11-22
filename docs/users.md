



#### Target User

- intelligent
- some programming experience / comfort
- issue aware re the API   (possibly the swagger file but probably not).
- manager or data analyst

If a manager...  You may be frustrated with

- fte headcount
- bugs
- slow pace of change

If a data analyst...  You may be frustrated with

- non-intuitive interface
- incomplete interface


#### Javathonic / Simplistic

Simplistic == sadly True 
Ironic

class-based translation is a simplification / approximation of the actual
problem.  Then the business problem is solved on this simplified version and
then the data re-transformed back to original (or some other) format, and we
hope the actual problem is solved.  Often it is almost solved.  Edge cases left
uncovered, etc.

# TODO: insert flow-chart here


#### For Managemnt Eyes Only

Red flags for simplistic code.

- lots of to_dict methods
- validation of an approximation
- x


#### This is not a joke

It is treated as a joke by industry standard but.
Energy given to translation/simplification is energy NOT given to solving the
business problem.

The difference is measurable.

- McCabe cyclomatic complexity
- at the computational level.   (not green)

It simply makes more operations by the computer.  This adds up.  Not green.

btw.  I bet there is a way to measure information density of json data vs class
data.  And I'm betting it turns out json is more dense.  So we transform dense
data in a simplistic way.  Solve the problem using the simplistic
representation, and then re-translate.   ugh.
I propose to work with the actual data instead.

Yes, it's a bit more difficult.  But the advantages accrue as the business
problems get more demanding.


#### When NOT to use it

- fast-changing API
- small projects
- one-off projects
- throw-away code
- short-term projects

#### When to use it

- multiple APIs
- solving unknown problems
- solving problems you have not thought of yet



