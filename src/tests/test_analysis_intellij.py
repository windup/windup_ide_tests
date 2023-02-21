import time


def test_run_analysis(setup_intellij, configuration_name, configuration_data):
    intellij = setup_intellij
    time.sleep(3)
    intellij.open_mta_perspective()
    time.sleep(3)
    intellij.run_simple_analysis(configuration_name)
    assert intellij.is_analysis_complete()
    assert intellij.verify_story_points(configuration_data["target"][0])
