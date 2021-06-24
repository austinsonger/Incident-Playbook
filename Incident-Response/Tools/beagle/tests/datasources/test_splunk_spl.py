import pytest
import mock
from beagle.datasources import SplunkSPLSearch


@mock.patch.object(SplunkSPLSearch, "setup_session")
def test_init(mock_method):
    SplunkSPLSearch(spl="search index=main | head 10")
    assert mock_method.called


@pytest.mark.parametrize(
    "spl,expected",
    [
        ("index=main | head 10", "search index=main | head 10"),
        ("search index=main | head 10", "search index=main | head 10"),
        ("|inputlookup foo.csv", "|inputlookup foo.csv"),
    ],
)
@mock.patch.object(SplunkSPLSearch, "setup_session")
def test_forces_search_appended(mock_method, spl, expected):
    op = SplunkSPLSearch(spl=spl)
    assert op.spl == expected


@mock.patch.object(SplunkSPLSearch, "setup_session")
@mock.patch.object(SplunkSPLSearch, "create_search")
@mock.patch.object(SplunkSPLSearch, "get_results")
def test_get_events(get_results_mock, create_search_mock, mock_session):

    op = SplunkSPLSearch(spl="index=main")

    create_search_mock.return_value = mock.MagicMock()
    create_search_mock.return_value.sid = "foo"
    create_search_mock.is_done.return_value = True

    get_results_mock.return_value = [{"foo": "bar"}]
    assert list(op.events()) == [{"foo": "bar"}]
    assert get_results_mock.called
