import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .exceptions import InvalidDependency, InvalidExpression


@dataclass(frozen=True)
class Attribute:
    """
    Representa un atributo para una relvar en términos de la teoría de diseño del modelo relacional.
    Cada atributo tiene un nombre y es inmutable.

    Atributos:
        name (str): El nombre del atributo.
    """
    name: str

    def __str__(self) -> str:
        return self.name


class Dependency(ABC):
    """
    Clase abstracta base para dependencias funcionales y multivaluadas.
    
    Esta clase define la estructura común y el comportamiento para todos los tipos de dependencias
    dentro de la teoría del modelo relacional.
    """
    _CAPTURE_EXPRESSION: str
    _SEPARATOR: str

    def __init__(self, expression: str):
        # validating expression data type
        if not isinstance(expression, str):
            raise InvalidExpression(f"Expression must be a string, got {type(expression).__name__}.")

        # clean expression
        expression = expression.replace(" ", "")

        # validating syntax
        if not self._is_expression_valid(expression):
            raise InvalidExpression("Provided string does not represent a functional dependency.")

        # extracting determinant and dependant expressions
        determinant_expression, dependant_expression = expression.split(self._SEPARATOR)
        self.determinant = Dependency._get_set_from_expression(determinant_expression)
        self.dependant = Dependency._get_set_from_expression(dependant_expression)

    def __str__(self) -> str:
        determinant_expression = f"{{{', '.join(attribute.name for attribute in self.determinant)}}}"
        dependent_expression = f"{{{', '.join(attribute.name for attribute in self.dependant)}}}"
        return f"{determinant_expression} {self._SEPARATOR} {dependent_expression}"

    def __repr__(self) -> str:
        return self.__str__()

    def _is_expression_valid(self, expression: str) -> bool:
        """
        Valida si la expresión proporcionada sigue la sintaxis correcta para la dependencia.
        
        Args:
            expression (str): La expresión a validar.
            
        Returns:
            bool: True si la expresión es válida, False en caso contrario.
        """
        clean_expression = expression.replace(" ", '')
        return bool(re.fullmatch(self._CAPTURE_EXPRESSION, clean_expression))

    @staticmethod
    def _get_set_from_expression(expression: str) -> set:
        """
        Convierte una expresión en cadena de texto de atributos en un conjunto de objetos Attribute.
        
        Args:
            expression (str): La expresión a convertir, por ejemplo, "{A,B,C}".
            
        Returns:
            set: Un conjunto de objetos Attribute.
        """
        expression = expression.replace(" ", '')
        expression = expression.strip("{}")

        return set(Attribute(name) for name in expression.split(","))

    @abstractmethod
    def is_trivial(self, *args, **kwargs) -> bool:
        """
        Determina si la dependencia es trivial o no.
    
        Returns:
            bool: True si la dependencia es trivial, False en caso contrario.
        """
        raise NotImplementedError()


class FunctionalDependency(Dependency):
    """
    Clase para dependencias funcionales.
    
    Una dependencia funcional es una restricción entre dos conjuntos de atributos en una relación
    de una base de datos. Representa una relación donde el valor de un conjunto de atributos
    (determinante) determina de manera única el valor de otro conjunto (dependiente).
    """
    _CAPTURE_EXPRESSION = r"\{[A-z]+(?:,[A-z]+)*\}->\{[A-z]+(?:,[A-z]+)*\}"
    _SEPARATOR = "->"

    def is_trivial(self) -> bool:
        """
        Determina si la dependencia funcional es trivial.
        
        Una dependencia funcional {X} -> {Y} es trivial si Y es un subconjunto de X.
        En otras palabras, todos los atributos del lado derecho (dependiente) también 
        están en el lado izquierdo (determinante).
        
        Returns:
            bool: True si la dependencia es trivial, False en caso contrario.
        """
        return self.dependant.issubset(self.determinant)


class MultivaluedDependency(Dependency):
    """
    Clase para dependencias multivaluadas.
    
    Una dependencia multivaluada es una restricción entre dos conjuntos de atributos en una relación
    de una base de datos. Existe cuando hay al menos dos atributos independientes que
    se relacionan con un tercer atributo con una relación de muchos a muchos.
    """
    _CAPTURE_EXPRESSION = r"\{[A-z]+(?:,[A-z]+)*\}->->\{[A-z]+(?:,[A-z]+)*\}"
    _SEPARATOR = "->->"

    def is_trivial(self, heading: set[Attribute]) -> bool:
        """
        Determina si la dependencia multivaluada es trivial.
        
        Una dependencia multivaluada {X} ->-> {Y} es trivial si se cumple alguna de estas condiciones:
        1. Y es un subconjunto de X (Y ⊆ X), o
        2. La unión de X e Y es igual al encabezado completo (X ∪ Y = heading)
        
        Args:
            heading (set[Attribute]): El conjunto de atributos en el encabezado de la relvar.
        
        Returns:
            bool: True si la dependencia es trivial, False en caso contrario.
        """
        return (
            self.dependant.issubset(self.determinant) or 
            self.determinant.union(self.dependant) == heading
        )


class Relvar:
    """
    Clase para relvars (variables de relación).
    
    Una relvar es una variable cuyo valor es una relación. Contiene un encabezado 
    (conjunto de atributos) y puede tener dependencias funcionales y multivaluadas asociadas.
    """
    def __init__(self, heading: [str], functional_dependencies: [FunctionalDependency] = None, multivalued_dependencies: [MultivaluedDependency] = None):
        """
        Inicializa una nueva instancia de Relvar.
        
        Args:
            heading ([str]): Lista de nombres de atributos para la relvar.
            functional_dependencies ([FunctionalDependency], opcional): Lista de dependencias funcionales. Por defecto es None.
            multivalued_dependencies ([MultivaluedDependency], opcional): Lista de dependencias multivaluadas. Por defecto es None.
        """
        self.heading = set(Attribute(name) for name in heading)
        self.functional_dependencies = set()
        self.multivalued_dependencies = set()

        if functional_dependencies:
            for fd in functional_dependencies:
                self.add_functional_dependency(fd)

        if multivalued_dependencies:
            for mvd in multivalued_dependencies:
                self.add_multivalued_dependency(mvd)

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena de texto de la relvar.
        
        Returns:
            str: Una cadena que representa el encabezado de la relvar.
        """
        return f"{{{', '.join(attribute.name for attribute in self.heading)}}}"

    def __repr__(self) -> str:
        """
        Devuelve una representación detallada en cadena de texto de la relvar.
        
        Returns:
            str: Una cadena que representa el encabezado de la relvar y sus dependencias funcionales.
        """
        return f"heading={repr(self.heading)}, functional_dependencies={repr(self.functional_dependencies)}"

    def _validate_dependency(self, dependency: Dependency):
        """
        Valida que todos los atributos en una dependencia estén contenidos en el encabezado de la relvar.
        
        Args:
            dependency (Dependency): La dependencia a validar.
            
        Raises:
            InvalidDependency: Si la dependencia contiene un atributo que no está en el encabezado.
        """
        for attribute in dependency.determinant | dependency.dependant:
            if attribute not in self.heading:
                raise InvalidDependency(f"{attribute} is not contained in relvar's heading.")

    def add_functional_dependency(self, functional_dependency: FunctionalDependency):
        """
        Añade una dependencia funcional al conjunto de dependencias funcionales de la relvar.
    
        Args:
            functional_dependency (FunctionalDependency): La dependencia funcional a añadir.
    
        Raises:
            InvalidDependency: Si la dependencia funcional contiene un atributo que no está
                presente en el encabezado de la relvar.
        """
        self._validate_dependency(functional_dependency)
        self.functional_dependencies.add(functional_dependency)

    def add_multivalued_dependency(self, multivalued_dependency: MultivaluedDependency):
        """
        Añade una dependencia multivaluada al conjunto de dependencias multivaluadas de la relvar.

        Args:
            multivalued_dependency (MultivaluedDependency): La dependencia multivaluada a añadir.

        Raises:
            InvalidDependency: Si la dependencia multivaluada contiene un atributo que no está
                presente en el encabezado de la relvar.
        """
        self._validate_dependency(multivalued_dependency)
        self.multivalued_dependencies.add(multivalued_dependency)
