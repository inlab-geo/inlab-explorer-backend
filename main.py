"""
This is the main script for running the parser.
Please see config.py to change any of configs.
"""
from config import Base_config
from relation_dict import hirc_tree, insert, insert_cofi_examples, relation_dict
from pysearch_tool import dir_search
import json


def main(Base_config):
    p = dir_search.Search(Base_config)
    p._search()
    method_tree = hirc_tree('CoFI')
    apps_tree = hirc_tree('Espresso')
    example_tree = hirc_tree('CoFI Examples')
    
    for i in p.mds():
        insert(method_tree,i)
    
    for i in p.aps():
        insert(apps_tree,i)
    
    for i in p.examples():
        insert_cofi_examples(example_tree,i)

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
