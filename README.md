# perdict

Persistent dictionary. Key-value pairs are stored on disk in a file. 

If no filename is specified stored ~/.perdict/globals.cpkl

### Install

```bash
$> pip install perdict
$> python
```

### Usage

```python
>>> from perdict import Perdict
>>> d = Perdict()
>>> d["my key"] = 3
>>> quit()
```

```bash
$> python
```

```python
>>> from perdict import Perdict
>>> d = Perdict()
>>> d["my key"]
3
```
