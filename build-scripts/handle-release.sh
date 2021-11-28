set -eu

target="$(./build-scripts/get-parent.sh)"
release="$1"

function tag_with_release() {
  git tag -a "release-v$1" -m "[AUTOMATED] new release $1"
  git push origin "release-v$1"
}

if [[ "$target" == "release" ]]
then
  tag_with_release "$release"
fi