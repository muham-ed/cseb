"""CLI for generation."""
import typer

app = typer.Typer()

@app.command()
def generate(source: str = "java", count: int = 100):
    typer.echo(f"Generating {count} COBOL programs from {source}...")

if __name__ == "__main__":
    app()
