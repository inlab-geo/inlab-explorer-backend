## Introduction

This package is designed to parse hierarchical information from CoFi, espresso, and cofi-examples. The generated JSON file will be loaded into the public folder in the frontend.


### Manaually run the backend
To run the backend manually, please first place the 'cofi', 'espresso', and 'cofi-examples' folders into the 'pysearch_tool' directory. Then execute the following command:

```bash
python main.py
```

This command generates three JSON files. Please transfer these files into the 'public' folder in the frontend for visualization.

If you want to use any other packages, please put the package in the "requirement.txt", it will be loaded in Git Action.



### Configs:

You may change many config in config.py, include path, working directory, link prefix etc.

### Main workflow:

The main workflow is defined in 'main.py'. It initiates the search script in the 'pysearch' folder ('dir_search.py'), and then packages the tree. The tree structure is defined in the 'relation_dict.py'.

### Git Action

The GitHub Action for the backend works by first downloading the source files, then running the script, and finally pushing the generated JSON files (which are located in the root folder) to the 'public' folder in the frontend.
