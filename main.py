import sys
import random
import string
import click
from names import get_random_name
from proto_schema_parser.parser import Parser
from proto_schema_parser.generator import Generator

def random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))

def create_name(separator: str) -> str:
    name = get_random_name(sep=separator)
    random_str = random_string(5)
    return f"{name}{random_str}".format(name=name,random_str=random_str)

@click.command()
@click.argument("input_file", type=click.File("rb"), nargs=1)
@click.option("--sed-out", type=click.File("w"), required=False,
              help="Output file for sed style replacement commands")
@click.option("--proto-out", type=click.File("w"), default='-',
              help="Output file for the generated protobuf (defaults to stdout)")
@click.option("--separator", default="_", show_default=True,
              help="Separator for sed substitution commands")
def cli(input_file, sed_out, proto_out, separator):
    """
    Mangle your protobuf file and update names recursively.
    Outputs sed commands for replacing old names with new names
    and writes the modified protobuf to a separate file.
    """

    modified = []

    try:
        ast = Parser().parse(input_file.read().decode("ascii"))
    except Exception as e:
        print("error parsing input file: ", e)
        sys.exit(1)

    def update_names_recursively(element: any):
        if hasattr(element, "name") and element.name is not None:
            old_name = element.name
            new_name = create_name(separator)
            element.name = new_name
            modified.append((old_name, new_name))
        if hasattr(element, "type") and element.type is not None:
            for m in modified:
                if m[0] == element.type:
                    element.type = m[1]
        if hasattr(element, "elements") and isinstance(element.elements, list):
            for child in element.elements:
                update_names_recursively(child)

    if len(ast.file_elements) < 1:
        print("There are not enough items in your protobuf file to modify")
        sys.exit(1)

    for file_element in ast.file_elements[1:]:
        update_names_recursively(file_element)

    if sed_out is not None:
        for old, new in modified:
            sed_command = f"s/{old}/{new}/g"
            sed_out.write(sed_command + "\n")
        sed_out.flush()

    proto = Generator().generate(ast)
    proto_out.write(proto)
    proto_out.flush()

if __name__ == "__main__":
    cli()

