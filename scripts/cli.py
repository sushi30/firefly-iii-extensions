import click
from scripts.parse_credit_card import inner
from scripts.create_tables import create_tables


@click.group()
def cli():
    pass


def decorate(f):
    for dec in [
        click.argument("path", type=click.File(mode="rb")),
        click.option("--out", default=None),
        click.option("--storage", default=None),
        cli.command(),
    ]:
        f = dec(f)
    return f


@decorate
def isracard(out, storage, path):
    inner("isracard", path, out, storage)


@cli.command()
@click.argument("category")
@click.argument("descriptions", nargs=-1)
def rule(category, descriptions):
    create_budget(category)


@decorate
def leumicard(out, storage, path):
    inner("leumicard", path, out, storage)


@cli.command()
@click.argument("storage")
def tables(storage):
    create_tables(storage)


if __name__ == "__main__":
    cli()
