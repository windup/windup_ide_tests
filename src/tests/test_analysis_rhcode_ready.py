def test_run_analysis(setup_codereadystudio):
    """
    Test to run a simple analysis on existing project in CodeReadyStudio IDE
    """
    codereadystudio = setup_codereadystudio
    codereadystudio.open_mta_perspective()
    codereadystudio.run_simple_analysis(project='acme')
    assert codereadystudio.is_analysis_complete()
