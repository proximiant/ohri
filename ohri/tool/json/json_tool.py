from functools import reduce


class JsonTool:
    @classmethod
    def down(cls, j_in, jpath):
        if not j_in:
            return None

        return reduce(lambda j,step:j.get(step) if j else None, jpath, j_in)

jdown = JsonTool.down