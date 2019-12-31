from itertools import chain


class CollectionTool:
    @classmethod
    def uniq_iterable(cls, seq, idfun=None):
        seen = set()
        if idfun is None:
            for x in seq:
                if x in seen: continue
                seen.add(x)
                yield x
        else:
            for x in seq:
                y = idfun(x)
                if y in seen: continue
                seen.add(y)
                yield x

    iuniq = uniq_iterable

    @classmethod
    def luniq(cls, *_, **__):
        return list(cls.uniq_iterable(*_, **__))

    @classmethod
    def lmap(cls, *_, **__):
        return list(map(*_, **__))

    # @classmethod
    # def lchain(cls, *_):
    #     return list(chain(*_))

luniq = CollectionTool.luniq
lmap = CollectionTool.lmap
# lchain = CollectionTool.lchain