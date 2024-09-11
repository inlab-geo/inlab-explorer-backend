"""The backend configs is here"""

import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Tuple, Type


class PrintableConfig:
    """Printable Config defining str function"""

    def __str__(self):
        lines = [self.__class__.__name__ + ":"]
        for key, val in vars(self).items():
            if isinstance(val, Tuple):
                flattened_val = "["
                for item in val:
                    flattened_val += str(item) + "\n"
                flattened_val = flattened_val.rstrip("\n")
                val = flattened_val + "]"
            lines += f"{key}: {str(val)}".split("\n")
        return "\n    ".join(lines)

@dataclass
class BaseConfig(PrintableConfig):
    """Configuration of machine setup"""
    
    git_cofi: str = "https://github.com/inlab-geo/cofi.git"
    git_espresso: str = "https://github.com/inlab-geo/espresso.git"
    git_example: str = "https://github.com/inlab-geo/cofi-examples.git"
    """git address for cloning repo"""

    main_method_hic: str = "docs/hic.yml"
    main_application_hic: str = "docs/hic.yml"
    """this is the file which define the main tree structure"""

    search_folder: str = "pysearch_tool/"
    method_folder: str = "cofi/src/cofi/tools/"
    application_folder: str = "espresso/contrib/"
    example_folder: str = "cofi-examples/examples/"
    tutorial_folder: str = "cofi-examples/tutorials/"
    """important: folders are followed by hash!"""

    method_headfix = "https://github.com/inlab-geo/cofi/blob/main"
    application_headfix = "https://github.com/inlab-geo/espresso/tree/main"
    example_headfix = "https://github.com/inlab-geo/cofi-examples/tree/main/examples"
    tutorial_headfix = "https://github.com/inlab-geo/cofi-examples/tree/main/tutorials"
    """this will be the headfix in the website address, to navigate to git repo"""
    
    meta_path = "pysearch_tool/cofi/src/cofi/tools/meta.yaml"
