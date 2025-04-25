from .components import FunctionalDependency, Attribute, Relvar, MultivaluedDependency

def closure(attributes: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> set[Attribute]:
    """
    Calcula el cierre de un conjunto de atributos dados un conjunto de dependencias funcionales.
    
    El cierre de un conjunto de atributos X (denotado como X⁺) es el conjunto de todos los atributos
    que son funcionalmente dependientes de X. Es decir, todos los atributos que pueden ser determinados
    a partir de X usando las dependencias funcionales dadas.
    
    Algoritmo:
    1. Inicializar el cierre con el conjunto de atributos dado.
    2. Mientras se sigan añadiendo atributos al cierre:
       a. Para cada dependencia funcional A -> B:
          i. Si el determinante A está completamente incluido en el cierre actual,
             añadir todos los atributos dependientes B al cierre.
    
    Args:
        attributes (set[Attribute]): Conjunto de atributos inicial para calcular su cierre.
        functional_dependencies (set[FunctionalDependency]): Conjunto de dependencias funcionales.
    
    Returns:
        set[Attribute]: El cierre completo del conjunto de atributos (X⁺).
    """
    # Inicializar el cierre con los atributos iniciales
    closure_set = set(attributes)
    changed = True
    
    # Continuar mientras se sigan añadiendo nuevos atributos al cierre
    while changed:
        changed = False
        for fd in functional_dependencies:
            # Si el determinante (lado izquierdo) está contenido en el cierre actual
            if fd.determinant.issubset(closure_set):
                # Obtener los atributos dependientes que aún no están en el cierre
                new_attributes = fd.dependant - closure_set
                if new_attributes:
                    # Añadir los nuevos atributos al cierre
                    closure_set.update(new_attributes)
                    changed = True  # Se agregaron nuevos atributos, continuar el proceso
    
    return closure_set


def is_superkey(attributes: set[Attribute], heading: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> bool:
    """
    Determina si un conjunto de atributos es una superclave.
    
    Una superclave es un conjunto de atributos que determina funcionalmente a todos
    los demás atributos del encabezado de la relación. En otras palabras, es un conjunto
    de atributos cuyo cierre contiene todos los atributos del encabezado.
    
    Args:
        attributes (set[Attribute]): Conjunto de atributos a evaluar como superclave.
        heading (set[Attribute]): Conjunto total de atributos de la relación (encabezado).
        functional_dependencies (set[FunctionalDependency]): Conjunto de dependencias funcionales.
    
    Returns:
        bool: True si el conjunto de atributos es una superclave, False en caso contrario.
    """
    # Un conjunto es superclave si su cierre contiene todos los atributos del encabezado
    # Es decir, si el cierre es un superconjunto del encabezado
    return closure(attributes, functional_dependencies).issuperset(heading)


def is_key(attributes: set[Attribute], heading: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> bool:
    """
    Determina si un conjunto de atributos es una clave (llave) mínima.
    
    Una clave es una superclave minimal, es decir, una superclave a la que no se le puede
    quitar ningún atributo sin perder la propiedad de ser superclave. En términos formales,
    un conjunto de atributos K es clave si:
    1. K es una superclave (determina funcionalmente todos los atributos)
    2. No existe un subconjunto propio de K que también sea superclave
    
    Args:
        attributes (set[Attribute]): Conjunto de atributos a evaluar como clave.
        heading (set[Attribute]): Conjunto total de atributos de la relación (encabezado).
        functional_dependencies (set[FunctionalDependency]): Conjunto de dependencias funcionales.
    
    Returns:
        bool: True si el conjunto de atributos es una clave, False en caso contrario.
    """
    # Verificar primero si es superclave
    if not is_superkey(attributes, heading, functional_dependencies):
        return False
    
    # Verificar que sea minimal (irreducible)
    # Para cada atributo, verificamos si podemos eliminarlo y seguir teniendo una superclave
    for attr in attributes:
        # Crear un conjunto sin el atributo actual
        reduced_set = attributes - {attr}
        # Si el conjunto reducido sigue siendo superclave, entonces el conjunto original no es minimal
        if is_superkey(reduced_set, heading, functional_dependencies):
            return False
    
    # Si es superclave y no se puede reducir, entonces es una clave
    return True


def is_relvar_in_bcnf(relvar: Relvar) -> bool:
    """
    Verifica si una relación está en Forma Normal de Boyce-Codd (BCNF).
    
    Una relación está en BCNF si para cada dependencia funcional no trivial X -> Y,
    X es una superclave. En otras palabras, toda dependencia funcional está determinada
    por una superclave.
    
    Algoritmo:
    1. Para cada dependencia funcional en la relación:
       a. Si la dependencia no es trivial y el determinante no es superclave,
          entonces la relación no está en BCNF.
    
    Args:
        relvar (Relvar): Relación que contiene el encabezado y las dependencias.
    
    Returns:
        bool: True si la relación está en BCNF, False en caso contrario.
    """
    for fd in relvar.functional_dependencies:
        # Una dependencia viola BCNF si:
        # 1. No es trivial (el lado derecho no está completamente en el lado izquierdo)
        # 2. El lado izquierdo (determinante) no es una superclave
        if not fd.is_trivial() and not is_superkey(fd.determinant, relvar.heading, relvar.functional_dependencies):
            return False
    
    # Si no hay violaciones, la relación está en BCNF
    return True


def is_relvar_in_4nf(relvar: Relvar) -> bool:
    """
    Verifica si una relación está en Cuarta Forma Normal (4NF).
    
    Una relación está en 4NF si está en BCNF y además, para cada dependencia multivaluada
    no trivial X ->-> Y, X es una superclave.
    
    Algoritmo:
    1. Verificar si la relación está en BCNF (requisito previo para 4NF).
    2. Para cada dependencia multivaluada en la relación:
       a. Si la dependencia no es trivial y el determinante no es superclave,
          entonces la relación no está en 4NF.
    
    Args:
        relvar (Relvar): La relación a verificar.
    
    Returns:
        bool: True si la relación está en 4NF, False en caso contrario.
    """
    # Primero verificamos que esté en BCNF (requisito para 4NF)
    if not is_relvar_in_bcnf(relvar):
        return False
    
    # Luego verificamos las dependencias multivaluadas
    for mvd in relvar.multivalued_dependencies:
        # Una dependencia multivaluada viola 4NF si:
        # 1. No es trivial
        # 2. El determinante no es una superclave
        if not mvd.is_trivial(relvar.heading) and not is_superkey(mvd.determinant, relvar.heading, relvar.functional_dependencies):
            return False
    
    # Si no hay violaciones, la relación está en 4NF
    return True
