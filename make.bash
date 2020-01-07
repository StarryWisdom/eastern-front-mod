#!/bin/bash -e

rm -rf _build

check_tmp () {
	 xmllint ./dat/vesselData.xml > /dev/null
	../../artemis-check.py --no-warn
}

# assumes the file location is good
# it really should check that, but that will be a long bit of code :/
# sorry if you edit it and it decides to zip your home directory
# assumes PWD is inside where the zip will be made
# $1 = zip name
create_zip () {
	zipName="$1"
	cd ..
	zip -qr "$zipName".zip "$zipName"
}

# checks and creates the zip being created at $1
check_and_create () {
	dir="$1"

	old_dir="$PWD"
	cd "$dir"

	check_tmp
	create_zip "`basename "$1"`"

	cd "$old_dir"
}

build_loc="_build/EF MOD"
mkdir -p "$build_loc"
rsync -aWSH mod-files/ "$build_loc"
check_and_create "$build_loc"
