#
# This Makefile produces all the binary images.
#

#
# default target: build both for installation
#
default: depends

depends:
	mkdir -p deps
	python3 -m pip install -r ./requirements.txt --target deps --upgrade

clean:
	rm -rf ../deps/*
	rm -rf __pycache__
