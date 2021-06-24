import mock
from beagle.datasources import ElasticSearchQSSerach


@mock.patch.object(ElasticSearchQSSerach, "_setup_session")
def test_init(mock_method):
    ElasticSearchQSSerach(index="logs-*", query="*")
    assert mock_method.called


@mock.patch.object(ElasticSearchQSSerach, "_setup_session")
def test_event_loop(mock_setup):
    ds = ElasticSearchQSSerach(index="logs-*", query="powershell.exe")

    ds.client = mock.MagicMock()

    ds.client.search.return_value = {
        "_scroll_id": "1",
        "hits": {
            "hits": [
                {"_source": {"key": "foo"}, "_id": "bar"},
                {"_source": {"key": "bar"}, "_id": "baz"},
            ]
        },
    }

    ds.client.scroll.return_value = {"_scroll_id": "1", "hits": {"hits": []}}

    assert len(list(ds.events())) == 2


@mock.patch.object(ElasticSearchQSSerach, "_setup_session")
def test_scroll(mock_setup):
    ds = ElasticSearchQSSerach(index="logs-*", query="powershell.exe")

    ds.client = mock.MagicMock()

    ds.client.search.return_value = {
        "_scroll_id": "1",
        "hits": {
            "hits": [
                {"_source": {"key": "foo"}, "_id": "bar"},
                {"_source": {"key": "bar"}, "_id": "baz"},
            ]
        },
    }

    ds.client.scroll.side_effect = [
        {
            "_scroll_id": "2",
            "hits": {
                "hits": [
                    {"_source": {"key": "foo"}, "_id": "bar"},
                    {"_source": {"key": "bar"}, "_id": "baz"},
                ]
            },
        },
        {"_scroll_id": "3", "hits": {"hits": []}},
    ]

    assert len(list(ds.events())) == 4
