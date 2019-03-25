# Script renderer test
# # Title
# ## Section
# ### Subsection

# paragraph 1
# paragraph 1

# #Fig
# ~~~
# d
# ~~~

# -
import pytest

from pheasant.script.renderer import Script


@pytest.fixture()
def source():
    with open(__file__, "r", encoding="utf-8-sig") as file:
        return file.read()


# -display
@pytest.fixture()
def script(source):
    """
    Return a Script instance.
    """
    script = Script()
    return script


# paragraph 2
# paragraph 2


def f():
    for x in range(10):

        yield x


# paragraph 3
# paragraph 3

# paragraph 4
# paragraph 4

# -inline
def g():
    pass


# fenced code test

# before:
# ~~~python
# # ```python
# # print(1)
# # ```
# ~~~
# after:
# ```python
# print(1)
# ```
# before:
# ~~~python
# # ~~~
# # ```python
# # print(1)
# # ```
# # ~~~
# ~~~
# after:
# ~~~
# ```python
# print(1)
# ```
# ~~~
