import time

import pytest

from src.utils.general import generate_uuid
from src.utils.ocr import find_all_sentence_occurrences


@pytest.mark.intellij
def test_empty_cli_path_intellij(setup_intellij):
    """
    Tests the validation of empty cli path
    """
    intellij = setup_intellij

    # Intellij freezes without this sleep
    time.sleep(3)

    intellij.delete_all_configurations()
    intellij.create_configuration_in_ui()
    intellij.run_simple_analysis("configuration0")

    assert len(find_all_sentence_occurrences("")) > 0


@pytest.mark.intellij
@pytest.mark.parametrize("app_name", ["weblogic_to_eap7"])
def test_invalid_cli_path_intellij(
    setup_intellij,
    intellij_config,
    config,
    app_name,
    analysis_data,
):
    """
    Tests the validation of invalid cli path
    """
    intellij = setup_intellij

    # Intellij freezes without this sleep
    time.sleep(3)

    intellij.delete_all_configurations()
    config["windup_cli_path"] = "path/dont/exist"
    intellij.create_configuration_in_file(
        analysis_data,
        app_name,
        intellij_config,
        config,
        uuid=generate_uuid(),
    )

    assert len(find_all_sentence_occurrences("Path to CLI executable does not exist")) > 0
