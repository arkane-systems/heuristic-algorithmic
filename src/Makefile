#
# This Makefile produces all the binary images.
#

#
# default target: build both for installation
#
default: depends build

depends:
	mkdir -p deps
	python3 -m pip install -r ./requirements.txt --target deps --upgrade

build:
	python3 -m zipapp -o ../heuristic-algorithmic -p "/usr/bin/env python3" -c .
	cp hal.ini ../hal.ini

clean:
	rm -f ../heuristic-algorithmic
	rm -f ../hal.ini
