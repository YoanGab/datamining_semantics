import numpy as np

def convert_kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15


def get_extension_from_format(format: str) -> str:
    """ Get the extension from the format
    :param format: the format
    :return: the extension
    """
    if format == 'xml':
        return 'xml'
    elif format == 'n3':
        return 'n3'
    elif format == 'turtle':
        return 'ttl'
    elif format == 'nt':
        return 'nt'
    elif format == 'pretty-xml':
        return 'xml'
    elif format == 'trix':
        return 'trix'
    elif format == 'trig':
        return 'trig'
    elif format == 'nquads':
        return 'nq'
    else:
        return 'xml'

def get_euclidean_distance(x:list,y:list) -> float:
    x = np.array(x)
    y = np.array(y)
    return np.linalg.norm(x-y)
