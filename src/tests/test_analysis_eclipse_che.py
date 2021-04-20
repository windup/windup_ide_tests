def test_run_analysis(setup_eclipse_che):
    """
    Test to run a simple analysis in Eclipse Che IDE
    and assert the story points
    """
    eclipse_che = setup_eclipse_che
    story_points = eclipse_che.run_analysis()
    assert int(story_points) == 35
