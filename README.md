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

+ Las pruebas las hicimos en Visual Studio Code y las escribimos en example.py

## Explicación de métodos
1)
Método is_trivial – FunctionalDependency 
Determina si una dependencia funcional 
𝑋 → 𝑌 es trivial, es decir, si todo lo que está en el lado derecho (Y) también está en el izquierdo (X).
- self.determinant: conjunto de atributos en el lado izquierdo.
- self.dependant: conjunto de atributos en el lado derecho.
- Si todos los de dependant están en determinant, entonces es trivial.

2)
Método is_trivial – MultivaluedDependency
Evalúa si X↠Y es trivial. Según teoría de bases de datos:
Es trivial si: 𝑌 ⊆ 𝑋 o 𝑋 ∪ 𝑌 = 𝑅 (todo el encabezado de la tabla)
- Verifico primero si Y está incluido en X.
- Si no, verifico si la unión de X y Y es igual al encabezado completo (heading).

3)
Función closure
Calcula el cierre de un conjunto de atributos usando las dependencias funcionales.
Lógica:
- Empieza con el conjunto dado.
- Recorre las dependencias funcionales.
- Si una dependencia aplica (el lado izquierdo está contenido en el cierre actual), entonces agrega el lado derecho.
- Repite hasta que no se agreguen más atributos.

4)
Función is_superkey
Verifica si un conjunto de atributos determina todo el encabezado.
Lógica:
- Solo compara si el cierre de attributes es igual al encabezado.

5) 
Función is_key
Verifica si un conjunto de atributos es una llave mínima, es decir:
- Determina todo el encabezado (is_superkey)
- No se puede quitar ningún atributo sin perder esa propiedad

6)
Función is_relvar_in_bcnf
Revisa si una relvar (tabla) está en Boyce-Codd Normal Form.
Para toda dependencia funcional no trivial, el lado izquierdo debe ser una superllave.

7)
Función is_relvar_in_4nf
Verifica si una relvar está en Cuarta Forma Normal (4NF).
Igual que BCNF, pero para dependencias multivaluadas:
- Si no es trivial, el lado izquierdo debe ser superllave.

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



