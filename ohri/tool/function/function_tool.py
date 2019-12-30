class FunctionToolkit:
    @classmethod
    def func2name(cls, f):
        return f.__name__

    # Moon - copied from private code
    @classmethod
    def func2cls(cls, meth):
        if inspect.ismethod(meth):
            for clazz in inspect.getmro(meth.__self__.__class__):
                if clazz.__dict__.get(meth.__name__) is meth:
                    return clazz
            meth = meth.__func__  # fallback to __qualname__ parsing

        if inspect.isfunction(meth):
            clazz = getattr(inspect.getmodule(meth),
                            meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
            if isinstance(clazz, type):
                return clazz
        return None

    @classmethod
    def func2class_func_name_list(cls, f):
        l = []

        clazz = cls.func2cls(f)
        if clazz: l.append(clazz.__name__)
        l.append(cls.func2name(f))

        return l
