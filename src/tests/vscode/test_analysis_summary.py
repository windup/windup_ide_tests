import json
import os

import pytest

from src.models.configuration.configuration import Configuration
from src.models.configuration.summery import Summary

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/data/"
MIN = 60


@pytest.mark.parametrize("app_name", ["classifications check"])
@pytest.mark.parametrize("analysis_data", [{
    "classifications check": {"options": {"target": ["eap8"]}},
}])
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_no_generated_classifications(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates polarion MTA-503
    vscode = setup_vscode
    vscode.set_focus()
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(app_name)
    status, message = vscode.is_analysis_complete(timeout=(5 * MIN))
    assert status, message

    configuration: Configuration = vscode.configurations_object.get_configuration(app_name)
    analysis_summery: Summary = configuration.summary

    assert analysis_summery.classification_count == 0, f"{str(analysis_summery.classification_count)} classifications were generated"
