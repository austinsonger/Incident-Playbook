from beagle.nodes import Alert, Domain


def test_create_alert():

    alert = Alert(alert_name="foo", alert_data={"time": "foo"})
    assert alert.alert_name == "foo"
    assert alert.alert_data == {"time": "foo"}


def test_alerted_on():
    alert = Alert(alert_name="foo", alert_data={"time": "foo"})

    dom = Domain("foobar.com")

    alert.alerted_on[dom].append(timestamp=1234)

    assert {"timestamp": 1234} in alert.alerted_on[dom]

