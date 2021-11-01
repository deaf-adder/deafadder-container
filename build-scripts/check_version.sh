set -e

#===============================
# This scripts is use to assert the version
# has a valid format and consistent across
# all main files

init_version=$(grep "__version__" deafadder_container/__init__.py | cut -d = -f 2 | cut -d\' -f 2)
poetry_version=$(grep -o "^version = \"[0-9\.a-zA-Z_-]*\"$" pyproject.toml | cut -d = -f 2 | cut -d \" -f 2)
if [[ "$init_version" == "$poetry_version" ]]
then
  echo "version match between init file and pyproject.toml file"
else
  >&2 echo "version does not match between init file and pyproject.toml file"
  exit 1
fi



if [[ "$ini_version" =~ [0-9]+\.[0-9]+\.[0-9]+ ]]
then
  echo "version has a valid format"
else
  >&2 echo "version has wrong format"
  exit 2
fi