# storyconverter

This is a simple tool for converting plaintext story files between markdown formats and styles. The current supported types are:

  - Markdown
  - BBCode

## Options and Arguments

The following arguments are required:

  - `sources` can be specified mutliple times and are the source files to be converted. If multiple files are specified, they will be concatenated with a separator
  - `format` is the desired format and can be `markdown` or `bbcode`

The following are options that are not required:

  - `--source-format` can be used to specify the input format, otherwise it will be determined heuristically from the first input file
  - `-O, --output` can be used to specify the output destination; the default is to output in the current directory using the first source file's name with an appropriate extension
  - `--overwrite` will allow the output to be overwritten; if the destination file already exists and this option is not given, an exception will be raised
