set -eu

target="$(./build-scripts/get-parent.sh)"
current_version="$1"


function tag_with_release() {
  git tag -a "release-v$1" -m "[AUTOMATED] new release $1"
  git push origin "release-v$1"
}

function incremented_bugfix() {
  local release="$1"
  local bugfix
  bugfix="$(echo "$release" | cut -d . -f 3)"
  bugfix=$((bugfix+1))

  echo "$(echo "$release" | cut -d . -f 1-2).$bugfix"
}

function update-version-everywhere() {
  local new_version="$1"
  ./build-scripts/update-version.sh "$new_version"
  git add deafadder_container/__init__.py
  git add tests/test_deafadder_container.py
  git add pyproject.toml
  git commit -m "update bugfix version to $new_version"
  git push
}

if [[ "$target" == "hotfix" ]]
then
  updated_version="$(incremented_bugfix "$current_version")"
  update-version-everywhere "$updated_version"
  tag_with_release "$updated_version"
fi