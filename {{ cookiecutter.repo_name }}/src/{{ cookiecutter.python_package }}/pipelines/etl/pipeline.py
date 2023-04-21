"""
This is a boilerplate pipeline 'etl'
generated using Kedro 0.18.7
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import extract_transform_load


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=extract_transform_load,
                inputs=["source_data", "params:label_column"],
                outputs=["raw_features", "raw_labels"],
                name="extract_transform_load",
                tags=["etl"],
            ),
        ]
    )
