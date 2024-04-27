
import os
import datetime
from git import Repo
from typing import TextIO
from typing import List
from rich.console import Console
from rich.status import Status
from rich.live import Live


# List of 25 most popular programming language file extensions
COMMON_LANGUAGE_EXTENSIONS = [
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".css",
    ".go",
    ".h",
    ".html",
    ".java",
    ".js",
    ".kt",
    ".m",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".swift",
    ".ts",
    ".vb",
    ".vue",
    ".json",
    ".xml",
    ".yaml",
    ".toml",
    ".md",
    ".yml",
    ".sql",
]

def _create_output_file(output_path: str) -> TextIO:
    """
    Creates an output text file for the repository content.

    Args:
    output_path (str): The path of the output text file.

    Returns:
    TextIO: File object for the output file.
    """
    try:
        file = open(output_path, "w+")
        return file
    except Exception as e:
        print(f"Failed to create the output file: {str(e)}")


def _clone_repo(git_repo_url: str, status: Status) -> Repo:
    """
    Clones the Git repository to the specified local directory.

    Args:
    git_repo_url (str): URL of the Git repository to clone.
    local_dir (str): Local directory path where the repo should be cloned.
    """
    try:
        # Create a temporary directory to clone the repository
        local_dir = f"temp_{datetime.datetime.now().isoformat()}"
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        elif os.listdir(local_dir):
            raise Exception(f"Directory {local_dir} is not empty. Please provide an empty directory.")

        # Clone the repository
        def _update(opc, cur_count, max_count=None, message=''):
            # There are 9 opcodes represented by a single bit, shifted by the opcode index
            # Note that we ignore BEGIN and END opcodes (0x1 and 0x2)
            beg_end_bitmask = 0xFC
            opc &= beg_end_bitmask
            opc_str = ""
            if opc & 0x4:
                opc_str = "Counting files..."
            if opc & 0x8:
                opc_str = "Compressing..."
            if opc & 0x10:
                opc_str = "Writing objects..."
            if opc & 0x20:
                opc_str = "Receiving objects..."
            if opc & 0x40:
                opc_str = "Resolving deltas..."
            if opc & 0x80:
                opc_str = "Finding sources..."
            if opc & 0x100:
                opc_str = "Checking out files..."
            status.update(f"[bold white]{opc_str} {cur_count}/{max_count} {message}")
        
        repo = Repo.clone_from(git_repo_url, local_dir, progress=_update)
        return repo
    except Exception as e:
        raise e

def textify_repo(
    url: str,
    output_path: str,
    file_extensions: List[str] = COMMON_LANGUAGE_EXTENSIONS
) -> None:
    """
    Recursively walks the repository and appends the content to a continuous text file.
    
    Args:
    url (str): The URL of the Git repository to textify.
    output_path (str): The path of the output text file.
    file_extensions (List[str]): List of file extensions to include in the text file.
    """
    console = Console()
    skipped_count = 0
    textified_count = 0
    try:
        with console.status(f"[bold green] Cloning from {url}...") as status:
            repo = _clone_repo(url, status=status)
        with console.status(f"[bold green] Textifying repository...") as status:
            with _create_output_file(output_path) as file:
                for root, _, files in os.walk(repo.working_dir):
                    for file_name in files:
                        status.update(f"[bold white]Processing {file_name}")
                        extension = os.path.splitext(file_name)[1]
                        if extension not in file_extensions:
                            skipped_count += 1
                            continue
                        file_path = os.path.join(root, file_name)
                        with open(file_path, "r") as f:
                            try:
                                file_text = f.read()
                                file.write(f"\n\n# {file_path}\n\n")
                                file.write(file_text)
                                textified_count += 1
                            except Exception as e:
                                file_name = file_path.split("/")[-1]
                                skipped_count += 1
                                continue

    except Exception as e:
        console.print(f"[bold red]Failed to textify the repository: {str(e)}")

    console.print(f"[bold green]Textified {textified_count} files.")
    console.print(f"[bold yellow]Skipped {skipped_count} files.")
    console.print(f"[bold green]Textification complete. Output saved to {output_path}")

    
    # Delete the cloned repository
    try:
        os.system(f"rm -rf {repo.working_dir}")
    except Exception as e:
        print(f"Failed to delete the cloned repository: {str(e)}")