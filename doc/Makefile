PROJECT_NAME = 'log-plotter'
SRC_PATH = ../

all: api.update _build/html/index.html
_build/html/index.html: html
api.update: *.rst conf.py
	sphinx-apidoc -F -o ./ $(SRC_PATH) -H $(PROJECT_NAME)
%.rst: $(SRC_PATH)/%.py
	if [ -e $@ ]; then rm $@; fi
	touch api.update
	echo $@ "updated"

include Makefile.sphinx
clean::
	rm *.rst
	rm api.update
