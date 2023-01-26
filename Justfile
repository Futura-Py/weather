isort:
    python3 -m isort *.py
    python3 -m isort tests/*.py

black:
    python3 -m black *.py
    python3 -m black tests/*.py