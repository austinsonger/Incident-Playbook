# -*- coding: utf-8 -*-
# Copyright 2017-2019 ControlScan, Inc.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Cyphon Engine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cyphon Engine. If not, see <http://www.gnu.org/licenses/>.

# standard library
import re

# local
from bottler.bottles.models import BottleField
from bottler.labels.models import LabelField
from cyphon.fieldsets import QueryFieldset
from .search_parameter import SearchParameter, SearchParameterType


class FieldTypes(object):
    """DataField field_Types written as constants."""

    BOOLEAN = 'BooleanField'
    CHAR = 'CharField'
    CHOICE = 'ChoiceField'
    DATE_TIME = 'DateTimeField'
    EMAIL = 'EmailField'
    FILE = 'FileField'
    FLOAT = 'FloatField'
    INT = 'IntegerField'
    IP_ADDR = 'GenericIPAddressField'
    LIST = 'ListField'
    POINT = 'PointField'
    TEXT = 'TextField'
    URL = 'URLField'
    EMBEDDED = 'EmbeddedDocument'


class FieldValueParsingError(Exception):
    """Custom error thrown when there's a problem parsing the field value."""

    pass


class FieldValueParsers(object):
    """Parse a field value.

    Collection of functions used to parse the field search value
    from a FieldSearchParameter.
    """

    BOOLEAN_CHOICES = ['true', 'false']
    """list of str

    Possible string values someone can use to represent a boolean value.
    """

    INVALID_BOOLEAN_CHOICE = (
        'Boolean field value must either be `true` or `false`.'
    )
    """str

    Error message explaining that the given string is not a valid
    boolean representation.
    """

    INVALID_INTEGER_VALUE = 'Could not parse integer from value `{}`'
    """str

    Error message explaining that the given string could not parse an
    integer value.
    """

    INVALID_FLOAT_VALUE = 'Could not parse float from value `{}`.'
    """str

    Error message explaining that the given string could not parse
    a float value.
    """

    @staticmethod
    def boolean_parser(value):
        """Parse a boolean string value.

        Parameters
        ----------
        value : str

        Returns
        -------
        bool

        Raises
        ------
        FieldValueParsingError
            If a string value other than true or false is used.
        """
        lowercased_value = value.lower()

        if lowercased_value not in FieldValueParsers.BOOLEAN_CHOICES:
            raise FieldValueParsingError(
                FieldValueParsers.INVALID_BOOLEAN_CHOICE
            )

        return (
            True if lowercased_value == FieldValueParsers.BOOLEAN_CHOICES[0]
            else False
        )

    @staticmethod
    def text_parser(value):
        """Parse a text value by stripping any quotation marks.

        Parameters
        ----------
        value : str
            String value to parse.

        Returns
        -------
        str
        """
        return value.strip('"')

    @staticmethod
    def int_parser(value):
        """Parse an integer value from a string.

        Parameters
        ----------
        value : str

        Returns
        -------
        int

        Raises
        ------
        FieldValueParsingError
            If the integer could not be parsed from the string.

        """
        try:
            return int(value)
        except ValueError:
            raise FieldValueParsingError(
                FieldValueParsers.INVALID_INTEGER_VALUE.format(value)
            )

    @staticmethod
    def float_parser(value):
        """Parse a float value from a string.

        Parameters
        ----------
        value : str

        Returns
        -------
        float

        Raises
        ------
        FieldValueParsingError
            If the float could not be parsed from the string.

        """
        try:
            return float(value)
        except ValueError:
            raise FieldValueParsingError(
                FieldValueParsers.INVALID_FLOAT_VALUE.format(value)
            )


class FieldValue(object):
    """Handle parsing the value of a FieldSearchParameter.

    Attributes
    ----------
    value : str
        Parsed string representation of the FieldSearchParameter value.

    errors : list of str
        Errors that occurred during parsing.

    parsed_value : any
        Parsed value from the string representation.

    """

    PARSERS = dict([
        (FieldTypes.BOOLEAN, FieldValueParsers.boolean_parser),
        (FieldTypes.CHAR, FieldValueParsers.text_parser),
        (FieldTypes.CHOICE, None),
        (FieldTypes.DATE_TIME, FieldValueParsers.text_parser),
        (FieldTypes.EMAIL, FieldValueParsers.text_parser),
        (FieldTypes.FILE, None),
        (FieldTypes.FLOAT, FieldValueParsers.float_parser),
        (FieldTypes.INT, FieldValueParsers.int_parser),
        (FieldTypes.IP_ADDR, FieldValueParsers.text_parser),
        (FieldTypes.LIST, None),
        (FieldTypes.POINT, None),
        (FieldTypes.TEXT, FieldValueParsers.text_parser),
        (FieldTypes.URL, FieldValueParsers.text_parser),
        (FieldTypes.EMBEDDED, None),
    ])
    """str of func

    Field types mapped to the function responsible for parsing the value.
    """

    INVALID_FIELD_TYPE = '`{}` is an invalid field type.'
    """str

    Error message explaining that the given field type isn't valid.
    """

    MISSING_PARSER = 'There is no parser for field types of `{}`.'
    """str

    Error message explaining that there is no parser for the given field_type.
    """

    EMPTY_VALUE = 'Field value is an empty string.'
    """str

    Error message explaining that the given value is empty.
    """

    def __init__(self, value, field_type):
        """Initialize a FieldValue object.

        Parameters
        ----------
        value : str
            Value to parse.

        field_type : str
            The known field type of this value.

        """
        self.value = value
        self.errors = []

        try:
            parser = FieldValue.PARSERS[field_type]
        except KeyError:
            self.errors.append(FieldValue.INVALID_FIELD_TYPE.format(field_type))
            return

        if parser is None:
            self.errors.append(FieldValue.MISSING_PARSER.format(field_type))
            return

        if not value:
            self.errors.append(FieldValue.EMPTY_VALUE)
            return

        try:
            self.parsed_value = parser(value)
        except FieldValueParsingError as error:
            self.errors.append(str(error))


class FieldOperator(object):
    """Class representation of how to compare the value on the field.

    Attributes
    ----------
    errors : list of str
        List of errors that occurred when parsing the operator.

    operator : str
        Operator string from the field search parameter.

    fieldset_operator : str
        The QueryFieldset operator equivalent to the given operator string.

    """

    EQUALS = '='
    """str

    String indicating that the field should equal the given value.
    """

    GREATER_THAN = '>'
    """str

    String indicating that the field should be greater than the given value.
    """

    LESS_THAN = '<'
    """str

    String indicating that the field should be less than the given value.
    """

    GREATER_THAN_OR_EQUAL = '>='
    """str

    String indicating that the field should be greater than or equal
    to the given value.
    """

    LESS_THAN_OR_EQUAL = '<='
    """str

    String indicating that the field should be less than or equal to the
    given value.
    """
    NOT_EQUAL = '!='
    """str

    String indicating that the field should not equal the given value.
    """

    ALL = [
        EQUALS,
        GREATER_THAN,
        LESS_THAN,
        GREATER_THAN_OR_EQUAL,
        LESS_THAN_OR_EQUAL,
        NOT_EQUAL,
    ]
    """list of str

    List of all the possible field operator strings.
    """

    BOOLEAN_OPERATORS = dict([(EQUALS, 'eq')])
    """dict of str

    Dictionary mapping of the the possible operator strings for
    boolean type values and their QueryFieldset operators.
    """

    TEXT_OPERATORS = dict([(EQUALS, 'regex')])
    """dict of str

    Dictionary mapping of the the possible operator strings for
    text type values and their QueryFieldset operators.
    """

    DATE_OPERATORS = dict([
        (GREATER_THAN, 'gt'),
        (LESS_THAN, 'lt'),
        (GREATER_THAN_OR_EQUAL, 'gte'),
        (LESS_THAN_OR_EQUAL, 'lte'),
    ])
    """dict of str

    Dictionary mapping of the the possible operator strings for
    date type values and their QueryFieldset operators.
    """

    NUMBER_OPERATORS = dict([
        (EQUALS, 'eq'),
        (GREATER_THAN, 'gt'),
        (LESS_THAN, 'lt'),
        (GREATER_THAN_OR_EQUAL, 'gte'),
        (LESS_THAN_OR_EQUAL, 'lte'),
        (NOT_EQUAL, 'not:eq'),
    ])
    """dict of str

    Dictionary mapping of the the possible operator strings for
    number type values and their QueryFieldset operators.
    """

    FIELD_TYPES_TO_OPERATORS = dict([
        (FieldTypes.BOOLEAN, BOOLEAN_OPERATORS),
        (FieldTypes.CHAR, TEXT_OPERATORS),
        (FieldTypes.CHOICE, None),
        (FieldTypes.DATE_TIME, DATE_OPERATORS),
        (FieldTypes.EMAIL, TEXT_OPERATORS),
        (FieldTypes.FILE, None),
        (FieldTypes.FLOAT, NUMBER_OPERATORS),
        (FieldTypes.INT, NUMBER_OPERATORS),
        (FieldTypes.IP_ADDR, TEXT_OPERATORS),
        (FieldTypes.LIST, None),
        (FieldTypes.POINT, None),
        (FieldTypes.TEXT, TEXT_OPERATORS),
        (FieldTypes.URL, TEXT_OPERATORS),
        (FieldTypes.EMBEDDED, None),
    ])
    """dict of dict

    Mapping of field types to their possible operators and their
    QueryFieldset equivalent.
    """

    NO_FIELD_MAPPING = (
        'There is no field operator mapping for fields of type `{}.`'
    )
    """str

    Error message explaining that there is no field operator mapping
    for a particular field type.
    """

    MISMATCHED_OPERATOR = (
        'The operator `{}` is not used for fields of type `{}`'
    )
    """str

    Error message explaining that given operator string has no
    QueryFieldset operator equivalent for the particular field type.
    """

    def __init__(self, operator, field_type):
        """Initialize a FieldOperator object."""
        self.errors = []
        self.operator = operator
        field_mapping = FieldOperator._get_operator_map(field_type)

        if not field_mapping:
            self.errors.append(
                FieldOperator.NO_FIELD_MAPPING.format(field_type)
            )
            return

        self.fieldset_operator = FieldOperator._get_fieldset_operator(
            field_mapping,
            operator,
        )

        if not self.fieldset_operator:
            self.errors.append(
                FieldOperator.MISMATCHED_OPERATOR.format(operator, field_type)
            )

    @staticmethod
    def _get_operator_map(field_type):
        """Return the QueryFieldset operator map for a certain field_type.

        Parameters
        ----------
        field_type : str

        Returns
        -------
        dict of str or None
        """
        try:
            return FieldOperator.FIELD_TYPES_TO_OPERATORS[field_type]
        except KeyError:
            return None

    @staticmethod
    def _get_fieldset_operator(operator_map, operator):
        """Return the matching QueryFieldset operator from an operator mapping.

        Parameters
        ----------
        operator_map : dict of str

        operator : str

        Returns
        -------
        str or None

        """
        try:
            return operator_map[operator]
        except KeyError:
            return None


class FieldSearchParameter(SearchParameter):
    """Parameter for searching values for s particular field.

    Attributes
    ----------
    field_name : str
        Name of the field to compare values against.

    data_field : DataField or None
        DataField matching the given field_name. If one isn't found, this
        is None.

    operator : FieldOperator or None
        Class used to map the query operator value to a QueryFieldset operator.
        This is None if a data_field cannot be found.

    value : FieldValue
        Class used to parse the string value to compare against into a
        value for a QueryFieldset.

    combined_errors : list of str
        The combined errors of the parameter, operator, and value. If the
        date_field cannot be found, this will only return the parameter errors.

    """

    FIELD_REGEX = re.compile(
        r'(?P<field_name>^\w[\w.]*)'  # Name of the field
        r'(?P<operator>[=<>!]{1,2})'  # Operator to compare value with
        r'(?P<value>$|\".*\"$|[\w.]*$)'  # Value to match on the field
    )
    """RegExp

    Regex object used to parse the field search properties from the
    parameter string.
    """

    FIELD_DOES_NOT_EXIST = 'Field `{}` does not exist.'
    """str

    Error message explaining that the requested field to be searched does
    not exist.
    """

    INVALID_PARAMETER = 'Could not parse parameter into field properties.'
    """str

    Error message explaining that the given parameter could not be parsed
    by the regex object.
    """

    EMPTY_VALUE = 'Value is empty.'
    """str

    Error message explaining that the value to compare against is empty.
    """

    CANNOT_CREATE_FIELDSET = (
        'Cannot create a QueryFieldset from an invalid FieldSearchParameter.'
    )

    CANNOT_CHECK_DISTILLERY = (
        'Cannot check if the parameter is related to a distillery if the '
        'parameter is invalid.'
    )

    def __init__(self, index, parameter):
        """Parse the parameter string into a FieldSearchParameter.

        Parameters
        ----------
        index: int
            Index of the parameter in the query string.

        parameter : str
            String representation of a field search parameter.

        """
        super(FieldSearchParameter, self).__init__(
            index,
            parameter,
            SearchParameterType.FIELD,
        )
        parsed_parameter = FieldSearchParameter.FIELD_REGEX.search(parameter)

        self.field_name = ''
        self.data_field = None
        self.operator = None
        self.value = None

        if not parsed_parameter:
            self._add_error(FieldSearchParameter.INVALID_PARAMETER)
            return

        self.field_name, operator, value = parsed_parameter.groups()
        self.data_field = FieldSearchParameter._get_data_field(self.field_name)

        if not self.data_field:
            self._add_error(
                FieldSearchParameter.FIELD_DOES_NOT_EXIST.format(
                    self.field_name,
                ),
            )
            return

        self.operator = FieldOperator(operator, self.data_field.field_type)
        self.value = FieldValue(value, self.data_field.field_type)

    @staticmethod
    def _get_bottle_field(field_name, bottle_field_queryset):
        """Return the BottleField with the given field name.

        Parameters
        ----------
        field_name : str
            Name of the BottleField to look for.

        Returns
        -------
            BottleField or None.

        """
        nested_fields = field_name.split('.')

        try:
            bottle_field = bottle_field_queryset.get(
                field_name__exact=nested_fields[0])

            if bottle_field.embedded_doc:
                return FieldSearchParameter._get_bottle_field(
                    '.'.join(nested_fields[1:]),
                    bottle_field.embedded_doc.fields)

            return bottle_field
        except BottleField.DoesNotExist:
            return None

    @staticmethod
    def _get_label_field(field_name):
        """Return the label field with the given field name.

        Parameters
        ----------
        field_name : str
            Name of the label field to look for.

        Returns
        -------
            LabelField or None

        """
        try:
            return LabelField.objects.get(field_name__exact=field_name)
        except LabelField.DoesNotExist:
            return None

    @staticmethod
    def _get_data_field(field_name):
        """Return the data field object associated with the field_name.

        Parameters
        ----------
        field_name : str
            Field name to compare values against.

        Returns
        -------
        BottleField or LabelField or None
            The associated bottle/label field or None if the field
            doesn't exist.
        """
        return (
            FieldSearchParameter._get_bottle_field(
                field_name, BottleField.objects.all())
            or
            FieldSearchParameter._get_label_field(field_name))

    @property
    def combined_errors(self):
        """Return the combined errors of the parameter, operator, and value.

        This will only combine the errors if a matching data_field object
        was found.

        Returns
        -------
        list of str

        """
        if self.data_field:
            return self.errors + self.value.errors + self.operator.errors

        return self.errors

    def is_valid(self):
        """Determine if the field is valid.

        Returns
        -------
        bool

        """
        return not bool(self.combined_errors)

    def as_dict(self):
        """Return a JSON serializable representation of this object.

        Returns
        -------
        dict

        """
        info = super(FieldSearchParameter, self).as_dict()

        info.update({
            'field_name': self.field_name,
            'operator': self.operator.operator if self.operator else None,
            'value': self.value.value if self.value else None,
            'errors': self.combined_errors,
        })

        return info

    def is_related_to_distillery(self, distillery):
        """Determine if a distillery contains the data_field of this parameter.

        Parameters
        ----------
        distillery : Distillery
            Distillery to look for the DataField on.

        Returns
        -------
        bool

        """
        if not self.data_field:
            return False

        bottle_fields = distillery.container.bottle.fields

        if bottle_fields.filter(field_name=self.field_name).exists():
            return True

        if not distillery.container.label:
            return False

        label_fields = distillery.container.label.fields

        return label_fields.filter(field_name=self.field_name).exists()

    def create_fieldset(self):
        """Create a QueryFieldset from this parameter and a distillery.

        Returns
        -------
        QueryFieldset

        Raises
        ------
        AssertionError
            If the FieldSearchParameter is not valid.

        """
        if not self.is_valid():
            raise ValueError(FieldSearchParameter.CANNOT_CREATE_FIELDSET)

        return QueryFieldset(
            self.field_name,
            self.data_field.field_type,
            self.operator.fieldset_operator,
            self.value.parsed_value,
        )
