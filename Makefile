# Install the origin-ci-tool on the local system.
# NOTE: this target may require `sudo` privileges.
install:
	pip install .
.PHONY: install

# Install the origin-ci-tool in the editable mode
# using the extra development dependencies.
install-development:
	pip install --editable .[development]
.PHONY: install-development

# Run the source code verification scripts.
verify:
	hack/verify/formatting.sh
	hack/verify/pep8.sh
	hack/verify/declared-versions-match.sh
.PHONY: verify

# Run the unit tests.
ifdef TARGET
    TARGET = --verbose $(TARGET)
else
    TARGET ?= discover --verbose
endif
test:
	coverage run -m unittest $(TARGET)
.PHONY: test

# Generate and view the coverage information.
coverage:
	coverage html
.PHONY: coverage
