class uCType(object):
    """
    Class that represents a type in the uC language.  Types
    are declared as singleton instances of this type.
    """

    def __init__(self, typename, unary_ops, binary_ops, rel_ops, assign_ops):
        """
        You must implement yourself and figure out what to store.
        """
        self.typename = typename
        self.unary_ops = unary_ops
        self.binary_ops = binary_ops
        self.rel_ops = rel_ops
        self.assign_ops = assign_ops


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
    "array",
    unary_ops={"*", "&"},
    binary_ops={},
    rel_ops={"==", "!="},
    assign_ops={"="},
)


class SymbolTable(object):
    """
    Class representing a symbol table.  It should provide functionality
    for adding and looking up nodes associated with identifiers.
    """

    def __init__(self):
        self.symtab = {}

    def lookup(self, a):
        return self.symtab.get(a)

    def add(self, a, v):
        self.symtab[a] = v


class NodeVisitor(object):
    """ A base NodeVisitor class for visiting uc_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.

        For example:

        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []

            def visit_Constant(self, node):
                self.values.append(node.value)

        Creates a list of values of all the constant nodes
        encountered below the given node. To use it:

        cv = ConstantVisitor()
        cv.visit(node)

        Notes:

        *   generic_visit() will be called for AST nodes for which
            no visit_XXX method was defined.
        *   The children of nodes for which a visit_XXX was
            defined will not be visited - if you need this, call
            generic_visit() on the node.
            You can use:
                NodeVisitor.generic_visit(self, node)
        *   Modeled after Python's own AST visiting facilities
            (the ast module of Python 3.0)
    """

    _method_cache = None

    def visit(self, node):
        """ Visit a node.
        """

        if self._method_cache is None:
            self._method_cache = {}

        visitor = self._method_cache.get(node.__class__.__name__, None)
        if visitor is None:
            method = "visit_" + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            self._method_cache[node.__class__.__name__] = visitor

        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for c in node:
            self.visit(c)


class Visitor(NodeVisitor):
    """
    Program visitor class. This class uses the visitor pattern. You need to define methods
    of the form visit_NodeName() for each kind of AST node that you want to process.
    Note: You will need to adjust the names of the AST nodes if you picked different names.
    """

    def __init__(self):
        # Initialize the symbol table
        self.symtab = SymbolTable()
        self.typechecker = [IntType, FloatType, CharType, ArrayType]
   
    def checkType(self, type1):
        for elem_type in typechecker:
            if elem_type.typename == type1:
                return type1

    def visit_ArrayDecl(self, node):
        # talvez tenha que checar tipos
        self.visit(node.decl)
        self.visit(node.type)
        type = checkType(node.type)
        assert type, "Unknown type"
        self.symtab.add(node.decl, type)

    def visit_ArrayRef(self, node):
        # se array ref existe:
        self.visit(node.array)
        self.visit(node.idx)
        sym = self.symtab.lookup(node.array)
        idx = node.idx.typename
        assert idx == IntType, "Invalid index type"
        assert sym, "Variable not declared"

    # Assert is generic

    def visit_Assignment(self, node):
        # 1. Make sure the location of the assignment is defined
        sym = self.symtab.lookup(node.lvalue)
        assert sym, "Assigning to unknown sym"
        # 2. Check that the types match
        self.visit(node.rvalue)
        assert sym.typename == node.rvalue.typename, "Type mismatch in assignment"

    def visit_BinaryOp(self, node):
        # 1. Make sure left and right operands have the same type
        self.visit(node.lvalue)
        self.visit(node.rvalue)

        left = self.symtab.lookup(node.lvalue)
        right = self.symtab.lookup(node.rvalue)

        assert left.typename == right.typename, "Type mismatch between operands"
        # 2. Make sure the operation is supported
        assert node.op in left.binary_ops, "Operation mismatch"
        # 3. Assign the result type
        node.type = left

    # Break is generic

    def visit_Cast(self, node):
        self.visit(node.expr)
        self.visit(node.type)
        type = self.symtab.lookup(node.type)
        assert type, "Unknown type"
        assert type == node.expr.typename, "Type mismatch in cast"
        self.symtab.add(node.expr, type)

    # TODO
    def visit_Compound(self, node):
        pass

    def visit_Constant(self, node):
        self.visit(node.value)
        self.visit(node.type)
        type = self.symtab.lookup(node.type)
        assert type, "Unknown type"
        value = self.symtab.lookup(node.value)
        if value:
            assert type == value.typename, "Type mismatch in decl"
        else:
            self.symtab.add(node.value, type)

    def visit_Decl(self, node):
        self.visit(node.init)
        self.visit(node.type)
        type = self.symtab.lookup(node.type)
        assert type, "Unknown type"
        init = self.symtab.lookup(node.init)
        assert type == init.typename, "Type mismatch in decl"
        self.symtab.add(node.init, type)

    def visit_DeclList(self, node):
        for _decl in node.decls:
            self.visit(_decl)

    # empty statement nao precisa ser checado

    def visit_ExprList(self, node):
        for _decl in node.expr:
            self.visit(_decl)

    # For gereric

    def visit_FuncCall(self, node):
        self.visit(node.name)
        self.visit(node.args)
        name = self.symtab.lookup(node.type)
        assert name, "Undeclared function"

    def visit_FuncDecl(self, node):
        self.visit(node.args)
        self.visit(node.type)

    def visit_FuncDef(self, node):
        self.vist(node.type)
        self.visit(node.declarator)
        for decls in node.declaration_list:
            self.visit(decls)   
        self.visit(node.compound_statement)
        sym = self.systab.lookup(node.declarator)
        assert (
            sym.typename == node.type.typename
        ), "Function already defined with a different type"
        self.symtab.add(node.declarator.value, node.type.typename)

    def visit_GlobalDecl(self, node):
        pass

    def visit_ID(self, node):
        pass

    def visit_If(self, node):
        pass

    def visit_InitList(self, node):
        pass

    def visit_ParamList(self, node):
        pass

    def visit_Print(self, node):
        pass

    def visit_PtrDecl(self, node):
        pass

    def visit_Program(self, node):
        # 1. Visit all of the global declarations
        # 2. Record the associated symbol table
        for _decl in node.gdecls:
            self.visit(_decl)

    def visit_Read(self, node):
        pass

    def visit_Return(self, node):
        pass

    def visit_Type(self, node):
        pass

    def visit_UnaryOp(self, node):
        pass

    def visit_VarDecl(self, node):
        pass

    def visit_While(self, node):
        pass
    
