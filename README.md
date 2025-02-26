# proto-mangle
Mangles your protobuf files

## Usage

```
Usage: main.py [OPTIONS] INPUT_FILE

  Mangle your protobuf file and update names recursively. Outputs sed commands
  for replacing old names with new names and writes the modified protobuf to a
  separate file.

Options:
  --sed-out FILENAME    Output file for sed style replacement commands
  --proto-out FILENAME  Output file for the generated protobuf (defaults to
                        stdout)
  --separator TEXT      Separator for sed substitution commands  [default: _]
  --help                Show this message and exit.
  ```
