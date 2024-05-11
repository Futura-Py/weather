ruff:
    ruff . --fix

isort:
    python3 -m isort *.py
    python3 -m isort tests/*.py

black:
    python3 -m black *.py
    python3 -m black tests/*.py

install:
    python3 -m pip install -r requirements.txt
    pip3 install autopep8 pyinstaller
    ruff --version

run:
    python3 main.py

run-tests:
    ruff .
    python3 -m unittest tests/test_*.py

autopep8:
    python3 -m autopep8 --in-place *.py
    python3 -m autopep8 --in-place tests/test_*.py


format:
    just black
    just autopep8
    just isort
    just ruff

build:
    pyinstaller weather.spec

build-win:
    pyinstaller weather-windows.spec
