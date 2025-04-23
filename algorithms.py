from .components import FunctionalDependency, Attribute, Relvar


def closure(attributes: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> set[Attribute]:
    # TODO: Actividad 3
    raise NotImplementedError()


def is_superkey(attributes: set[Attribute], heading: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> bool:
    # TODO: Actividad 4
    raise NotImplementedError()


def is_key(attributes: set[Attribute], heading: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> bool:
    # TODO: Actividad 5
    raise NotImplementedError()


def is_relvar_in_bcnf(relvar: Relvar):
    # TODO: Actividad 6
    raise NotImplementedError()


def is_relvar_in_4nf(relvar: Relvar):
    # TODO: Actividad 7
    raise NotImplementedError()
