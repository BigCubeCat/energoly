from .Types import Generator
import json
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree._tree import Tree
from sklearn.ensemble import RandomForestRegressor


class WindGenerator(Generator):
    def __init__(self, index, parents, name, rent_price, weather_wind_all, coordinate, power_wind) -> None:
        super().__init__(index, parents, name)
        self.setBill(rent_price)

        self.model = self.load_model()
        self.weather_sun_all = weather_wind_all
        self.coordinate = coordinate
        self.power_wind = power_wind

    def deserialize_decision_tree_regressor(self, model_dict):
        deserialized_decision_tree = DecisionTreeRegressor()

        deserialized_decision_tree.max_features_ = model_dict['max_features_']
        deserialized_decision_tree.n_features_ = model_dict['n_features_']
        deserialized_decision_tree.n_outputs_ = model_dict['n_outputs_']

        tree = self.deserialize_tree(model_dict['tree_'], model_dict['n_features_'], 1, model_dict['n_outputs_'])
        deserialized_decision_tree.tree_ = tree

        return deserialized_decision_tree

    def deserialize_tree(self, tree_dict, n_features, n_classes, n_outputs):
        tree_dict['nodes'] = [tuple(lst) for lst in tree_dict['nodes']]

        names = ['left_child', 'right_child', 'feature', 'threshold', 'impurity', 'n_node_samples',
                 'weighted_n_node_samples']
        tree_dict['nodes'] = np.array(tree_dict['nodes'],
                                      dtype=np.dtype({'names': names, 'formats': tree_dict['nodes_dtype']}))
        tree_dict['values'] = np.array(tree_dict['values'])

        tree = Tree(n_features, np.array([n_classes], dtype=np.intp), n_outputs)
        tree.__setstate__(tree_dict)

        return tree

    def load_model(self):
        try:
            # ссылка на файл: https://drive.google.com/file/d/1u14dhbunno4kqDhfdgnsjWl28bDiSt0U/view?usp=sharing
            with open('model_good_a1_v-full.json', 'r') as model_json:
                model_dict = json.load(model_json)
                model = RandomForestRegressor(**model_dict['params'])
                estimators = [
                    self.deserialize_decision_tree_regressor(decision_tree) for decision_tree in model_dict['estimators_']
                ]
                model.estimators_ = np.array(estimators)
                model.n_features_ = model_dict['n_features_']
                model.n_outputs_ = model_dict['n_outputs_']
                  
                return model
        except FileNotFoundError:
            print("\n\n\nCсылка на модель для нейронки, скачай!!!: https://drive.google.com/file/d/1u14dhbunno4kqDhfdgnsjWl28bDiSt0U/view?usp=sharing\n\n\n")
            return

    def update(self, tick):
        data = [
            self.weather_sun_all[tick - 3] ** 5 if tick >= 3 else 0,
            self.weather_sun_all[tick - 2] ** 5 if tick >= 2 else 0,
            self.weather_sun_all[tick - 1] ** 5 if tick >= 1 else 0,
            self.weather_sun_all[tick] ** 5,
            self.coordinate[0],
            self.coordinate[1],
            self.power_wind
        ]
        data_normal = [[0]*7, data]
        result = self.model.predict(data_normal)[1]
        return result

