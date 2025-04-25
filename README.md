# ITAM Primavera 2025 - Tarea de Normalización

---

## Configuración

Este proyecto no tiene dependencias adicionales de Python, por lo que no es 
necesario crear un ambiente virtual. Está desarollado y probado con Python 3.13,
pero debe funcionar con 3.8 o superior.

## Supuestos Realizados

- Los atributos en una dependencia funcional o multivaluada son representados como instancias de la clase `Attribute`.
- Se considera que una dependencia funcional es trivial si todos los atributos del lado derecho están contenidos en el lado izquierdo.
- Se considera que una dependencia multivaluada es trivial si el lado derecho está contenido en el lado izquierdo **o** si la unión del lado izquierdo y derecho equivale al encabezado completo.
- Para evaluar si una relvar está en BCNF, se verifica que todas las dependencias funcionales no triviales tengan un determinante que sea superllave.
- Para evaluar si una relvar está en 4NF, se aplica el mismo criterio pero sobre las dependencias multivaluadas.

## Ejemplos de Uso

```python
from normalization.components import Attribute, FunctionalDependency, MultivaluedDependency, Relvar
from normalization.algorithms import closure, is_superkey, is_key, is_relvar_in_bcnf, is_relvar_in_4nf

# Definición de atributos
A = Attribute("A")
B = Attribute("B")
C = Attribute("C")

# Dependencias funcionales
fd1 = FunctionalDependency("{A}->{B}")
fd2 = FunctionalDependency("{B}->{C}")

# Dependencia multivaluada
mvd1 = MultivaluedDependency("{A}->->{B}")

# Cierre de A
closure({A}, {fd1, fd2})  # Devuelve {A, B, C}

# Verificar superllave y llave
is_superkey({A}, {A, B, C}, {fd1, fd2})  # True
is_key({A}, {A, B, C}, {fd1, fd2})       # True

# Verificar formas normales
relvar = Relvar(heading=["A", "B", "C"], functional_dependencies=[fd1, fd2], multivalued_dependencies=[mvd1])
is_relvar_in_bcnf(relvar)  # False (porque B->C y B no es superllave)
is_relvar_in_4nf(relvar)   # False (porque A->->B no es trivial y A no es superllave)

