# Introduction
This Python module copies all files and folders of an AWS CodeCommit repository.
It was written for the purpose of copying all files of a CodeCommit repository into an AWS Lambda function.

# Usage
codecommitcloner uses boto3 and will search for credentials in the standard manner.

```python
from codecommitcloner import copy
repo = "repo-name"
copy(repo) # copies the codecommit repository in a folder with the same name as the repository
copy(repo, "newname") # copies the codecommit repository in a folder called "newname"
copy(repo, dest="./newname") # does the same as the command before
copy(repo, dest="./newname", repo_folder="src") # copies recursively starting from the top-level folder src
```
