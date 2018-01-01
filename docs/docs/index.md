# Pheasant

## Overview

Pheasant is a Markdown converter which can be used as a plugin for static site generators such as [MkDocs](http://www.mkdocs.org/) or [Pelican](http://docs.getpelican.com/en/stable/).

Highlights include:

+ Auto generation of outputs for a fenced code block in Markdown source using [Jupyter client](https://jupyter-client.readthedocs.io/en/stable/). The code language is not restricted to Python.
+ Auto numbering of headers, figures, and tables. Numbered objects can be linked from Markdown source.
+ Simple interface to use Pheasant as a plugin for other site generators.
+ Easy to introduce any extensions you want to Pheasant.


## How to install

You can install Pheasant from PyPI.

~~~
$ pip install pheasant
~~~

If you use Pheasant as a plugin for MkDocs or Pelican, you also need to instal them.

~~~
$ pip install mkdocs pelican
~~~

## Plugin settings

### MkDocs

In your `mkdocs.yml`, add lines below:

~~~
plugins:
  - pheasant:
      jupyter:
        enabled: True
      number:
        enabled: True
~~~

### Pelican

In your `pelicanconf.py`, add lines below:

~~~
PLUGINS = ['pheasant']
PHEASANT = {'jupyter': {'enabled': True}}
~~~

!!! Note
    In general, auto numbering feature is not suitable for articles (such as blog) written in Pelican.

## Examples

### Auto generation of outputs with Jupyter client

A markdown soure below:

~~~
```python
print(1)
```
~~~

is converted into:

~~~
```python
>>> print(1)
1
```
~~~

after execution of `print` function via Jupyter client and finally the output becomes

```python
print(1)
```

Pheasant supports various output formats other than standard stream. For example, you can create a PNG image from Matplotlib.

~~~
```python
%matplotlib inline
import matplotlib.pyplot as plt
plt.plot([1, 3, 2]);
```
~~~

The above Markdown source creates an input Python code block and a PNG image:

```python
%matplotlib inline
import matplotlib.pyplot as plt
plt.plot([1, 3, 2]);
```

You may want not to display a code block itself. You can use `hide-input` option after a ```` ```python ```` statement.

~~~
```python hide-input
plt.plot([1, 3, 2]);
```
~~~

This creates only a PNG image without a code block like below:

```python hide-input
plt.plot([1, 3, 2]);
```

!!! Note
    Matplotlib package already has been imported in the previous code block so that we don't need install it again here.

Pheasant also supports Bokeh's HTML output.

~~~
```python hide-input
from bokeh.plotting import figure
from bokeh.io import output_notebook
from bokeh.io import show
output_notebook()
p = figure(plot_width=250, plot_height=250)
p.circle([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], size=10)
show(p)
```
~~~

```python hide-input
from bokeh.plotting import figure
from bokeh.io import output_notebook
from bokeh.io import show
output_notebook()
p = figure(plot_width=250, plot_height=250)
p.circle([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], size=10)
show(p)
```

The language executed in Pheasant is not restricted to Python. For example,
if you install Julia kernel, you can write:

~~~
```julia
x = 2
println(3x)
```
~~~

to get output like below:


```julia
x = 2
println(3x)
```

### Auto numbering of headers, figures, and tables.

As you can see, all of headers are numbered in this document. This is done by Pheasant automatically. In addition, Pheasant can count the number of figures and tables and give the identical number to each figure or table.

You can use a special *header* statement for figure (`#Figure`) and table (`#Table`) to number them like below:

~~~
#Figure This is a cat. {#cat#}

![jpg](img/cat.jpg)
~~~

#Fig This is a cat. {#cat#}

![jpg](img/cat.jpg)

!!! Note
    In the above Markdown source, `{#<tag>#}` is a tag for hyperlink described below.

Off course, you can use any code to create a figure:

~~~
#Fig A Matplotlib figure

```python hide-input
plt.plot([3, 1]);
```
~~~

#Fig A Matplotlib figure

```python hide-input
plt.plot([3, 1]);
```

Like figures, tables can be numbered.

~~~
#Table A Markdown table

a | b
--|--
0 | 1
2 | 3
~~~

#Table A Markdown table

a | b
--|--
0 | 1
2 | 3

Pandas DataFarme is useful to create a table programmatically.

~~~
#Table A Pandas DataFrame

```python hide-input
import pandas as pd
pd.DataFrame([[1, 2], [3, 4]], columns=list('ab')) * 2
```
~~~


#Table A Pandas DataFrame

```python hide-input
import pandas as pd
pd.DataFrame([[1, 2], [3, 4]], columns=list('ab')) * 2
```


Numbered objects are linked from Markdown source using `{#<tag>#}`:

~~~
Go to Fig. {#cat#}
~~~


Go to Fig. {#cat#}
