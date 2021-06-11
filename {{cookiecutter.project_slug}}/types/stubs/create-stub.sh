#!/bin/bash -eu

package_name="${1:?package name}"

mkdir "${package_name}"
touch "${package_name}"/init.pyi
