"""
This is a boilerplate pipeline
generated using Kedro 0.18.7
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import make_predictions, preprocess, split_data, train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess,
                inputs="raw_features",
                outputs="features",
                name="preprocess",
                tags=["training", "inference"],
            ),
            node(
                func=split_data,
                inputs=[
                    "features",
                    "raw_labels",
                    "params:train_fraction",
                    "params:random_state",
                ],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data",
                tags=["training"],
            ),
            node(
                func=train_model,
                inputs=["X_train", "X_test", "y_train", "y_test", "params:n_neighbors"],
                outputs=["trained_model", "accuracy"],
                name="train_model",
                tags=["training"],
            ),
            node(
                func=make_predictions,
                inputs=["trained_model", "features"],
                outputs="predictions",
                name="make_predictions",
                tags=["inference"],
            ),
        ]
    )
