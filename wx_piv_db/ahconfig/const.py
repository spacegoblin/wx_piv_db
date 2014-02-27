import sys

class Borg(object):
    """Cookbook 5.23.2 p. 273"""
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class ExampleBorg(Borg):
    def __init__(self, name=None):
        Borg.__init__(self)
        if name is not None:
            self.name = name
        
    def __str__(self):
        return "Example (%s)" % self.name


class _const(object):
    
    class ConstError(TypeError): pass
    
    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Cannot rebind constant %s" % name
        self.__dict__[name] = value
        
    def __delattr__(self, name):
        raise NameError, name

sys.modules[__name__] = _const()

def testBorg():
    a = ExampleBorg('Alex')
    b = ExampleBorg()
    print a, b
    c = ExampleBorg('Hermine')
    print a, b, c
    b.name = 'Maus'
    print a, b, c
    
if __name__=='__main__':
    print "aaaa"
    testBorg()