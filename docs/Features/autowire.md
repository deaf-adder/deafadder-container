# Autowire

This is maybe the single most import feature.

Once you have created your `Component`, you will find yourself in a scenario
where your component will need to have access to other components.

A simple example could be a service, dedicated to the orchestration of different services
where each service is a `Component`.

## With default instance

### Service 1:
```python
# service/first.py

import random

from deafadder_container.MetaTemplate import Component


class Service1(metaclass=Component):
    
    stuff = ["stuff1", "stuff2", "no"]
    
    def do_stuff(self):
        return random.choice(self.stuff)

```

### Service 2:
```python
# service/second.py

from deafadder_container.MetaTemplate import Component


class Service2(metaclass=Component):
    
    @staticmethod
    def print_first():
        print("first case")

    @staticmethod
    def print_second():
        print("second case")
```


### Service Orchestrator:

here, we don't need to instantiate the two service since the `Component`
will take care of retrieving suitable candidate for the au injection when
we create the Orchestrator instance.

```python
# orchestrator.py

from deafadder_container.MetaTemplate import Component

from service.first import Service1
from service.second import Service2


class Orchestrator(metaclass=Component):
    
    service1: Service1
    service2: Service2
    
    def handle_scenario(self):
        stuff = self.service1.do_stuff()
        if stuff == "no":
            self.service2.print_second()
        else:
            self.service2.print_first()

```

### Main
and the main function:
```python
# main.py

from service.first import Service1
from service.second import Service2
from orchestrator import Orchestrator


def _initialiaze():
    service1 = Service1()
    service2 = Service2()
    orchestrator = Orchestrator()

    
if __name__ == "__main__":
    _initialiaze()
    
    Orchestrator.get().handle_scenario()

```

## With non default instance

Here, we will take the same `Service1` and `Service2` class as above.
But let imagine that, for whatever reason, we don't want to use the default instances (
the one created without the `instance_name` parameter or with the `default` name).


### Service Orchestrator with autowire:

When you want to inject a specific name instance, we have to tell which named instance
should be injected. To do so, you can use the `autowire` decorator on the `__init__`
method. 

This decorator does not do anything and is only for reference. It use any number of 
key-word argument where the key is the name of the field inside the `Component` and 
the value is the name of the instance you want to inject.


```python
# orchestrator.py

from deafadder_container.MetaTemplate import Component
from deafadder_container.Wiring import autowire

from service.first import Service1
from service.second import Service2


class Orchestrator(metaclass=Component):
    
    service1: Service1
    service2: Service2
    
    #@autowire(service1="named instance")
    #@autowire(service2="other name")
    # or 
    @autowire(service1="named instance", service2="other name")
    def __init__(self):
        pass
    
    def handle_scenario(self):
        stuff = self.service1.do_stuff()
        if stuff == "no":
            self.service2.print_second()
        else:
            self.service2.print_first()

```

### Main
and the main function:
```python
# main.py

from service.first import Service1
from service.second import Service2
from orchestrator import Orchestrator


def _initialiaze():
    service1 = Service1(instance_name="named instance")
    service2 = Service2(instance_name="other name")
    orchestrator = Orchestrator()

    
if __name__ == "__main__":
    _initialiaze()
    
    Orchestrator.get().handle_scenario()

```
