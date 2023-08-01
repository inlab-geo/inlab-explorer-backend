"""
This is the main script for running the parser.
Please see config.py to change any of configs.
"""


from config import Base_config
from relation_dict import hirc_tree, insert, relation_dict
from pysearch_tool import dir_search
import json
# import boto3








def main(Base_config):
    p = dir_search.Search(Base_config)
    p._search()
    method_tree = hirc_tree('CoFI')
    apps_tree = hirc_tree('37 EARTH SCIENCES')
    example_tree = hirc_tree('37 EARTH SCIENCES')
    
    for i in p.mds():
        method_tree = insert(method_tree,i)
    
    for i in p.aps():
        apps_tree = insert(apps_tree,i)
    
    for i in p.examples():
        example_tree = insert(example_tree,i)


    method_rel_key = "method_relation.json"
    app_rel_key = "app_relation.json"
    example_rel_key = "example_relation.json"

    relation_method = relation_dict(method_tree)
    relation_app = relation_dict(apps_tree)
    relation_example = relation_dict(example_tree)

    with open(method_rel_key, 'w') as fp:
        json.dump(relation_method, fp)
    
    with open(app_rel_key, 'w') as fp:
        json.dump(relation_app, fp)

    with open(example_rel_key, 'w') as fp:
        json.dump(relation_example, fp)




if __name__ == "__main__": 
    main(Base_config())
