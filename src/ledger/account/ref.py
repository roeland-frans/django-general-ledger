class RefError(Exception):
    """
    General reference error.
    """

    pass


class BaseRef(object):
    """
    The base class for reference numbers.
    """

    internal_ref_re = None

    def match_internal_ref(self, ref):
        raise NotImplementedError

    def generate(self, *args, **kwargs):
        raise NotImplementedError

    def description(self):
        raise NotImplementedError
