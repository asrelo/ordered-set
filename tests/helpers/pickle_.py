import pickle


def pickle_roundtrip(obj, protocol=None):
    return pickle.loads(pickle.dumps(obj, protocol=protocol))
