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

if [[ "$target" == "hotfix" ]]
then
  tag_with_release "$(incremented_bugfix "$current_version")"
fi