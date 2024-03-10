from sprnldata.core import EcosSet

import pandas
from pandaspro.core.frame import FramePro

__all__ = [
    'EcosSet',
    'FramePro'
]

if __name__ == '__main__':
    a = pandas.DataFrame({
        'id': [1, 2, 3, 5, 6],
        'value': ['a', 'b', 1, 'd', 'e']
    })
    a = a.set_index('value')
    type(a.index)