class uCType(object):
    """
    Class that represents a type in the uC language.  Types 
    are declared as singleton instances of this type.
    """

    def __init__(self, name, typename, unary_ops, binary_ops, rel_ops, assign_ops):
        """
        You must implement yourself and figure out what to store.
        """
        self.typename = typename
        self.unary_ops = unary_ops or set()
        self.binary_ops = binary_ops or set()
        self.rel_ops = rel_ops or set()
        self.assign_ops = assign_ops or set()


# Create specific instances of types. You will need to add
# appropriate arguments depending on your definition of uCType
IntType = uCType(
    "int",
    unary_ops={"-", "+", "--", "++", "p--", "p++", "*", "&"},
    binary_ops={"+", "-", "*", "/", "%"},
    rel_ops={"==", "!=", "<", ">", "<=", ">="},
    assign_ops={"=", "+=", "-=", "*=", "/=", "%="},
)

FloatType = uCType(
    "float",
    unary_ops={"-", "+", "--", "++", "p--", "p++", "*", "&"},
    binary_ops={"+", "-", "*", "/", "%"},
    rel_ops={"==", "!=", "<", ">", "<=", ">="},
    assign_ops={"=", "+=", "-=", "*=", "/=", "%="},
)
CharType = uCType(
    "char",
    unary_ops={"-", "+", "--", "++", "p--", "p++", "*", "&"},
    binary_ops={"+", "-"},
    rel_ops={"==", "!="},
    assign_ops={"=", "+=", "-="},
)
ArrayType = uCType(
    "array", unary_ops={"*", "&"}, rel_ops={"==", "!="}, assign_ops={"="},
)
