from dataclasses import dataclass
from threading import Lock
from typing import Any, Dict, List
from deafadder_container.ContainerException import InstanceNotFound, MultipleAutowireReference, \
    AnnotatedDeclarationMissing

DEFAULT_INSTANCE_NAME = "default"
import inspect
import ast


@dataclass
class _NamedInstance:
    name: str
    instance: Any


class Component(type):
    _instances: Dict[Any, List[_NamedInstance]] = {}
    _lock: Lock = Lock()

    def __call__(cls, instance_name: str = DEFAULT_INSTANCE_NAME, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = []
            if instance_name not in cls._known_instance_name_for_class():
                new_instance = super().__call__(*args, **kwargs)
                auto = _Autowire(new_instance)
                for autowire_candidate in auto.autowire_triplet_candidates:
                    setattr(new_instance, autowire_candidate[0], Component.get(autowire_candidate[2], autowire_candidate[1]))
                cls._instances[cls].append(_NamedInstance(name=instance_name, instance=new_instance))
        container_entry = cls._get_entry_for_name(instance_name)
        return container_entry.instance

    def get(cls, instance_name: str = DEFAULT_INSTANCE_NAME):
        if cls in cls._instances and instance_name in cls._known_instance_name_for_class():
            return cls._get_entry_for_name(instance_name).instance
        else:
            raise InstanceNotFound(f"Unable to find an instance for {cls} with name '{instance_name}'")

    def delete(cls, instance_name: str = DEFAULT_INSTANCE_NAME):
        with cls._lock:
            if cls in cls._instances and instance_name in cls._known_instance_name_for_class():
                cls._instances[cls] = list(filter(lambda i: i.name != instance_name, cls._instances[cls]))
            else:
                raise InstanceNotFound(f"Unable to find an instance for {cls} with name '{instance_name}'")

    def delete_all(cls):
        with cls._lock:
            if cls in cls._instances:
                cls._instances.pop(cls)

    def _known_instance_name_for_class(cls) -> List[str]:
        return [i.name for i in cls._instances[cls]]

    def _get_entry_for_name(cls, instance_name) -> _NamedInstance:
        return next(filter(lambda i: i.name == instance_name, cls._instances[cls]))


class _Autowire:
    autowire_triplet_candidates = []
    _autowire_candidates = []
    _autowire_non_default_candidates = []
    _autowire_default_candidates = []
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
            raise AnnotatedDeclarationMissing("Element to autowire should be defined and annotated at class level.")

        all_autowire_candidate = {i[0]:i[1] for i in self._autowire_candidates}
        self._autowire_non_default_candidates = [(i[0], i[1], all_autowire_candidate[i[0]]) for i in flattened_args]

    @staticmethod
    def _count_name_occurrence(names: list) -> dict:
        occurrences = {name: 0 for name in set(names)}
        for name in names:
            occurrences[name] = occurrences[name] + 1
        return occurrences

    def _infer_autowire_default_candidates(self):
        non_default = [i[0] for i in self._autowire_non_default_candidates]
        all_candidates = [i[0] for i in self._autowire_candidates]
        default_candidates = set(all_candidates) - set(non_default)
        all_candidates_a_dict = {i[0]:i[1] for i in self._autowire_candidates}
        self._autowire_default_candidates = [(i, DEFAULT_INSTANCE_NAME, all_candidates_a_dict[i]) for i in default_candidates]


def _get_init_decorators(cls):
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
