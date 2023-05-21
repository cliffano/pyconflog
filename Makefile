version=`yq -r .version conf/info.yaml`

ci: clean deps lint test coverage doc package install

clean:
	rm -rf stage *.egg-info build dist logconf/_pycache_/ logconf/*.pyc tests/_pycache_/ tests/*.pyc .coverage

stage:
	mkdir -p stage stage/ docs/

deps:
	pip3 install --ignore-installed -r requirements.txt
	pip3 install --ignore-installed -r requirements-dev.txt

lint: stage
	mkdir -p stage/lint/pylint/ docs/lint/pylint/
	pylint logconf/*.py logconf/loaders/*.py tests/*.py tests/loaders/*.py
	pylint logconf/*.py logconf/loaders/*.py tests/*.py tests/loaders/*.py --output-format=pylint_report.CustomJsonReporter > stage/lint/pylint/report.json
	pylint_report stage/lint/pylint/report.json -o docs/lint/pylint/index.html

complexity: stage
	wily build logconf/

install: package
	pip3 install dist/logconf-`yq -r .version conf/info.yaml | sed "s/-/_/g"`-py3-none-any.whl

reinstall:
	pip3 uninstall logconf -y || echo "Nothing to uninstall..."
	make clean deps package install

doc: stage
	rm -rf docs/doc/sphinx/ && mkdir -p docs/doc/sphinx/
	sphinx-apidoc -o stage/doc/sphinx/ --full -H "logconf" -A "Cliffano Subagio" logconf && \
		cd stage/doc/sphinx/ && \
		make html && \
		cp -R _build/html/* ../../../docs/doc/sphinx/

# Due to the difference in pre-release handling between Python setuptools and semver (which RTK supports),
# we have to massage the version number in conf/info.yaml before and after rtk release.
release:
	sed -i '' -e 's/rc0/-rc0/' conf/info.yaml
	rtk release
	sed -i '' -e 's/-rc0.0/rc0/' conf/info.yaml
	git commit conf/info.yaml -m "Switch version to Python setuptools versioning scheme"

publish:
	# TODO: publish to pypi

################################################################################
# Test targets
################################################################################

test:
	pytest -v tests --html=docs/test/pytest/index.html --self-contained-html

test-integration:
	tests-integration/test.sh

coverage:
	COVERAGE_FILE=.coverage.unit coverage run --source=./logconf -m unittest discover -s tests
	coverage combine
	coverage report
	coverage html

################################################################################
# Package targets
################################################################################

package:
	python3 setup.py sdist bdist_wheel

.PHONY: ci clean deps doc lint test coverage package install release package-lambdas package-lambda-layers jfrog-package jfrog-package-lambdas jfrog-package-lambda-layers
