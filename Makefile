.PHONY: bootstrap generate validate enrich benchmark export

bootstrap:
pip install -r requirements.txt
python -m src.cli.generate --help

generate:
python -m src.cli.generate

validate:
python -m src.cli.validate

enrich:
python -m src.cli.enrich

benchmark:
python -m src.cli.benchmark

export:
python -m src.cli.export
