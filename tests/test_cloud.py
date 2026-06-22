from src.agents.runner import run_agent

def test_adk():
    out = run_agent('check posture', {'control_id': 'CIS-1.1'})
    assert out['trace']
