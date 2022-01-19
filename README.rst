.. image:: https://circleci.com/gh/deaf-adder/deafadder-container/tree/master.svg?style=svg&circle-token=16b2bcd2e9f92ee31a92571b05ab75929085ab38
        :target: https://circleci.com/gh/deaf-adder/deafadder-container/tree/master


deafadder-container
===================

    A container library to manage dependencies between services and component *à la spring*
    but using :code:`metaclass`.

This library provide a way to manage :code:`Components` in a python application.
A :code:`Component` being a kind of singleton (meaning, unless specified, it will be a singleton) that can automatically link (inject) dependencies if
those dependencies are other v`Components`.

For those familiar with Java, the base idea comes from Spring where it is easy to inject Components into other Components without having to deal with
the all the manual wiring and object initialization. While this library as been inspired by the autowiring mechanism of Spring, it is still immature,
with a reduced scope and present some limitation (due to :code:`metaclass`). While some limitation are expected to change in future version, it's future is still
uncertain, so use with caution.


Documentation
-------------

Just follow this link: https://deaf-adder.github.io/deafadder-container/#/

Fancy a more example base approach ? The documentation is full of examples and the tests files should be enough to have a better understanding of
what can be achieved.

Expected future developments
----------------------------

- getting rid of the :code:`metaclass` to achieve the same, or similar, result *(why ? Because I'd like to include dependency injection based on ABC class
  which are :code:`metaclass` and one object could not extends an ABC class and be have a :code:`Component` metaclass as well)*
- add a section to present projects build around this library

