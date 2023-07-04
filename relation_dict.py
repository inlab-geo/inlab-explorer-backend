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

tokens = {} #key: token id
textSize = 22

class hirc_tree:
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

    def to_pos(self):
        return [self.x, self.y,0,0]

def insert(tre, method):
        lst = method.tree()
        if len(lst)!= 1:
            token = lst.pop(0)
            if token == tre.me():
                flag = False
                child = lst[0]
                for tok in tre.children():
                    if child == tok.me():
                        insert(tok, method)
                        flag = True
                if not flag:
                    node = hirc_tree(child)
                    node.add_parent(token)
                    insert(node, method)
                    tre.add_child(node)
        else:
            tre.add_description(method.des())
            tre.add_path(method.path())
            
        return tre

def assign_depth(node, current_depth):
    node.depth = current_depth
    for child in node.children():
        assign_depth(child, current_depth + 1)

position_dict = {}
#-----------------------------------
def build_pos(node):
    spreation = 20
    if node.depth in position_dict.keys():
        position_dict[node.depth].append(node)
    else: 
        position_dict[node.depth] = [node]
    if node.children():
        for i in node.children():
            build_pos(i)

    for i in position_dict.keys():
        for j in position_dict[i]:
            j.x = 5201314
    return position_dict


#-------------------------------------
def create_layers(node):
    layers = {}
    assign_depth(node, 0)

    def add_to_layer(node):
        depth = node.depth
        if depth not in layers:
            layers[depth] = []
        layers[depth].append(node)

        for child in node.children():
            add_to_layer(child)

    add_to_layer(node)
    return layers

def assign_coordinates(tree, separation_x=20, separation_y=150):
    layers = create_layers(tree)
    res = []
    center = 0
    temp_parent_node_x = {}
    for layer in list(layers.keys())[::-1]:
        assign_node_in_layer(layers[layer],center,separation_x)


def assign_node_in_layer(nodes, center, separation_x):
    for node in nodes:
        print(node.me())

    layter_width = sum([max(node.width, node.ch_width) for node in nodes]) + (len(nodes) - 1) * separation_x
    start_x = center - layter_width / 2
    for node in nodes:
        print(start_x)
        if (node.x) :
            start_x += node.ch_width
        else:
            node.x = start_x
            start_x += max(node.width, node.ch_width) + separation_x




def dict_package(node):
    res = {}
    load_to_dict(node,res)
    offsetX = 150 - res[node.me()][0]
    offsetY = 120 - res[node.me()][1]
    for i in res.values():
        i[0] += offsetX
        i[1] += offsetY
    
    return res

def load_to_dict(node, res):
    res[node.me()] = node.to_pos()
    for i in node.children():
        load_to_dict(i, res)
#----------------------

def description(node):
    res = {}
    pack_des(res,node)
    return res

def pack_des(dict,node):
    dict[node.me()] = node.description()
    if node.children():
        for i in node.children():
            pack_des(dict,i)

#-------------------------
def relation_dict(node):
    return relation_pack(node)

def relation_pack(node):
    node_dict = {}
    node_dict["name"] = node.me()
    node_dict["link_git"] = node.path()
    node_dict["link_doc"] = "www.google.com.au"
    node_dict["children"] = []
    node_dict["description"] = node.description()
    if node.children():
        for j in node.children():
            node_dict["children"].append(relation_pack(j))
    return node_dict





#------------------------


# tokens1 = ['cofi_simple_newton', 'simple Newton step', 'InLab', 'non-linear', 'optimization', 'parameter estimation', 'CoFI']
# tokens2 = ['pygimli_dcip_century_tri_mesh.ipynb', 'Newton conjugate gradient trust-region algorithm (trust-ncg)', 'scipy.optimize.minimize',  'non-linear', 'optimization', 'parameter estimation', 'CoFI']

# tre = hirc_tree('CoFI', [])

# t = insert(tre, tokens1[::-1])
# t1 = insert(t, tokens1[::-1])


# print(t1.children()[0].children()[0].me())
