import doctest

OPTIONS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS |\
          doctest.NORMALIZE_WHITESPACE

doctest.testfile('test_checkplanetdiff.rst', verbose=True,
                 optionflags=OPTIONS)  