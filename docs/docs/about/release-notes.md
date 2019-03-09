# Release Notes

---

## Upgrading

To upgrade Pheasant to the latest version, use pip:

~~~
pip install -U pheasant
~~~

You can determine your currently installed version using `pheasant --version`:

~~~
$ pheasant --version
pheasant, version 1.0.0 from /path/to/pheasant (Python 3.7)
~~~

## Maintenance team

The current member of the MkDocs team.

* [@daizutabi](https://github.com/daizutabi/)

## Version 1.1 (2019-03-07)

* [Black](https://github.com/ambv/black) formatted.
* Drop dependency on [nbconvert](https://nbconvert.readthedocs.io/en/latest/) and [nbformat](https://nbformat.readthedocs.io/en/latest/). Code is executed as a plain source instead of a Jupyter Notebook's cell.
* Kernel client's `execute_interactive` method invoked instead of `execute` method. The method is new in Version 5.0 of [jupyter_client](https://jupyter-client.readthedocs.io/en/stable/index.html)

## Version 1.0 (2019-03-05)

* First major release.
