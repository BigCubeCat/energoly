def interactive():

    import os
    import code
    import readline
    import rlcompleter
    import atexit

    vars = globals()
    vars.update(locals())
    readline.set_completer(rlcompleter.Completer(vars).complete)
    readline.parse_and_bind("tab: complete")

    del os, readline, rlcompleter, atexit
    code.interact(banner="", local=vars)


if __name__ == "__main__":
    # noinspection PyUnresolvedReferences
    from .__init__ import *
    interactive()
