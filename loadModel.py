import json
import numpy as np
import zlib
from io import StringIO

from sklearn.tree import DecisionTreeRegressor
from sklearn.tree._tree import Tree
from sklearn.ensemble import RandomForestRegressor


def deserialize_decision_tree_regressor(model_dict):
    deserialized_decision_tree = DecisionTreeRegressor()

    deserialized_decision_tree.max_features_ = model_dict['max_features_']
    # deserialized_decision_tree.n_features_ = model_dict['n_features_']
    deserialized_decision_tree.n_outputs_ = model_dict['n_outputs_']

    tree = deserialize_tree(model_dict['tree_'], model_dict['n_features_'], 1, model_dict['n_outputs_'])
    deserialized_decision_tree.tree_ = tree

    return deserialized_decision_tree


def deserialize_tree(tree_dict, n_features, n_classes, n_outputs):
    tree_dict['nodes'] = [tuple(lst) for lst in tree_dict['nodes']]

    names = ['left_child', 'right_child', 'feature', 'threshold', 'impurity', 'n_node_samples',
             'weighted_n_node_samples']
    tree_dict['nodes'] = np.array(tree_dict['nodes'],
                                  dtype=np.dtype({'names': names, 'formats': tree_dict['nodes_dtype']}))
    tree_dict['values'] = np.array(tree_dict['values'])

    tree = Tree(n_features, np.array([n_classes], dtype=np.intp), n_outputs)
    tree.__setstate__(tree_dict)

    return tree


def load_model(filename="compress_model"):
    with open(filename, 'rb') as data:
        compress = data.read()
        decompress = zlib.decompress(compress).decode('utf-8')
        prev_model = StringIO(decompress)

    model_dict = json.load(prev_model)

    params = model_dict['params']
    params.pop('min_impurity_split')

    model = RandomForestRegressor(**params)
    estimators = [
        deserialize_decision_tree_regressor(decision_tree) for decision_tree in model_dict['estimators_']
    ]
    model.estimators_ = np.array(estimators)
    # model.n_features_ = model_dict['n_features_']
    model.n_outputs_ = model_dict['n_outputs_']

    return model
