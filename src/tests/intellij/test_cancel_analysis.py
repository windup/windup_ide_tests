import os
import time

import pytest

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/data/"


@pytest.mark.parametrize("app_name", ["weblogic_to_eap7"])
@pytest.mark.parametrize("ide", ["intellij"])
@pytest.mark.intellij
def test_cancel_analysis_intellij(configurations, setup_intellij, app_name, analysis_data, ide):
    """
    Tests the behaviour of canceling an analysis
    """
    intellij = setup_intellij

    # Intellij freezes without this sleep
    time.sleep(3)
    intellij.run_simple_analysis(app_name, wait_for_analysis_finish=False)
    intellij.cancel_analysis()
    intellij.wait_find_element(locator_type="image", locator="analysis_cancelled.png")
