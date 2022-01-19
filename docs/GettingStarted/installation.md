# Installation

This has started as a private project, published on [artifactory](https://leddzip.jfrog.io/ui/packages/pypi:%2F%2Fdeafadder-container).
But since version 0.5.0, this is also published on PYPI

## pip

### Private artifactory (Optional)
Modify your `~/.pip/pip.conf` to add:

```toml
[global]
index-url = https://<user>:<key>@leddzip.jfrog.io/artifactory/api/pypi/deaf-adder-pypi/simple
```

### pip install
Install with this command:

```bash
pip install deafadder-container
```

## poetry

### Private artifacotry (optional)
Update or add this section inside your `pyproject.toml`:

```toml
[[tool.poetry.source]]
name = "deafadder_pypi"
url = "https://<user>:<key>@leddzip.jfrog.io/artifactory/api/pypi/deaf-adder-pypi/simple"
```

### poetry add
Install with this command:

```bash
poetry add deafadder-container
```
