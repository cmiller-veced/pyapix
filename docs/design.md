

### Translation

From json to DAO.  Translation is an interesting programming problem.  But if it
is not your core business, why are you doing it?
There are many things one can say about DAO.  There is one thing I can say for
certain about it.  It is not solving your business problem.

The "best practice" in software engineering is to begin with the assumption that
the data needs to be translated into DAO. This assumption is 

- unwarrented
- ridiculous
- absurd
- unexamined

Assumptions in code should be stated explicitly.
Caveat.  Sometimes DAO is a good approach, or even ideal.  Explain...


### More...


We pull data from swagger and use it.  Unfortunately, swagger files often
contain errors so a pre-processing step(s) is required.

Tests are written BEFORE code.  When tests are written after code the bugs
become baked into the tests.  Fooey on that!

Using swagger as data has multiple benefits.

- no duplication of effort that went into swagger defs
- a record of swagger errors

We do not have to define our data if someone else (the swagger author) has
already done it.  This is a huge benefit.

Our tests will reveal any errors in the swagger.  Errors are corrected in the
pre-processing step.  Errors also generate bug reports to the swagger maintaner.
Given the option of multiple swagger sources we go for the one with fewest
errors and best responsiveness to bug reports.

Swagger is not the only acceptable data source.  It is a good data source
because it is a well-defined json/yaml representation with good documentation.
There are plenty of other good options, for example botocore.  botocore is
a well thought-out system.
The important thing is to have a well-defined, slowly changing interface.  If we
have that we can write code quickly to leverage the API.  If we have competition
that prefers the xxx/marshmallow/pydantic approach of manually defined Python
classes, so much the better.  We will run circles around them.  (read Paul
Graham).

#### why?

The landscape is crowded with Python validation libraries.  Why would I create
another one?  Because...

1.  It's obviously not a definitively solved problem
B.  I have a different way of doing it.

A big part of the new vision is eliminating needless transformation.  So things
like DAOs have no place in it.  Yes, I'm saying a DAO is a needless
transformation.  Maybe not always, but I've yet to see a needful one.  If you
think about it, you will notice that the only benefit of the average DAO is the
dot notation for attribute access.  You don't need DAO for that.  If we need it
we will do it, without resorting to the LCD that is DAO.

- LCD:  lowest common denominator

btw.  It's not so much a data validation library as a set of techniques for
accessing APIs.  Validation is part of it, but by no means the primary focus.
Important, yes, but not the center of the universe.

 # aside
First step is to read swagger / OpenAPI files.
These files are in json/yaml.
We shall take the things we find there and represent them as data.

Next step is to validate data against the swagger.  The tricky part is getting
references.  Worthwhile because it keeps us in the original data format.

Call the APIs.

Other tasks present themselves as we go.  Navigating json data is tedious
without good tools so we create the tools as we go.


# How to do it?   design principles

We follow principles of ...

- the Unix Philosophy
- the Agile Manifesto
- good code
- etc

There are important factors that are routinely ignored in typical Python
programming.  Two of these include...

- do not duplicate effort
- do not transform without justification

If someone else has already defined important data we will not repeat that
effort.  Likewise, when we receive data we will not transform it without a good
reason.  "our programmers like Pydantic" (or other xxx) is not a good reason.

Our target users are people who understand the swagger.  The goal is to remove
the need for the programmer between the data analyst and the data.

### Represent our own data in json too.

- Then we store it in simple text file.
- super easy I/O with Python
- cross-platform.  Totally transferable to other language.  Try that with classes.
 
