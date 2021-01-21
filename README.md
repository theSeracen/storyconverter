# storyconverter

This is a simple tool for converting plaintext story files between markup formats and styles. The current supported types are:

  - Markdown
  - BBCode

The converter is also capable of validating the markup used in the files. This is done automatically when converting, or can be done on files without conversion.

## Options and Arguments

The following arguments are required:

  - `sources` can be specified mutliple times and are the source files to be converted. If multiple files are specified, they will be concatenated with a separator
  - `format` is the desired format and can be `markdown` or `bbcode`; for the validator, this is the markup format to check

The following are options that are not required:

  - `--source-format` can be used to specify the input format, otherwise it will be determined heuristically from the first input file
  - `-O, --output` can be used to specify the output destination; the default is to output in the current directory using the first source file's name with an appropriate extension
  - `--overwrite` will allow the output to be overwritten; if the destination file already exists and this option is not given, an exception will be raised
  - `-s, --stdout` will turn off logging and output convert
  - `-V, --validate` will take the source files and validate the markup in them.

## Example Command

### Conversion

To take two markdown files, concatenate them, and then output a BBCode file, the following command could be used.

`python3 -m storyconverter file1.md file2.md bbcode -O converted_file.txt`

### Validation

To take three BBCode files and validate the markup, use the following command:

`python3 -m storyconverter file1.txt file2.txt bbcode -V`