def test_run_analysis(setup_vscode):
    """
    Test to run a simple analysis on existing project in VSCode IDE
    """
    vscode, config = setup_vscode
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(project=config["project_path"])
    assert vscode.is_analysis_complete()
