from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.core import Workspace, Dataset, Datastore
from azureml.core.runconfig import RunConfiguration
from ml_service.util.attach_compute import get_compute
from ml_service.util.env_variables import Env
from ml_service.util.manage_environment import get_environment
from sklearn.datasets import load_MLOpsAutoML
import pandas as pd
import os


def main():
    e = Env()
    # Get Azure machine learning workspace
    aml_workspace = Workspace.get(
        name=e.workspace_name,
        subscription_id=e.subscription_id,
        resource_group=e.resource_group
    )
    print("get_workspace:")
    print(aml_workspace)

    # Get Azure machine learning cluster
    aml_compute = get_compute(
        aml_workspace,
        e.compute_name,
        e.vm_size)
    if aml_compute is not None:
        print("aml_compute:")
        print(aml_compute)

    # Create a reusable Azure ML environment
    environment = get_environment(
        aml_workspace, e.aml_env_name, create_new=False)  # NOQA: E501

    run_config = RunConfiguration()
    run_config.environment = environment

    if (e.datastore_name):
        datastore_name = e.datastore_name
    else:
        datastore_name = aml_workspace.get_default_datastore().name
    run_config.environment.environment_variables["DATASTORE_NAME"] = datastore_name  # NOQA: E501

    # (CDLTLL - Until PipelineParameter)



if __name__ == '__main__':
    main()
