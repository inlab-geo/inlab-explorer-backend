"""
This is the main script for running the parser.
Please see config.py to change any of configs.
"""
from config import BaseConfig
from relation_dict import RelationTree, insert, insert_cofi_examples, relation_dict
from pysearch_tool import dir_search
import json


def main(BaseConfig):
    p = dir_search.Search(BaseConfig)
    p._search()
    method_tree = RelationTree('CoFI')
    apps_tree = RelationTree('Espresso')
    example_tree = RelationTree('CoFI Examples')
    
    for i in p.methods():
        insert(method_tree, i)
    
    for i in p.applications():
        insert(apps_tree, i)
    
    for i in p.examples():
        insert_cofi_examples(example_tree, i)
    
    for i in p.tutorials():
        insert_cofi_examples(example_tree, i, isTutorial=True)

    method_rel_key = "method_relation.json"
    app_rel_key = "app_relation.json"
    example_rel_key = "example_relation.json"

    relation_method = relation_dict(method_tree)
    relation_app = relation_dict(apps_tree)
    relation_example = relation_dict(example_tree)

    with open(method_rel_key, 'w') as fp:
        json.dump(relation_method, fp, indent=2)
    
    with open(app_rel_key, 'w') as fp:
        json.dump(relation_app, fp, indent=2)

    with open(example_rel_key, 'w') as fp:
        json.dump(relation_example, fp, indent=2)


if __name__ == "__main__": 
    main(BaseConfig())
