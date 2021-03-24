

def test_run_analysis(setup_codereadystudio):
    codereadystudio = setup_codereadystudio
    codereadystudio.open_mta_perspective()
    codereadystudio.run_simple_analysis()
    assert codereadystudio.is_analysis_complete()
