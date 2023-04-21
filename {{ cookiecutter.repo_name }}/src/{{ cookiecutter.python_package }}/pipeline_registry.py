"""Project pipelines."""
from platform import python_version
from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from kedro_mlflow.pipeline import pipeline_ml_factory
from pip._internal.operations.freeze import freeze


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()

    complete_pipeline = sum(pipelines.values())
    etl_pipeline = complete_pipeline.only_nodes_with_tags("etl")
    training_pipeline = complete_pipeline.only_nodes_with_tags("training")
    inference_pipeline = complete_pipeline.only_nodes_with_tags("inference")

    training_pipeline_ml = pipeline_ml_factory(
        training=training_pipeline,
        inference=inference_pipeline,
        input_name="raw_features",
        log_model_kwargs=dict(
            registered_model_name="{{ cookiecutter.azure_prefix }}_model",
            conda_env={
                "name": "mlflow-env",
                "channels": ["conda-forge"],
                "dependencies": [
                    f"python={python_version()}",
                    *[pkg.replace("==", "=") for pkg in freeze() if "pip" in pkg],
                    {"pip": [pkg for pkg in freeze() if "pip" not in pkg]},
                ],
            },
            code_path=["pyproject.toml", "src/{{ cookiecutter.python_package }}"],
            signature="auto",
        ),
    )

    return {
        "__default__": training_pipeline_ml,
        "etl": etl_pipeline,
        "training": training_pipeline_ml,
        "inference": inference_pipeline,
        "complete": complete_pipeline,
    }
