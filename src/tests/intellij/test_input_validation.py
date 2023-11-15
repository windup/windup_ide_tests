import time

import pytest

from src.utils.general import generate_uuid
from src.utils.ocr import find_all_sentence_occurrences


@pytest.mark.intellij
def test_empty_input_validation(setup_intellij):
    """
    Analysis tests for intellij using various migration paths
    """

    intellij = setup_intellij
    intellij.delete_all_configurations()
    intellij.create_configuration_in_ui()
    intellij.run_simple_analysis("configuration0")

    # Intellij freezes without this sleep
    time.sleep(3)

    assert len(find_all_sentence_occurrences("Path to input required")) > 0


@pytest.mark.intellij
@pytest.mark.parametrize("app_name", ["weblogic_to_eap7"])
@pytest.mark.parametrize("ide", ["intellij"])
def test_invalid_input_validation(
    setup_intellij,
    app_name,
    intellij_config,
    config,
    analysis_data,
    ide,
):
    """
    Analysis tests for intellij using various migration paths
    """

    intellij = setup_intellij
    intellij.delete_all_configurations()

    analysis_data[app_name]["paths"][0] = "/invalid/input/path"
    uuid = generate_uuid()

    intellij.create_configuration_in_file(analysis_data, app_name, intellij_config, config, uuid)
    intellij.run_simple_analysis(app_name)

    # Intellij freezes without this sleep
    time.sleep(3)

    assert len(find_all_sentence_occurrences("Input location does not exist")) > 0
