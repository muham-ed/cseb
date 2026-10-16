"""CLI for export."""
import typer

app = typer.Typer()

@app.command()
def export(format: str = "parquet"):
    typer.echo(f"Exporting dataset as {format}...")

if __name__ == "__main__":
    app()
