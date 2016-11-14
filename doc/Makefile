PROJECT_NAME = 'log-plotter API'
SRC_PATH = ../

all: api.update _build/html/index.html
_build/html/index.html: html
api.update: *.rst conf.py
	sphinx-apidoc -H $(PROJECT_NAME) -o ./api_doc $(SRC_PATH)
%.rst: $(SRC_PATH)/%.py
	if [ -e $@ ]; then rm $@; fi
	touch api.update
	echo $@ "updated"

include Makefile.sphinx
clean::
	rm api_doc/*.rst
	rm api.update
