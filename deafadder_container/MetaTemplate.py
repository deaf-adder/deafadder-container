import inspect
import ast
import logging

from dataclasses import dataclass
from threading import Lock
from typing import Any, Dict, List
from deafadder_container.ContainerException import InstanceNotFound, MultipleAutowireReference, \
    AnnotatedDeclarationMissing

DEFAULT_INSTANCE_NAME = "default"

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


@dataclass
class _NamedInstance:
    """Used internally to represent a named component instance"""
    name: str
    instance: Any


class Component(type):
    _instances: Dict[Any, List[_NamedInstance]] = {}
    _lock: Lock = Lock()

    def __call__(cls, instance_name: str = DEFAULT_INSTANCE_NAME, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                log.debug(f"(__call__) Component {cls} not present, initializing the entry in the instance record.")
                cls._instances[cls] = []
            if instance_name not in cls._known_instance_name_for_class():
                log.debug(f"(__call__) No instance with name '{instance_name}' found for the Component {cls}. Creating it...")
                new_instance = super().__call__(*args, **kwargs)

                log.debug(f"(__call__) Injecting dependencies for {cls} with name '{instance_name}':")
                auto = _AutowireMechanism(new_instance)
                for autowire_candidate in auto.autowire_triplet_candidates:
                    log.debug(f"(__call__) Injecting the dependency {autowire_candidate.component_class} "
                              f"with name '{autowire_candidate.component_instance_name}' in the field '{autowire_candidate.attribute_name}'")
                    setattr(new_instance,
                            autowire_candidate.attribute_name,
                            Component.get(autowire_candidate.component_class,
                                          autowire_candidate.component_instance_name))
                log.debug(f"(__call__) Dependency injection finished for {cls} with name '{instance_name}'")
                cls._instances[cls].append(_NamedInstance(name=instance_name, instance=new_instance))
        container_entry = cls._get_entry_for_name(instance_name)
        log.debug(f"(__call__) Instance found: {container_entry.instance.__class__} with name '{container_entry.name}'.")
        return container_entry.instance

    def get(cls, instance_name: str = DEFAULT_INSTANCE_NAME):
        """Retrieve a Component based on its class and name

        -----------------------------------------------
        Example:
        --------

        class MyCustomComponent(metaclass=Component):
            pass

        Component.get(MyCustomComponent, "name")
        # or
        MyCustomComponent.get("name")
        -----------------------------------------------


        :param instance_name: the name of the instance to retrieve
        :return: the instance with the given name if present
        :raises: InstanceNotFound exception if there is no instance of the given class with the given name
        """
        if cls in cls._instances and instance_name in cls._known_instance_name_for_class():
            log.debug(f"(get) Instance found for {cls} with name '{instance_name}'")
            return cls._get_entry_for_name(instance_name).instance
        else:
            raise InstanceNotFound(f"Unable to find an instance for {cls} with name '{instance_name}'")

    def delete(cls, instance_name: str = DEFAULT_INSTANCE_NAME):
        """Remove one specific instance form the list of possible instance for a given Component.

        -----------------------------------------------
        Example:
        --------

        class MyCustomComponent(metaclass=Component):
            pass

        Component.delete(MyCustomComponent, "name")
        # or
        MyCustomComponent.delete("name")
        -----------------------------------------------

        If a reference to the instance exist somewhere else, this reference will continue to exist.
        However, it will not be possible to retrieve the instance using Component.get() or using
        the autowire mechanism after use of this function.

        This is mostly for test purpose. Since there is very few use case that could need this
        deletion feature in real world scenario.

        :param instance_name: the name of the instance to delete
        :return:  Nothing
        :raises: InstanceNotFound exception if there is no instance of the given class with the given name
        """
        with cls._lock:
            if cls in cls._instances and instance_name in cls._known_instance_name_for_class():
                log.debug(f"(delete) Deleting instance for {cls} with name '{instance_name}'")
                cls._instances[cls] = list(filter(lambda i: i.name != instance_name, cls._instances[cls]))
            else:
                raise InstanceNotFound(f"Unable to find an instance for {cls} with name '{instance_name}'")

    def delete_all(cls) -> None:
        """Remove all instance of the given Component from the possible references.

        -----------------------------------------------
        Example:
        --------

        class MyCustomComponent(metaclass=Component):
            pass

        Component.delete_all(MyCustomComponent)
        # or
        MyCustomComponent.delete_all()
        -----------------------------------------------

        If a reference to the instance exist somewhere else, this reference will continue to exist.
        However, it will not be possible to retrieve the instance using Component.get() or using
        the autowire mechanism after use of this function.

        This is mostly for test purpose. Since there is very few use case that could need this
        deletion feature in real world scenario.

        :return: Nothing
        """
        with cls._lock:
            if cls in cls._instances:
                log.debug(f"(delete_all) Deleting all entries for {cls}. Entries deleted: {cls._instances[cls]}")
                cls._instances.pop(cls)
            else:
                log.debug(f"(delete_all) Nothing to do. No instance found for class {cls}")

    @staticmethod
    def purge():
        """Remove all instance.

        If a reference to the instance exist somewhere else, this reference will continue to exist.
        However, it will not be possible to retrieve the instance using Component.get() or using
        the autowire mechanism after use of this function.

        This is mostly for test purpose. Since there is very few use case that could need this
        deletion feature in real world scenario.

        :return: Nothing
        """
        Component._purge(_Anchor)

    def _purge(cls):
        """Inner function to remove all instance from the dict.

        It is splat this way in order to let the purge function be static, but still access
        class level attribute.
        """
        with cls._lock:
            keys = [k for k,v in cls._instances.items()]
            log.debug(f"(purge) Deleting all instances for the following Component: {keys}")
            for k in keys:
                cls._instances.pop(k)

    def _known_instance_name_for_class(cls) -> List[str]:
        return [i.name for i in cls._instances[cls]]

    def _get_entry_for_name(cls, instance_name) -> _NamedInstance:
        return next(filter(lambda i: i.name == instance_name, cls._instances[cls]))


class _Anchor(metaclass=Component):
    """This is a dummy class only to enable a purge behavior on Component"""
    pass


@dataclass
class _AutowireCandidate:
    """Used internally for autowiring mechanism.
    It groups together the attribute to autowire in the Component, the component instance name to use and the component class to use
    for injection.
    """
    attribute_name: str
    component_instance_name: str
    component_class: Any


class _AutowireMechanism:
    """Package the autowiring mechanism

    This class is used by the Component metaclass in order to detect filed that are Component and can be autowire
    either explicitly (with the autowire decorator) or implicitly (when the component with the default name is
    required).

    It uses ast to parse the Abstract Syntax Tree and inspect to get the source of the Component.

    Each component, at creation time, will be inspected by this class to detect if autowiring is needed and, if so,
    retrieve the correct instance to inject into the correct fields.
    """
    autowire_triplet_candidates: List[_AutowireCandidate] = []
    _autowire_candidates = []
    _autowire_non_default_candidates: List[_AutowireCandidate] = []
    _autowire_default_candidates: List[_AutowireCandidate] = []
    _instance = None

    def __init__(self, instance):
        try:
            instance.__annotations__
        except AttributeError:
            return

        self._instance = instance
        self._infer_autowire_candidates()
        self._infer_explicit_autowire_candidates()
        self._infer_autowire_default_candidates()
        self.autowire_triplet_candidates = [*self._autowire_default_candidates, *self._autowire_non_default_candidates]

    @staticmethod
    def _is_component(clazz) -> bool:
        # type(x) return the metaclass of the class (whatever the inheritance level)
        # so type(x) is either Component or something else in our case
        if type(clazz) is Component:
            return True
        else:
            return False

    def _infer_autowire_candidates(self):
        annotations = self._instance.__annotations__
        self._autowire_candidates = [(k, annotations[k]) for (k, v) in annotations.items()
                                     if not hasattr(self._instance, k)
                                     and self._is_component(v)]

    def _infer_explicit_autowire_candidates(self):
        init_decorators = _get_init_decorators(self._instance.__class__)
        if not init_decorators:
            self._autowire_non_default_candidates = []
            return
        autowire_decorators = init_decorators["autowire"]
        flattened_args = [t for sublist in autowire_decorators for t in sublist]

        all_args_name = [i[0] for i in flattened_args]

        duplicate_args = [name for name, times in self._count_name_occurrence(all_args_name).items() if times > 1]
        if len(duplicate_args) > 0:
            raise MultipleAutowireReference(f"The following arguments are referenced multiple times in autowire: {', '.join(duplicate_args)}")

        annotated_elements = [i[0] for i in self._autowire_candidates]
        not_annotated_elements_in_explicit_autowire = [i for i in all_args_name if i not in annotated_elements]
        if len(not_annotated_elements_in_explicit_autowire) > 0:
            raise AnnotatedDeclarationMissing(f"Elements to autowire '{', '.join(not_annotated_elements_in_explicit_autowire)}'"
                                              f" should be defined and annotated at class level.")

        all_autowire_candidate = {i[0]: i[1] for i in self._autowire_candidates}
        self._autowire_non_default_candidates = [
            _AutowireCandidate(attribute_name=i[0],
                               component_instance_name=i[1],
                               component_class=all_autowire_candidate[i[0]])
            for i in flattened_args
        ]

    @staticmethod
    def _count_name_occurrence(names: list) -> dict:
        """This class is used to count the """
        occurrences = {name: 0 for name in set(names)}
        for name in names:
            occurrences[name] = occurrences[name] + 1
        return occurrences

    def _infer_autowire_default_candidates(self) -> None:
        """Retrieve all field in the component that should be autowired using the default instance if present.

        It does not return any value but store the result inside the _autowire_default_candidates attribute
        """
        non_default = [i.attribute_name for i in self._autowire_non_default_candidates]
        all_candidates = [i[0] for i in self._autowire_candidates]
        default_candidates = set(all_candidates) - set(non_default)
        all_candidates_as_dict = {i[0]:  i[1] for i in self._autowire_candidates}
        self._autowire_default_candidates = [
            _AutowireCandidate(attribute_name=i,
                               component_instance_name=DEFAULT_INSTANCE_NAME,
                               component_class=all_candidates_as_dict[i])
            for i in default_candidates
        ]


def _get_init_decorators(cls):
    """Parse the AST to retrieve all decorator on the __init__ method for a given class"""
    target = cls
    init_decorators = {}

    def visit_function_def(node):
        if node.name != "__init__":
            return
        for n in node.decorator_list:
            decorator_args = []
            name = ''
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
                decorator_args = [(decorator_arg.arg, decorator_arg.value.value) for decorator_arg in n.keywords]
            # to be complete, the decorator without parenthesis should be included. But since we
            # don't really need it, we can ignore it for now
            #
            # Sample code to be complete
            # > else:
            # >    name = n.attr if isinstance(n, ast.Attribute) else n.id

            if name not in init_decorators:
                init_decorators[name] = []
            init_decorators[name].append(decorator_args)

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_function_def
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return init_decorators
