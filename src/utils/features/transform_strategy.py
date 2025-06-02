from abc import ABC, abstractmethod

from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils.features.postprocessor_strategy import (PostprocessorStrategy,DefaultLstmPostprocessor)

class TransformStrategy(ABC):
    @abstractmethod
    def fit(self, X, y=None):
        pass

    @abstractmethod
    def transform(self, X, y=None):
        pass

    @abstractmethod
    def fit_transform(self, X, y=None):
        pass

    @abstractmethod
    def get_feature_names(self):
        pass

    @abstractmethod
    def get_postprocessor(self) -> PostprocessorStrategy:
        pass


class DefaultLstmTransformStrategy(TransformStrategy):
    def __init__(
    self, 
    numeric_transformer=StandardScaler(),
    categorical_transformer=OneHotEncoder(sparse_output=False, handle_unknown='ignore')):
            
        self._numeric_transformer = numeric_transformer
        self._categorical_transformer = categorical_transformer

        # Define a ColumnTransformer
        self.column_transformer = ColumnTransformer(
            transformers=[
                ('numeric', self._numeric_transformer, make_column_selector(dtype_include="number")),
                ('categorical', self._categorical_transformer, make_column_selector(dtype_include="object"))
                ],
            remainder='passthrough'
        )
        

    def fit(self, X, y=None):
        self.column_transformer.fit(X, y)
        return self

    def transform(self, X, y=None):
        return self.column_transformer.transform(X)

    def fit_transform(self, X, y=None):
        return self.column_transformer.fit_transform(X, y)
    
    def get_postprocessor(self,selected_features = None)->PostprocessorStrategy:

        filtered_transformers = []

        for name, transformer, columns in self.column_transformer.transformers:
            # Se o ColumnTransformer for baseado em nomes de colunas:
            if isinstance(columns, list):
                # Mantém apenas colunas desejadas
                filtered_cols = [col for col in columns if col in selected_features]

                if filtered_cols:
                    filtered_transformers.append((name, transformer, filtered_cols))

        return DefaultLstmPostprocessor(ColumnTransformer(transformers=filtered_transformers))
    
    def get_feature_names(self, input_features = None):
        return self.column_transformer.get_feature_names_out(input_features=input_features)

    def get_params(self, deep=True):
        return self.column_transformer.get_params(deep)

    def set_params(self, **params):
        self.column_transformer.set_params(**params)
        return self
    