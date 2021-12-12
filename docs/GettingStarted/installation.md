# Installation

For now, it's only a private project, published on [artifactory](https://leddzip.jfrog.io/ui/packages/pypi:%2F%2Fdeafadder-container).

## pip

Modify your `~/.pip/pip.conf` to add:

```toml
[global]
index-url = https://<user>:<key>@leddzip.jfrog.io/artifactory/api/pypi/deaf-adder-pypi/simple
```

When it is done. Install with this command:

```bash
pip install deafadder-container
```

## poetry

Update or add this section inside your `pyproject.toml`:

```toml
[[tool.poetry.source]]
name = "deafadder_pypi"
url = "https://<user>:<key>@leddzip.jfrog.io/artifactory/api/pypi/deaf-adder-pypi/simple"
```

When it is done. Install with this command:

```bash
poetry add deafadder-container
```