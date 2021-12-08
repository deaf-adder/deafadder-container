set -eu

#===============================
# This scripts is use in the context of merge commit.
# It will take the last commit of the current branch,
# validate if it is a merge commit, then try to infer
# the type of branch the commit comes from (being a
# release or a hotfix).

COMMIT_PATTERN="[a-f0-9]{7}"
MERGE_PATTERN="$COMMIT_PATTERN $COMMIT_PATTERN"

HOTFIX_PATTERN="^hotfix/.*$"
RELEASE_PATTERN="^release/.*"

HEAD_PATTERN="^  remotes/origin/HEAD -> origin/master$"
MASTER_STAR_PATTERN="^\* master$" # because on how 'git branch -a --contains xxx' works. It will put the current branch with a leading *

MASTER_PATTERN="^master$"

parent=""
commit1=""
commit2=""

#===============================
# Try to get all the branches that include this specific commit.
# In our context, if should be the master (with various prefix or suffix)
# and the release or hotfix branch.
#
# Params:
#   $1: the commit for which we want to get the branches that contains it
#
# Returns:
#   all the branches that contains this commit (one branch per line)
#
function get_branches_commit_belong_to() {
  git branch -a --contains "$1" | grep -v -e "$MASTER_STAR_PATTERN" -e "$HEAD_PATTERN"
}

#===============================
# echo the message into the stderr then exit the script
#
# Params:
#   $1: the message to display
function errcho() {
  >&2 echo "$1"
  exit 1
}

parent=$(git log -n 1 | grep -E "^Merge: $MERGE_PATTERN$" | grep -E -o "$MERGE_PATTERN") || exit 0
IFS=' ' read commit1 commit2 <<< "$parent"


branches_for_both_commit=$(printf "%s\n%s" "$(get_branches_commit_belong_to "$commit1")" "$(get_branches_commit_belong_to "$commit2")")
branches_for_both_commit=$(echo "$branches_for_both_commit" | cut -d/ -f 3- | grep -v -e "$MASTER_PATTERN")

cleaned_branch_for_both_commit=$(echo "$branches_for_both_commit" | sort | uniq) # should only contains one line

[[ $(echo "$cleaned_branch_for_both_commit" | wc -l) != 1 ]] && errcho "multiple branch detected. Only one remaining expected: $cleaned_branch_for_both_commit"

[[ "$cleaned_branch_for_both_commit" =~ ^release/[0-9]*\.[0-9]*\.[0-9]*$ ]] && echo "release" && exit 0
[[ "$cleaned_branch_for_both_commit" =~ ^hotfix/.*$ ]] && echo "hotfix" && exit 0

errcho "not recognized pattern for branch: $cleaned_branch_for_both_commit"