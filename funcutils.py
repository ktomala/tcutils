import types


def class_methods(cls):
    return [name for name, kind in cls.__dict__.items() \
            if type(kind) == types.FunctionType]


def class_prefixed_methods(cls, prefix):
    methods = class_methods(cls)
    return list(filter(lambda x: x.startswith(prefix), methods))
