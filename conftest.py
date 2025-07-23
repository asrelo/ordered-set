# pytest refuses to take this from a conftest.py file in the tests directory,
# because that directory "is not a root directory".
pytest_plugins = ('pytest_universal_indirection',)
