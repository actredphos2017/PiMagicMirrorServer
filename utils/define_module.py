from typing import Callable

from utils.pipe import Pipe


class ModuleEntity:
    def __init__(self, main_function: Callable[[Pipe], None], name: str):
        self.main_function = main_function
        self.name = name


def define_module(name: str) -> Callable[[Callable[[Pipe], None]], Callable[[], ModuleEntity]]:
    return lambda main_function: (lambda: ModuleEntity(main_function, name))
