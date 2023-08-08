import time
import pytest

from src.utils.OCR import find_all_string_occurrences


@pytest.mark.parametrize("app_name", ["weblogic_to_eap7"])
def test_cli_validation_intellij(setup_intellij, app_name, analysis_data):
    """
    Tests the validation of CLI path
    """
    intellij = setup_intellij

    # Intellij freezes without this sleep
    time.sleep(3)

    intellij.delete_all_configurations()
    intellij.create_configuration()
    intellij.run_simple_analysis("configuration0")

    assert len(find_all_string_occurrences("Path to CLI executable required")) > 0

    intellij.delete_all_configurations()
    intellij.create_configuration()
