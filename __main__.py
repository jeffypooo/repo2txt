"""
Usage:
    python __main__.py [repo_url] [output_path] --flags...

Positional Arguments:
    repo_url (str): The URL of the Git repository to textify.
    output_path (str): The path of the output text file.

Flags:
    --extensions:  A list of file extensions to include in the text file. (default: .c, .cc, .cpp, .cs, .css, .go, .h, .html, .java, .js, .kt, .m, .php, .py, .rb, .rs, .swift, .ts, .vb, .vue, .json, .xml, .yaml, .toml, .md, .yml, .sql)
"""



import argparse
import repo2txt


def main() -> None:
    parser = argparse.ArgumentParser(description="Textify a Git repository")
    parser.add_argument("repo_url", type=str, help="The URL of the Git repository to textify.")
    parser.add_argument("output_path", type=str, help="The path of the output text file.")
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=repo2txt.COMMON_LANGUAGE_EXTENSIONS,
        help="A list of file extensions to include in the text file.",
    )

    args = parser.parse_args()

    repo2txt.textify_repo(args.repo_url, args.output_path, args.extensions)
    

if __name__ == "__main__":
    main()

