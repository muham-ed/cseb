"""CLI for validation."""
import typer

app = typer.Typer()

@app.command()
def validate(input_dir: str = "data/generated/cobol"):
    typer.echo(f"Validating COBOL in {input_dir}...")

if __name__ == "__main__":
    app()
