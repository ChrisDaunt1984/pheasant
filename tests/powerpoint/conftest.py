import os
import platform

import pytest

try:
    from pheasant.powerpoint import PowerPoint
except ImportError:
    pass


is_not_windows = platform.system() != 'Windows'


@pytest.fixture(scope='module')
def root():
    root = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(root, '../resources/office'))
    yield root


@pytest.fixture(scope='module')
def pp():
    yield PowerPoint()


@pytest.fixture(scope='module')
def prs(pp, root):
    path = os.path.join(root, 'presentation.pptx')
    prs = pp.presentations.open(path, with_window=False)
    yield prs
    prs.close()
