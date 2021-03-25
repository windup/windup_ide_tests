

def test_run_analysis(setup_eclipse):
    """
    Test to run a simple analysis on existing project in Eclipse IDE
    """
    eclipse = setup_eclipse
    eclipse.open_mta_perspective()
    eclipse.run_simple_analysis(project='acme')
    assert eclipse.is_analysis_complete()
