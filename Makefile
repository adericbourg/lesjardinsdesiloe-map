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
	mkdir -p output
	cp templates/base.template.html output/index.html

github: publish
	ghp-import -m "(script) Generate site from source" -b master output
	git push origin master
