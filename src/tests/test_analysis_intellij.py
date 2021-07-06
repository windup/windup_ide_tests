import time
from src.lib.config import config_data


def test_run_analysis(setup_intellij):
    """
    Test to run a simple analysis on existing project in IntelliJ IDE
    """
    intellij = setup_intellij
    time.sleep(10)
    intellij.open_mta_perspective()
    intellij.run_simple_analysis(project=config_data["project_path"])
    time.sleep(5)
    # assert intellij.is_analysis_complete()
