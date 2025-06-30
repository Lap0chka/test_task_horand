#!/usr/bin/env bash

if [ -z "${CI_MERGE_REQUEST_TARGET_BRANCH_NAME}" ]; then
  CI_MERGE_REQUEST_TARGET_BRANCH_NAME=main
fi

echo "Target branch: origin/${CI_MERGE_REQUEST_TARGET_BRANCH_NAME}"

# Исключаем venv_template/ из diff
git_diff_py_files=$(git diff origin/${CI_MERGE_REQUEST_TARGET_BRANCH_NAME} --name-only \
  | grep ".*\.py$" \
  | grep -Ev "^venv/" \
  | grep -Ev "core/" \
  | grep -Ev "manage.py")

run_linters() {
  echo "Running black..."
  python3 -m black --check "$@"

  echo "Running mypy..."
  python3 -m mypy "$@"

  echo "Running flake8..."
  python3 -m flake8 "$@"

  echo "Running pylint..."
  python3 -m pylint -j 4 --prefer-stubs y "$@"
}

if [ -n "$git_diff_py_files" ]; then
  py_files=''
  for file in $git_diff_py_files; do
    if [ -f "$file" ]; then
      py_files="$py_files $file"
    fi
  done

  echo "Validating changed Python files..."
  run_linters $py_files
else
  echo "No Python changes — validating all Python files..."
  all_py_files=$(find . -type f -name "*.py" \
    -not -path "./venv/*" \
    | grep -Ev "core/" \
    | grep -Ev "manage.py")

  run_linters $all_py_files
fi