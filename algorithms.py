from .components import FunctionalDependency, Attribute, Relvar


def closure(attributes: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> set[Attribute]:
    """Calcula el cierre de un conjunto de atributos dado un conjunto de dependencias funcionales."""
    closure_set = set(attributes)
    changed = True
    while changed:
        changed = False
        for fd in functional_dependencies:
            if fd.determinant.issubset(closure_set) and not fd.dependant.issubset(closure_set):
                closure_set.update(fd.dependant)
                changed = True
    return closure_set


def is_superkey(attributes: set[Attribute], heading: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> bool:
    """Determina si el conjunto de atributos es superllave (determina todo el encabezado)."""
    return closure(attributes, functional_dependencies) == heading


def is_key(attributes: set[Attribute], heading: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> bool:
    """Determina si el conjunto de atributos es llave mínima (superllave irreductible)."""
    if not is_superkey(attributes, heading, functional_dependencies):
        return False
    for attr in attributes:
        reduced = attributes - {attr}
        if is_superkey(reduced, heading, functional_dependencies):
            return False
    return True


def is_relvar_in_bcnf(relvar: Relvar):
    # TODO: Actividad 6
    raise NotImplementedError()


def is_relvar_in_4nf(relvar: Relvar):
    # TODO: Actividad 7
    raise NotImplementedError()
