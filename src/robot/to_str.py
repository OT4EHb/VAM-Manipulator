def to_str(obj, index=1):
    delim = ' ' * index

    cls = obj.__class__
    if '__str__' in cls.__dict__:
        return str(obj)
    if '__repr__' in cls.__dict__:
        return repr(obj)

    attrs = {k: to_str(v, index + 1) for k, v in obj.__dict__.items() if not k.startswith('_')}
    attrs_str = ",\n".join([f"{delim}{k}: {v}" for k, v in attrs.items()])
    return f"{obj.__class__.__name__}(\n{attrs_str}\n{delim[1:]})"


if __name__ == "__main__":
    class A:
        def __init__(self):
            self.a = 1
            self.b = 2
            self.c = [1, 2, 3]


    class B:
        def __init__(self):
            self.name = "class B"
            self.value = A()


    b = B()
    print(to_str(b))
