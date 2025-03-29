"""
This is the main script for running the parser.
Please see pysearch_tool/config.py to change any of configs.
"""
from pysearch_tool.config import BaseConfig
from pysearch_tool.relation_dict import RelationTree, insert, insert_cofi_examples, relation_dict
from pysearch_tool import dir_search
import json


def main(config):
    p = dir_search.Search(config)
    p.search()
    
    cofi_method_tree = RelationTree('CoFI')
    espresso_application_tree = RelationTree('Espresso')
    cofi_example_tree = RelationTree('CoFI Examples')
    
    for i in p.methods():
        insert(cofi_method_tree, i)
    
    for i in p.applications():
        insert(espresso_application_tree, i)
    
    for i in p.examples():
        insert_cofi_examples(cofi_example_tree, i)
    
    for i in p.tutorials():
        insert_cofi_examples(cofi_example_tree, i, isTutorial=True)

    file_cofi_method = "method_relation.json"
    file_espresso_application = "app_relation.json"
    file_cofi_example = "example_relation.json"

    relation_method = relation_dict(cofi_method_tree)
    relation_app = relation_dict(espresso_application_tree)
    relation_example = relation_dict(cofi_example_tree)

    with open(file_cofi_method, 'w') as fp:
        json.dump(relation_method, fp, indent=2)
    
    with open(file_espresso_application, 'w') as fp:
        json.dump(relation_app, fp, indent=2)

    with open(file_cofi_example, 'w') as fp:
        json.dump(relation_example, fp, indent=2)


if __name__ == "__main__": 
    main(BaseConfig())
