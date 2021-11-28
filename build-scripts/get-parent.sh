
set -eux

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

function get_branches_commit_belong_to() {
  git branch -a --contains "$1" | grep -v -e "$MASTER_STAR_PATTERN" -e "$HEAD_PATTERN"
}

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