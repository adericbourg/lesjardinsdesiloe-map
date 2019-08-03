OUTPUT_DIR=output

all: check publish

help:
	@echo 'Usage:                                                                    '
	@echo '   make help                           display this message               '
	@echo '   make check                          check data consistency             '
	@echo '   make publish                        generate output locally            '
	@echo '   make github                         publicly publish outp              '

check:
	@echo "No check yet :("

publish:
	@python script/generate.py $(OUTPUT_DIR)

github: publish
	ghp-import -m "(script) Generate site from source" -b master $(OUTPUT_DIR)
	git push origin master
