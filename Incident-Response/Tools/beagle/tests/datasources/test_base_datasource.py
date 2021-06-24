import pytest
from beagle.datasources.base_datasource import DataSource
from beagle.transformers.base_transformer import Transformer


def test_subclass_no_name():

    with pytest.raises(RuntimeError):

        class MyDataSource(DataSource):
            transformers = []

            def __init__(*args, **kwargs):
                super()

            def metadata(self):
                return {}

            def events(self):
                yield {}

    # With name, no error
    class OtherDataSource(DataSource):
        name = "OtherDataSource"
        category = "foo"
        transformers = []

        def __init__(*args, **kwargs):
            super()

        def metadata(self):
            return {}

        def events(self):
            yield {}

    assert OtherDataSource.name == "OtherDataSource"


def test_subclass_no_transformers():

    with pytest.raises(RuntimeError):

        class MyDataSource(DataSource):
            name = "1234"

            def __init__(*args, **kwargs):
                super()

            def metadata(self):
                return {}

            def events(self):
                yield {}

    with pytest.raises(RuntimeError):

        class MyOtherDataSource(DataSource):
            transformers = "1234"
            name = "foo"
            category = "bar"

            def __init__(*args, **kwargs):
                super()

            def metadata(self):
                return {}

            def events(self):
                yield {}

    # With name, no error
    class OtherDataSource(DataSource):
        name = "OtherDataSource"
        transformers = []
        category = "foo"

        def __init__(*args, **kwargs):
            super()

        def metadata(self):
            return {}

        def events(self):
            yield {}

    assert OtherDataSource.name == "OtherDataSource"


def test_transformer():
    class SomeTransformer(Transformer):
        def transform():
            return []

    # With name, no error
    class OtherDataSource(DataSource):
        name = "OtherDataSource"
        transformers = [SomeTransformer]
        category = "foo"

        def metadata(self):
            return {}

        def events(self):
            return []

    assert isinstance(OtherDataSource().to_transformer(), SomeTransformer)
