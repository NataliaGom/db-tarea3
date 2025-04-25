from normalization.components import Relvar, FunctionalDependency, MultivaluedDependency, Attribute
from normalization.algorithms import (
    closure,
    is_superkey,
    is_key,
    is_relvar_in_bcnf,
    is_relvar_in_4nf
)

if __name__ == "__main__":
    fd1 = FunctionalDependency("{RFC} -> {Nombre, CP}")
    fd2 = FunctionalDependency("{FolioF} -> {RFC}")
    fd3 = FunctionalDependency("{FolioF} -> {MontoF, IVA, FechaF}")
    fd4 = FunctionalDependency("{FolioF} -> {RegimenF, CFDI}")
    fd5 = FunctionalDependency("{FolioP} -> {MontoP, FechaP}")
    fd6 = FunctionalDependency("{FolioP} -> {FolioF}")
    fd7 = FunctionalDependency("{MontoF} -> {IVA}")

    mvd1 = MultivaluedDependency("{RFC} ->-> {RegimenC}")

    relvar = Relvar(
        heading=["Nombre", "RFC", "CP", "RegimenF", "RegimenC", "CFDI", "FolioF", "MontoF", "IVA", "FechaF", "Producto", "FolioP", "MontoP", "FechaP"],
        functional_dependencies=[fd1, fd2, fd3, fd4, fd5, fd6],
        multivalued_dependencies=[mvd1]
    )

    print(f"Relvar: {relvar}")

    print("\nFunctional dependencies:")
    for fd in relvar.functional_dependencies:
        print(fd)

    print("\nMultivalued dependencies:")
    for mvd in relvar.multivalued_dependencies:
        print(mvd)


# Crear atributos
A = Attribute("A")
B = Attribute("B")
C = Attribute("C")

# Definir dependencias funcionales
fd1 = FunctionalDependency("{A}->{B}")
fd2 = FunctionalDependency("{B}->{C}")

# Definir dependencia multivaluada
mvd1 = MultivaluedDependency("{A}->->{B}")

# Mostrar cierre de A
print("Cierre de {A}:", {str(a) for a in closure({A}, {fd1, fd2})})

# Verificar si A es superllave
print("¿A es superllave?:", is_superkey({A}, {A, B, C}, {fd1, fd2}))

# Verificar si A es llave
print("¿A es llave mínima?:", is_key({A}, {A, B, C}, {fd1, fd2}))

# Crear relvar y verificar formas normales
relvar = Relvar(
    heading=["A", "B", "C"],
    functional_dependencies=[fd1, fd2],
    multivalued_dependencies=[mvd1]
)

print("¿Relvar está en BCNF?:", is_relvar_in_bcnf(relvar))
print("¿Relvar está en 4NF?:", is_relvar_in_4nf(relvar))

