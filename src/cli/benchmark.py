"""CLI for benchmark."""
import typer

app = typer.Typer()

@app.command()
def build(tasks: int = 500):
    typer.echo(f"Building {tasks} benchmark tasks...")

if __name__ == "__main__":
    app()
