from beagle.web.api.models import Graph


def test_make_graph(session):
    g = Graph(
        sha256="1234",
        meta={"foo": "bar"},
        category="test_cat",
        comment="foo",
        file_path="foo_Bar_/",
    )
    session.add(g)
    session.commit()

    assert g.id > 0

