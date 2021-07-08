import time

from src.lib.config import config_data


def test_run_analysis(setup_intellij):
    """
    Test to run a simple analysis on existing project in IntelliJ IDE
    """
    intellij = setup_intellij
    intellij.open_mta_perspective()
    # Intellij freezes without this sleep
    time.sleep(3)
    intellij.run_simple_analysis(project=config_data["project_path"], target="eap7")
    assert intellij.is_analysis_complete()
    assert intellij.verify_story_points()
