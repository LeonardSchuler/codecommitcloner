import boto3
from pathlib import Path
import logging


logging.basicConfig(encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)
client = boto3.client("codecommit")


def download_file(repo: str, blob_id: str) -> bytes:
    """
    Returns the file (specified by the blob_id) in bytes from a codecommit repository.

    Parameters
    ----------
    repo : str
        Name of the codecommit repository.
    blob_id: str
        Identifies a file in a codecommit repository.
    Returns
    -------
    file : bytes
        Codecommit file in bytes 
    """
    response = client.get_blob(
            repositoryName=repo,
            blobId=blob_id
            )
    content = response['content']
    return content

def ls(repo: str, folder: str):
    """
    Returns the files and subfolders of a folder in a repository.

    Parameters
    ----------
    repo : str
        Name of the codecommit repository.
    folder: str
        Folder in the codecommit repository.
    Returns
    -------
    (files, subfolders) : list of dictionaries
    """
    response = client.get_folder(
        repositoryName=repo,
        folderPath=folder
    )
    # keys: 'files', 'subFolders', 'subModules', 'symbolicLinks'
    subfolders = response['subFolders']
    files = response['files']
    return files, subfolders

def mkdir(path: Path):
    logger.info(f"mkdir: {path}")
    path.mkdir(parents=True, exist_ok=True)

def copy(repo: str, dest='./', repo_folder='/') -> None:
    """
    Copies a codecommit repository starting from repo_folder to a destination on the drive.

    Parameters
    ----------
    repo : str
        Name of the codecommit repository.
    dest: str
        Destination to copy to on your filesystem.
    repo_folder: str
        Folder in the codecommit repository.
    """
    if dest == './':
        dest = Path(f"{repo}")
    else:
        dest = Path(dest)

    if repo_folder == '/':
        mkdir(dest)
    else:
        mkdir(dest / repo_folder)

    logger.info(f"Copying folder: {repo_folder}")
    files, subfolders = ls(repo, repo_folder)
    for file in files:
        # file keys 'absolutePath', 'blobId', 'fileMode', 'realtivePath', 'treeId'
        logger.info(f"Copying file: {file['absolutePath']}")
        content = download_file(repo, file['blobId'])
        with open(dest / file['absolutePath'], 'wb') as f:
            f.write(content)

    for folder in subfolders:
        # folder keys 'absolutePath', 'realtivePath', 'treeId'
        copy(repo, dest, repo_folder=folder['absolutePath'])



if __name__ == '__main__':
    repo = "repo-name"
    copy(repo)
