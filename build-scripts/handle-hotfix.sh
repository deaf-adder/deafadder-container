set -eu

#==========================================================
# In case of a hotfix merged into master,
# this script will increment the bugfix version
# in all version reference in the project,
# then tag with the newly updated version and
# push it into github.
#
# Another pipeline is then triggered on our CI/CD tool
# that listen to this tag and perform a deployment
# of the new version in the correct repo.
#
# This script will execute only when the current commit
# is a merge commit and one of the parent is the master
# while the other is a hotfix branch.
#
# Script PARAMS:
#   $1: the current version of the release
#
# Returns/print:
#   Nothing
#
#==========================================================

target="$(./build-scripts/get-parent.sh)"
current_version="$1"

#-------------------------------
# Tag the current commit and push it to the
# origin remote.
#
# Params:
#   $1: the version to tag. Should be of the form xx.yy.zz
#
function tag_with_release() {
  git tag -a "release-v$1" -m "[AUTOMATED] new release $1"
  git push origin "release-v$1"
}

#-------------------------------
# Increment the bugfix number of the given
# release number. The release should be of the
# form xx/yy/zz
#
# Return/print:
#   The new updated release
#
function incremented_bugfix() {
  local release="$1"
  local bugfix
  bugfix="$(echo "$release" | cut -d . -f 3)"
  bugfix=$((bugfix+1))

  echo "$(echo "$release" | cut -d . -f 1-2).$bugfix"
}

#-------------------------------
# Update the version with the new version
# given in parameter in the different
# files that contains a reference  of the version
#
# Params:
#   $1: The new version
#
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