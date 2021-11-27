set -eu

new_version="$1"

function update-pyproject-toml() {
  sed -i "0,/version = ".*"/{s/version = ".*"/version = \"$1\"/}" pyproject.toml
}

function update-init-py() {
  echo "__version__ = '$1'" > deafadder_container/__init__.py

}

function update-test() {
  sed -i "0,/assert __version__ == '.*'/{s/assert __version__ == '.*'/assert __version__ == '$1'/}" tests/test_deafadder_container.py
}


update-pyproject-toml "$new_version"
update-init-py "$new_version"
update-test "$new_version"
