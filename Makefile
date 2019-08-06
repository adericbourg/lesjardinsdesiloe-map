OUTPUT_DIR=output

all: check publish

help:
	@echo 'Usage:                                                                          '
	@echo '   make help                           display this message                     '
	@echo '   make check                          check data consistency                   '
	@echo '   make publish                        generate output                          '
	@echo '   make dev                            generate output for local test           '
	@echo '                                       (combine with devserver)                 '
	@echo '   make watch                          rebuild the full site for every change   '
	@echo '   make devserver                      run local webserver                      '
	@echo '   make github                         publicly publish output                  '

check:
	@python -m unittest discover -s tests

dev:
	@DEVSETTINGS=true python script/generate.py $(OUTPUT_DIR)

watch:
	@fswatch  --one-per-batch content script static templates | xargs -n1 -I{} make dev

devserver: dev
	@python -m http.server --directory $(OUTPUT_DIR) 9000

publish:
	@python script/generate.py $(OUTPUT_DIR)

github: publish
	ghp-import -m "(script) Generate site from source" -b master $(OUTPUT_DIR)
	git push origin master
