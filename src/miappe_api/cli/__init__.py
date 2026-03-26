"""CLI module for MIAPPE-API."""

import typer

app = typer.Typer(
    name="miappe",
    help="Schema-driven CLI for MIAPPE-compliant phenotyping metadata.",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """Show the version."""
    from miappe_api import __version__

    typer.echo(f"miappe-api {__version__}")


if __name__ == "__main__":
    app()
