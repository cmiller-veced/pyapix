# The Task

Given: 
We need a good way to prove that `pyapix' does the right thing.
We need to hit lots of endpoints with lots of data and verify the results.
On lots of APIs.
We need to hit individual endpoints.
We need to hit a sequence of endpoints, thus doing meaningful work.
We notice that Postman does exactly this.
We notice that our system is very similar to Postman because
- (endpoint, verb)-centric
- Domain-based: the solution domain models the problem domain in language and structure
- This is a happy accident because I noticed (like Postman and Swagger) that the
  business domain is (endpoint, verb)-centric.

My first thought was to leverage Postman in some way, eg automatically grab data
from Postman collections.  This is still probably a good idea but when I grab
that data I need someplace for it to go.

Create:  
  A system for 
- storing test data by (endpoint, verb)
    - both for single API calls and sequences of calls.
- running the data through the API
- verifying the results
- be able to run any individual or combination
- bonus:  automatically populate it from a Postman file.
- bonus:  automatically populate a Postman file.


## Preliminary Tasks

Research on similar code.
See if there is already a solution, especially in Python.

Now that we have identified the solution as being similar to Postman we can
assume that Postman designers had similar reasoning, and therefore Postman could
be good inspiration for more decisions.

## Alternatives

- Postman

## Why do it this way?

## Tradeoffs

### Benefits

- facilitates communication
- objective artifact
- Like Postman
    - but fully in a programming language
    - Calling multiple APIs is no problems (contrast with Postman)

### Drawbacks

# A new principal / property / acronym


