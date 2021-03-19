def pytest_sessionfinish(session, exitstatus):
    if exitstatus == 5:
        session.exitstatus = 10 # Any arbitrary custom status you want to return```