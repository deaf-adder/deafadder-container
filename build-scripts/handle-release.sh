set -eu

#==========================================================
# In case of release merged into master,
# this script will tag the merged commit with the
# version given in parameters.
#
# This script will only execute when the current
# commit is a merge commit and one of the parent
# is the master while hte other is a release branch.
#
# Script PARAMS:
#   $1: the current version of the release
#
# Return/print
#   Nothing
#
#==========================================================

target="$(./build-scripts/get-parent.sh)"
release="$1"

#-------------------------------
# Tag the current commit and push it
# to the origin remote
#
function tag_with_release() {
  git tag -a "release-v$1" -m "[AUTOMATED] new release $1"
  git push origin "release-v$1"
}

if [[ "$target" == "release" ]]
then
  tag_with_release "$release"
fi