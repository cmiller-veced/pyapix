# The Task

    Given: An OpenAPI / Swagger file with errors.
       Ie.  Does not accurately represent the service
    Return: A correct OpenAPI file (json doc)


## Alternatives


## Why do it this way?

## Tradeoffs

### Benefits

- we can use it to generate the client
- facilitates communication
    - easy to show the OpenAPI publisher 
        - as a bug fix
    - (or anyone else) eg our users.
        - scenario.  We publish the corrected Swagger to our users.  They can
          help us to identify anything we missed.
          MEAB (more eyes are better)
- objective artifact
    - visible to anyone
    - correctable by anyone


### Drawbacks

- more complex (in our code) than ad-hoc patching in code


# A new principal / property / acronym

- MEAB: more eyes are better
- MEMBD:  more eyes means better debugging
- LUD:  Let users debug


# Considerations

Probably will need to learn about swagger versions.
Current code is unaware of swagger versions.  Probably some of the ugliness in
that part of the code is due to version issues.


# Follow-up

We could publish swagger files for web services that do not provide swagger.
That would be a nice public service.



