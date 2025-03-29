import os
import yaml
from typing import List


class Search:
    def __init__(self, config):
        """
        search earch repository in given path, extract the
        first line.

        Parameters
        ----------------
        method_path : str
            the folder that contains inference methods in CoFI
        app_path : str
            the folder that contains applications in espresso
        prob_path : str
            the folder that contains example problems in CoFI
            examples
        """
        # pysearch_tool/cofi/src/cofi/tools/
        self._method_path = config.search_folder + config.method_folder
        # pysearch_tool/espresso/contrib/
        self._application_path = config.search_folder + config.application_folder
        # pysearch_tool/cofi-examples/examples/
        self._examples_path = config.search_folder + config.example_folder
        # pysearch_tool/cofi-examples/tutorials/
        self._tutorial_path = config.search_folder + config.tutorial_folder
        self._config = config
        self._methods = []
        self._applications = []
        self._examples = []
        self._tutorials = []
        self._method_to_examples = {}
        self._method_tutorials = {}

    def methods(self):
        return self._methods
    
    def applications(self):
        return self._applications

    def examples(self):
        return self._examples
    
    def tutorials(self):
        return self._tutorials
    
    def search(self):
        def parse(file_path, mode):
            temp_line = None
            with open(file_path) as file:
                while True:
                    if temp_line:
                        line = temp_line
                        temp_line = None
                    else:
                        line = file.readline()
                    if line:
                        if "->" in line and "#" in line:
                            if mode == "Method":
                                method_tree = line.strip('\n')[2:].split(" -> ")
                                method_description = file.readline().strip('\n')[15:]
                                method = CoFIMethod(self._config.method_headfix + file_path[18:], method_tree, method_description)
                                
                                temp_line = file.readline()
                                if temp_line[:16] == '# documentation:':
                                    method._documentLink = temp_line[17:]
                                    temp_line = None
                                self._methods.append(method)
                            if mode == "Application":
                                app_tree = line.strip('\n')[2:].split(" -> ")
                                app_des = file.readline().strip('\n')[15:]
                                app_path = self._config.application_headfix + file_path[22:]
                                self._applications.append(EspressoApplication(app_path, app_tree, app_des))                    
                    else:
                        break

        # walk through pysearch_tool/cofi/src/cofi/tools/
        for _, _ , files in os.walk(self._method_path):
            for i in files:
                parse(self._method_path + i, mode="Method")

        # walk through pysearch_tool/espresso/contrib/
        for root, dirs, files in os.walk(self._application_path):
            if root == self._application_path:
                for dirr in dirs:
                    parse(self._application_path + dirr + '/' + dirr + '.py', mode="Application")
        
        # walk through pysearch_tool/cofi-examples/examples/
        for root, dirs, files in os.walk(self._examples_path):
            if root == self._examples_path:
                for dirr in dirs:
                    try:
                        path = self._examples_path + dirr + '/'
                        with open(path + 'meta.yml', 'r') as file:
                            data = yaml.safe_load(file)
                            for k in data['method'].keys():
                                github_path = self._config.example_headfix + "/"
                                github_path += path[37:]
                                description = data['description']
                                methods = data['method'][k]
                                if not isinstance(methods, list):
                                    description = methods['description']
                                    methods = methods['methods']
                                e = CoFIExample(name=data['title'], filename=k, 
                                                path=github_path + k, 
                                                tree=data['application domain'].split(" -> "), 
                                                des=description, methods=methods)
                                self._examples.append(e)
                    except Exception as e:
                        pass
            break
        
        # walk through pysearch_tool/cofi-examples/tutorials/
        for root, dirs, files in os.walk(self._tutorial_path):
            if root == self._tutorial_path:
                for dirr in dirs:
                    try:
                        path = self._tutorial_path + dirr + '/'
                        with open(path + 'meta.yml', 'r') as file:
                            data = yaml.safe_load(file)
                            for k in data['method'].keys():
                                github_path = self._config.tutorial_headfix + "/"
                                github_path += path[38:]
                                description = data['description']
                                methods = data['method'][k]
                                if not isinstance(methods, list):
                                    description = methods['description']
                                    methods = methods['methods']
                                e = CoFIExample(name=data['title'], filename=k,
                                                path=github_path + k, 
                                                tree=data['application domain'].split(" -> "),
                                                des=description, methods=methods)
                                self._tutorials.append(e)
                    except Exception as e:
                        pass
            break

        # attach examples & tutorials to methods
        for method in self.methods():
            for example in self.examples():
                if " -> ".join(method.tree()) in example.methods():
                    d = {}
                    d['name'] = example.name() + ' - ' + example.filename()
                    d['description'] = example.des()
                    d['linkToGit'] =  example.path()
                    method.add_examples(d)
            for tutorial in self.tutorials():
                if " -> ".join(method.tree()) in tutorial.methods():
                    d = {}
                    d['name'] = tutorial.name() + ' - ' + tutorial.filename()
                    d['description'] = tutorial.des()
                    d['linkToGit'] =  tutorial.path()
                    method.add_tutorials(d)

                    
class CoFIMethod:
    def __init__(self, path, tree, des):
        """
        A single Method defination.

        Parameters
        -----------
        name : str
            method name
        path : str
            method file path
        tree : list
            tree path of the method
        """
        self._path = path
        self._tree = tree
        self._des = des
        self._documentLink = None
        self._examples = []
        self._tutorials = []
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des
    
    def doc(self):
        return self._documentLink

    def examples(self):
        return self._examples
    
    def tutorials(self):
        return self._tutorials

    def add_examples(self, examples: List["CoFIExample"]):
        self._examples.append(examples)
    
    def add_tutorials(self, tutorials: List["CoFIExample"]):
        self._tutorials.append(tutorials)

    
class EspressoApplication:
    def __init__(self, path, tree, des):
        """
        A single Method defination.

        Parameters
        -----------
        name : str
            method name
        path : str
            method file path
        tree : list
            tree path of the method
        """
        self._path = path
        self._tree = tree
        self._des = des
        self._documentLink = None
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des
    
    def doc(self):
        return self._documentLink


class CoFIExample:
    def __init__(self, name, filename, path, tree, des, methods):
        """
        A single Method defination.

        Parameters
        -----------
        name : str
            method name
        path : str
            method file path
        tree : list
            tree path of the method
        """
        self._name = name
        self._filename = filename
        self._path = path
        self._tree = tree
        self._des = des
        self._methods = methods
        self._documentLink = None
    
    def name(self):
        return self._name

    def filename(self):
        return self._filename
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des
    
    def methods(self):
        return self._methods
    
    def doc(self):
        return self._documentLink
    
    def __repr__(self) -> str:
        return f"{self._name}: {self._filename}"
