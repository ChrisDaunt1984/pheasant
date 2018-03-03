```python inline
df = pd.DataFrame([[5, 0], [3, 4]], columns=['a', 'b'])

def func(x):
  plt.cla()
  plt.plot([0, x, 3*x])
  return {{^plt.gca()}}

{{df.applymap(func)}}
```

![python](hello.func)

~~~python
print(1)
print(2)

def func(x):
    return 2 * x
~~~

abcde

#Tab. a html table

First Header | Second Header
------------ | -------------
Content Cell | Content Cell
Content Cell | Content Cell

#Tab. a DataFrame table

<!-- begin -->
```python
## inline
df = pd.DataFrame([[1, 2]])
{{df}}
```
<!-- end -->
