default:

clean:
	rm -rf .venv

freeze: testenv
	./.venv/bin/pip freeze >requirements.txt

testenv: clean
	python -m venv .venv
	./.venv/bin/pip install -r requirements.txt
