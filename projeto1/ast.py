import sys


class Node(object):
    """
    Base class example for the AST nodes.

    By default, instances of classes have a dictionary for attribute storage.
    This wastes space for objects having very few instance variables.
    The space consumption can become acute when creating large numbers of instances.

    The default can be overridden by defining __slots__ in a class definition.
    The __slots__ declaration takes a sequence of instance variables and reserves
    just enough space in each instance to hold a value for each variable.
    Space is saved because __dict__ is not created for each instance.
    """

    """ Abstract base class for AST nodes.
    """

    def __repr__(self):
        """ Generates a python representation of the current node
        """
        result = self.__class__.__name__ + "("
        indent = ""
        separator = ""
        for name in self.__slots__[:-2]:
            result += separator
            result += indent
            result += (
                name
                + "="
                + (
                    _repr(getattr(self, name)).replace(
                        "\n",
                        "\n  " + (" " * (len(name) + len(self.__class__.__name__))),
                    )
                )
            )
            separator = ","
            indent = " " * len(self.__class__.__name__)
        result += indent + ")"
        return result

    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def show(
        self,
        buf=sys.stdout,
        offset=0,
        attrnames=False,
        nodenames=False,
        showcoord=False,
        _my_node_name=None,
    ):
        """ Pretty print the Node and all its attributes and children (recursively) to a buffer.
            buf:
                Open IO buffer into which the Node is printed.
            offset:
                Initial offset (amount of leading spaces)
            attrnames:
                True if you want to see the attribute names in name=value pairs. False to only see the values.
            nodenames:
                True if you want to see the actual node names within their parents.
            showcoord:
                Do you want the coordinates of each Node to be displayed.
        """
        lead = " " * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__ + " <" + _my_node_name + ">: ")
        else:
            buf.write(lead + self.__class__.__name__ + ": ")

        if self.attr_names:
            if attrnames:
                nvlist = [
                    (n, getattr(self, n))
                    for n in self.attr_names
                    if getattr(self, n) is not None
                ]
                attrstr = ", ".join("%s=%s" % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ", ".join("%s" % v for v in vlist)
            buf.write(attrstr)

        if showcoord:
            if self.coord:
                buf.write("%s" % self.coord)
        buf.write("\n")

        for (child_name, child) in self.children():
            child.show(buf, offset + 4, attrnames, nodenames, showcoord, child_name)

    __slots__ = ()
    attr_names = ()
    coord = ()


class ArrayDecl(Node):
    __slots__ = ("decl", "coord")

    def __init__(self, decl, coord=None):
        self.coord = coord
        self.decl = decl

    def children(self):
        nodelist = []
        if self.decl is not None:
            nodelist.append(self.decl)
        return tuple(nodelist)

    attr_names = ()


class ArrayRef(Node):
    __slots__ = ("array", "idx", "coord")

    def __init__(self, array, idx, coord=None):
        self.array = array
        self.idx = idx
        self.coord = coord

    def children(self):
        nodelist = []
        if self.array is not None:
            nodelist.append(("array", self.array))
        if self.idx is not None:
            nodelist.append(("idx", self.idx))
        return tuple(nodelist)

    attr_names = ()


class Assert(Node):
    __slots__ = ("lvalue", "rvalue", "coord")

    def __init__(self, lvalue, rvalue, coord=None):
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.coord = coord

    def children(self):
        nodelist = []
        if self.lvalue is not None:
            nodelist.append(("lvalue", self.lvalue))
        if self.rvalue is not None:
            nodelist.append(("rvalue", self.rvalue))
        return tuple(nodelist)

    attr_names = ()


class Assignment(Node):
    __slots__ = (
        "op",
        "lvalue",
        "rvalue",
        "coord",
    )

    def __init__(self, op, lvalue, rvalue, coord=None):
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.coord = coord

    def children(self):
        nodelist = []
        if self.lvalue is not None:
            nodelist.append(("lvalue", self.lvalue))
        if self.rvalue is not None:
            nodelist.append(("rvalue", self.rvalue))
        return tuple(nodelist)

    attr_names = ("op",)


class BinaryOp(Node):
    __slots__ = ("op", "lvalue", "rvalue", "coord")

    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.lvalue = left
        self.rvalue = right
        self.coord = coord

    def children(self):
        nodelist = []
        if self.lvalue is not None:
            nodelist.append(("lvalue", self.lvalue))
        if self.rvalue is not None:
            nodelist.append(("rvalue", self.rvalue))
        return tuple(nodelist)

    attr_names = ("op",)


class Break(Node):
    __slots__ = "coord"

    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return None

    attr_names = ()


class Cast(Node):
    __slots__ = ("type", "expr", "coord")

    def __init__(self, type, expr, coord=None):
        self.type = type
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(("type", self.type))
        if self.expr is not None:
            nodelist.append(("expr", self.expr))

        return tuple(nodelist)

    attr_names = ()


class Compound(Node):
    __slots__ = ("declaration_list", "statement_list", "coord")

    def __init__(self, declaration_list, statement_list, coord=None):
        self.declaration_list = declaration_list
        self.statement_list = statement_list
        self.coord = coord

    def children(self):
        nodelist = []
        for idx, dec in enumerate(self.declaration_list):
            nodelist.append(("declaration_list[%d]" % idx, dec))
        for idx, state in enumerate(self.statement_list):
            nodelist.append(("statement_list[%d]" % idx, state))
        return tuple(nodelist)

    attr_names = ()


class Constant(Node):
    __slots__ = ("type", "value", "coord")

    def __init__(self, type, value, coord=None):
        self.type = type
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = (
        "type",
        "value",
    )


class Decl(Node):
    __slots__ = ("type", "name", "init", "coord")

    def __init__(self, type, name, init, coord=None):
        self.type = type
        self.name = name
        self.init = init
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(("type", self.type))
        if self.name is not None:
            nodelist.append(("name", self.name))
        if self.init is not None:
            nodelist.append(("init", self.init))
        return tuple(nodelist)

    atrr_names = ("name",)


class DeclList(Node):
    __slots__ = ("type", "name_list", "init", "coord")

    def __init__(self, type, name_list, init, coord=None):
        self.type = type
        self.name_list = name_list
        self.init = init
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(("type", self.type))
        for idx, name in enumerate(self.name_list):
            nodelist.append(("names[%d]" % idx, name))
        if self.init is not None:
            nodelist.append(("init", self.init))
        return tuple(nodelist)

    atrr_names = ()


class EmptyStatement(Node):
    __slots__ = "coord"

    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    attr_names = ()


class ExprList(Node):
    __slots__ = ("expr", "coord")

    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.expr or []):
            nodelist.append(("exprs[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()


class For(Node):
    __slots__ = ("init", "cond", "step", "stmt", "coord")

    def __init__(self, init, cond, step, stmt, coord=None):
        self.init = init
        self.cond = cond
        self.step = step
        self.stmt = stmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.init is not None:
            nodelist.append(("init", self.init))
        if self.cond is not None:
            nodelist.append(("cond", self.cond))
        if self.step is not None:
            nodelist.append(("step", self.step))
        if self.stmt is not None:
            nodelist.append(("stmt", self.stmt))
        return tuple(nodelist)

    attr_names = ()


class FuncCall(Node):
    __slots__ = ("name", "args", "coord")

    def __init__(self, name, args, coord=None):
        self.name = name
        self.args = args
        self.coord = coord

    def children(self):
        nodelist = []
        if self.name is not None:
            nodelist.append(("name", self.name))
        if self.args is not None:
            nodelist.append(("args", self.args))
        return tuple(nodelist)

    attr_names = ()


class FuncDecl(Node):
    __slots__ = ("args", "type", "coord")

    def __init__(self, args, type, coord=None):
        self.args = args
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.args is not None:
            nodelist.append(("args", self.args))
        if self.type is not None:
            nodelist.append(("type", self.type))
        return tuple(nodelist)

    attr_names = ()


class FuncDef(Node):
    __slots__ = (
        "type",
        "declarator",
        "declaration_list",
        "compound_statement",
        "coord",
    )

    def __init__(
        self, type, declarator, declaration_list, compound_statement, coord=None
    ):
        self.type = type
        self.declarator = declarator
        self.declaration_list = declaration_list
        self.compound_statement = compound_statement
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(("type", self.type))
        if self.declarator is not None:
            nodelist.append(("declarator", self.declarator))
        for i, dec in enumerate(self.declaration_list or []):
            nodelist.append(("declaration_list[%d]" % i, dec))
        if self.compound_statement is not None:
            nodelist.append(("compound_statement", self.compound_statement))
        return tuple(nodelist)

    attr_names = ()


class GlobalDecl(Node):
    __slots__ = ("glbldec", "coord")

    def __init__(self, glbldec, coord=None):
        self.glbldec = glbldec
        self.coord = coord

    def children(self):
        nodelist = []
        if self.glbldec is not None:
            nodelist.append(("glbldec", self.glbldec))
        return tuple(nodelist)

    attr_names = ()


class ID(Node):
    __slots__ = ("name", "coord")

    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ("name",)


class If(Node):
    __slots__ = ("cond", "if_true", "if_false", "coord", "__weakref__")

    def __init__(self, cond, if_true, if_false, coord=None):
        self.cond = cond
        self.if_true = if_true
        self.if_false = if_false
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None:
            nodelist.append(("cond", self.cond))
        if self.if_true is not None:
            nodelist.append(("if_true", self.if_true))
        if self.if_false is not None:
            nodelist.append(("if_false", self.if_false))
        return tuple(nodelist)

    attr_names = ()


class InitList(Node):
    __slots__ = ("initializer", "coord")

    def __init__(self, initializer, coord=None):
        self.initializer = initializer
        self.coord = coord

    def children(self):
        nodelist = []
        for i, dec in enumerate(self.initializer or []):
            nodelist.append(("initializer[%d]" % i, dec))
        return tuple(nodelist)

    attr_names = ()


class ParamList(Node):
    __slots__ = ("parameter_declaration", "coord")

    def __init__(self, parameter_declaration, coord=None):
        self.parameter_declaration = parameter_declaration
        self.coord = coord

    def children(self):
        nodelist = []
        for i, dec in enumerate(self.parameter_declaration or []):
            nodelist.append(("parameter_declaration[%d]" % i, dec))
        return tuple(nodelist)

    attr_names = ()


class Print(Node):
    __slots__ = ("expression", "coord")

    def __init__(self, expression, coord=None):
        self.expression = expression
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expression is not None:
            nodelist.append(("expression", self.expression))
        return tuple(nodelist)

    attr_names = ()


class PtrDecl(Node):
    __slots__ = ("pointer", "coord")

    def __init__(self, pointer, coord=None):
        self.pointer = pointer
        self.coord = coord

    def children(self):
        nodelist = []
        if self.pointer is not None:
            nodelist.append(("pointer", self.pointer))
        return tuple(nodelist)

    attr_names = ()


class Program(Node):
    __slots__ = ("gdecls", "coord")

    def __init__(self, gdecls, coord=None):
        self.gdecls = gdecls
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.gdecls or []):
            nodelist.append(("gdecls[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()


class Read(Node):
    __slots__ = ("argument_expression", "coord")

    def __init__(self, argument_expression, coord=None):
        self.argument_expression = argument_expression
        self.coord = coord

    def children(self):
        nodelist = []
        if self.argument_expression is not None:
            nodelist.append(self.argument_expression)
        return tuple(nodelist)

    attr_names = ()


class Return(Node):
    __slots__ = ("expression", "coord")

    def __init__(self, expression, coord=None):
        self.coord = coord
        self.expression = expression

    def children(self):
        nodelist = []
        if self.expression is not None:
            nodelist.append(("expression", self.expression))
        return tuple(nodelist)

    attr_names = ()


class Type(Node):
    __slots__ = ("type", "coord")

    def __init__(self, type, coord=None):
        self.coord = coord
        self.type = type

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ("type",)


class UnaryOp(Node):
    __slots__ = ("operator", "expr", "coord")

    def __init__(self, operator, expr, coord=None):
        self.operator = operator
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.operator is not None:
            nodelist.append(("operator", self.operator))
        if self.expr is not None:
            nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    attr_names = ("operator",)


class VarDecl(Node):
    __slots__ = ("var", "coord")

    def __init__(self, var, coord=None):
        self.var = var
        self.coord = coord

    def children(self):
        nodelist = []
        if self.var is not None:
            nodelist.append(self.var)
        return tuple(nodelist)

    attr_names = ()


class While(Node):
    __slots__ = ("expression", "statement", "coord")

    def __init__(self, expression, statement, coord=None):
        self.coord = coord
        self.expression = expression
        self.statement = statement

    def children(self):
        nodelist = []
        if self.expression is not None:
            nodelist.append(("expression", self.expression))
        if self.statement is not None:
            nodelist.append(("statement", self.statement))
        return tuple(nodelist)

    attr_names = ()


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


class Coord(object):
    """ Coordinates of a syntactic element. Consists of:
            - Line number
            - (optional) column number, for the Lexer
    """

    __slots__ = ("line", "column")

    def __init__(self, line, column=None):
        self.line = line
        self.column = column

    def __str__(self):
        if self.line:
            coord_str = "   @ %s:%s" % (self.line, self.column)
        else:
            coord_str = ""
        return coord_str

    def _token_coord(self, p, token_idx):
        last_cr = p.lexer.lexer.lexdata.rfind("\n", 0, p.lexpos(token_idx))
        if last_cr < 0:
            last_cr = -1
        column = p.lexpos(token_idx) - (last_cr)
        return Coord(p.lineno(token_idx), column)


def _repr(obj):
    """
    Get the representation of an object, with dedicated pprint-like format for lists.
    """
    if isinstance(obj, list):
        return "[" + (",\n ".join((_repr(e).replace("\n", "\n ") for e in obj))) + "\n]"
    else:
        return repr(obj)


"""
types = [
   x ArrayDecl(),
   x ArrayRef(),
   x Assert(),
   x Assignment(op),
   x BinaryOp(op),
   x Break(),
   x Cast(),
   x Compound(),
   x Constant(type, value),
   x Decl(name),
   x DeclList(),
   x EmptyStatement(),
   x ExprList(),
   x For(),
   x FuncCall(),
   x FuncDecl(),
   x FuncDef(),
   x GlobalDecl(),
   x ID(name),
   x If(),
   x InitList(),
   x ParamList(),
   x Print(),
   x Program(),
   x PtrDecl(),
   x Read(),
   x Return(),
   x Type(names),
   x VarDecl(),
   x UnaryOp(op),
   x While(),
]
"""