# Claude.ai skill package, generated from the same files used by gh skill and the plugin.
.PHONY: skill-package test

skill-package:
	rm -f wcag-accessibility.skill
	cd skills && zip -rXD ../wcag-accessibility.skill wcag-accessibility -x '*.DS_Store'

test:
	python -m unittest discover -s tests -v
