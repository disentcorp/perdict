# perdict

![Coverage Status](./coverage-badge.svg?dummy=8484744)

Super simple Persistent dictionary. Key-value pairs are stored on disk in a file. Also supports "dot-notation".

If no filename is specified stored ~/.perdict/globals.cpkl. Serialization is courtesy of `cloudpickle`.

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

### Dot notation

```python
>>> from perdict import Perdict
>>> d = Perdict()
>>> d.new_key = 3  # all user keys with spaces are interpreted as underscore (`_`).
>>> d["new key"]
3
```

### Why use this?

- Variable storage
- Settings module
- Data storage module
