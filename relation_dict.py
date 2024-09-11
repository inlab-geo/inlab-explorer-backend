# An example labelling for CoFI methods

#     cofi_simple_newton <- simple Newton step <- InLab 
# <- non-linear <- optimization <- parameter estimation <- CoFI



# An example labelling for Espresso problems

#     magnetotelluric_1D <- magnetotelluric <- 
#  370602 Electrical and electromanetic methods in geophysics <- 
#  3706 Geophysics <- 37 Earth Sciences



# An example labelling for CoFI examples: pygimli_dcip_century_tri_mesh.ipynb

#     Application domain: pygimli_dcip_century_tri_mesh.ipynb <- DCIP 
#   <- 370602 Electrical and electromanetic methods in geophysics 
#   <- 3706 Geophysics <- 37 Earth Sciences
#     Methods domain: pygimli_dcip_century_tri_mesh.ipynb <- Newton conjugate gradient trust-region algorithm (trust-ncg) <- scipy.optimize.minimize <- non-linear <- optimization <- parameter estimation <- CoFI



# Another example labelling for CoFI examples

#     Application domain: pygimli_dcip.ipynb <- DCIP <- 370602 Electrical and electromanetic methods in geophysics <- 3706 Geophysics <- 37 Earth Sciences
#     Methods domain:
#         pygimli_dcip.ipynb <- Newton conjugate gradient trust-region algorithm (trust-ncg) <- scipy.optimize.minimize <- non-linear <- optimization <- parameter estimation <- CoFI
#         pygimli_dcip.ipynb <- RAdam <- torch.optim <- non-linear <- optimization <- parameter estimation <- CoFI

from config import BaseConfig
from pysearch_tool.dir_search import Example


class RelationTree:
    def __init__(self, me):
        """
        relationship tree for as parsing result

        Parameters
        ----------------
        me : str
            current leaf name
       
        child : [hirc_tree]
            current leaf's children
        """
        self._me = me
        self._children = []
        self._parent = None
        self._path = None
        self._description = None
        self._examples = []
        self._tutorials = []
        self._doc = None

        #---graphics property
        self.x = None
        self.y = None
        self.modifier = 0
        self.width = max(220,len(me) * 22)
        self.ch_width = 0

    def me(self):
        return self._me
    
    def children(self):
        return self._children
    
    def parent(self):
        return self._parent
    
    def add_child(self, node):
        self._children.append(node)

    def add_parent(self, node):
        self._parent = node
    
    def add_description(self, des):
        self._description = des
    
    def add_path(self, path):
        self._path = path
    
    def description(self):
        return self._description
    
    def path(self):
        return self._path

    def examples(self):
        return self._examples
    
    def tutorials(self):
        return self._tutorials

    def add_examples(self, e: Example):
        for i in e:
            if i['name'] not in [j['name'] for j in self._examples]:
                self._examples.append(i)
                
    def add_tutorials(self, e: Example):
        for i in e:
            if i['name'] not in [j['name'] for j in self._tutorials]:
                self._tutorials.append(i)

    def add_doc(self, d):
        self._doc = d

    def doc(self):
        return self._doc


def insert(tre, node):
        try:    # CoFI methods
            tre.add_examples(node.examples())
            tre.add_tutorials(node.tutorials())
        except Exception as e:      # Espresso application domains
            pass
        lst = node.tree()
        if len(lst)!= 1:
            token = lst.pop(0)
            if token == tre.me():
                flag = False
                child = lst[0]
                for tok in tre.children():
                    if child == tok.me():
                        insert(tok, node)
                        flag = True
                if not flag:
                    btree = RelationTree(child)
                    btree.add_parent(token)
                    insert(btree, node)
                    tre.add_child(btree)
        else:
            tre.add_description(node.des())
            tre.add_path(node.path())
            tre.add_doc(node.doc())
            
        return tre

def insert_cofi_examples(tree, node: Example, isTutorial=False):
    # Start at the root
    current_node = tree

    # Traverse the node's tree path, navigating/creating nodes as necessary
    for level in node.tree():
        # Prevent duplicate "CoFI Examples" as a child of the root
        if current_node == tree and level == "CoFI Examples":
            matching_children = [tree]
        else:
            # Check if a child with the current level's name already exists
            matching_children = [child for child in current_node.children() if child.me() == level]

        # If the child exists, navigate to it
        if matching_children:
            current_node = matching_children[0]
        # If the child doesn't exist, create it and navigate to it
        else:
            new_child = RelationTree(level)
            new_child.add_parent(current_node)
            current_node.add_child(new_child)
            current_node = new_child

        # Add the filename as an example to the current node's examples list
        if isTutorial:
            tutorial = {
                'name': node.filename(),
                'description': node.des(),
                'linkToGit': node.path(),
            }
            if tutorial not in current_node.tutorials():
                current_node.add_tutorials([tutorial])
        else:
            example = {
                'name': node.filename(), 
                'description': node.des(), 
                'linkToGit': node.path(), 
            }
            if example not in current_node.examples():
                current_node.add_examples([example])


def relation_dict(node):
    return relation_pack(node)

def relation_pack(node):
    data_doc = {}
    data_git = {}
    data_des = {}
    with open(BaseConfig.search_folder + BaseConfig.method_folder + "__init__.py") as file:
        while True:
            line = file.readline()
            if line:
                if line.startswith("# link_doc: "):
                    data_doc[line.strip('\n')[12:].split(" -> ")[0]] = line.strip('\n')[12:].split(" -> ")[1]
                if line.startswith("# link_git: "):
                    data_git[line.strip('\n')[12:].split(" -> ")[0]] = line.strip('\n')[12:].split(" -> ")[1]
                if line.startswith("# description: "):
                    data_des[line.strip('\n')[15:].split(" -> ")[0]] = line.strip('\n')[15:].split(" -> ")[1]
            else:
                break
        node_dict = {}
        node_dict["name"] = node.me()
 
        if node.me() in data_git.keys():
            node_dict["link_git"] = data_git[node.me()]
        else:
            node_dict["link_git"] = node.path()
        
        if node.me() in data_doc.keys():
            node_dict["link_doc"] = data_doc[node.me()]
        else:
            node_dict["link_doc"] = node.doc()
            
        if node.me() in data_des.keys():
            node_dict["description"] = data_des[node.me()]
        else:
            node_dict["description"] = node.description()
        
        if node.examples():
            node_dict["examples"] = node.examples()
        if node.tutorials():
            node_dict["tutorials"] = node.tutorials()
        
        node_dict["children"] = []
        if node.children():
            for j in node.children():
                node_dict["children"].append(relation_pack(j))
        return node_dict


#------------------------

