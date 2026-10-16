"""CLI for enrichment."""
import typer

app = typer.Typer()

@app.command()
def enrich(input_dir: str = "data/validated/passed"):
    typer.echo(f"Enriching {input_dir}...")

if __name__ == "__main__":
    app()
