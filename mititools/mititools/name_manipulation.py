import re


def create_table_filename(table_name):
    """
    Args:
        table_name: A name for a table which is part of a MITI data bundle.
    Returns:
        A conventional filename for a tabular file which containing the table's
        data.
    """
    return table_name + '.tsv'


def create_auxiliary_table_filename(table_name):
    """
    Args:
        table_name: A name for an auxiliary table which is part of a MITI data
        bundle.
    Returns:
        A conventional filename for a tabular file which containing the table's
        data.
    """
    return table_name + '.tsv'


def create_auxiliary_table_name(field_name, table_name):
    """
    Args:
        field_name: A table field whose value identifies a record in a foreign
        table.
        table_name: The table containing the field field_name.
    Returns:
        A conventional name for the foreign table. Some whitespace and
        special-character stripping is enforced.
    """
    if not re.search('^' + table_name, field_name):
        composite = table_name + ' ' + field_name
    else:
        composite = field_name
    return re.sub('[\s\-\_]+', '_', composite).lower()


def create_human_readable_label(text_name):
    """
    Args:
        text_name: An unstructured/free-text name for a table field.
    Returns:
        A human readable label adhering to a naming convention which is basically
        space-separated words and prohibition of certain characters. A space is
        inserted before capital letters in some situations, as exemplified in
        "FOVSizeX" becoming "FOV Size X".
    """
    label = text_name
    label = re.sub('[\s\-\_]+', ' ', label)
    label = re.sub('(?<=[a-z0-9])([A-Z])', ' \\1', label)
    return label


def create_machine_readable_token(text_name):
    """
    Args:
        text_name: An unstructured/free-text name for a table field.
    Returns:
        A conventional token which is machine-readable across many language
        environments. The result is essentially lower snakecase.
    """
    label = create_human_readable_label(text_name)
    token = label
    token = re.sub('[\/\:\(\)]', '', token)
    token = re.sub('\#', 'number', token)
    token = re.sub('[\s\-\_]+', '_', token)
    return token.lower()


def check_has_patterns(patterns, string):
    """
    Args:
        patterns: A list of regex patterns
        string: Input to check.
    Returns:
        Whether or not the string matches any of the patterns.
    """
    return any([re.search(pattern, string) for pattern in patterns])


def extract_table_name(table_filename):
    """
    Args:
        table_filename: A table filename possibly containing information in
        addition to a table name.
    Returns:
        A guessed extracted table name obtained by stripping instances of certain
        patterns from the beginning and end of the filename (e.g. whitespace,
        numbers). Generally conforms to lower snakecase.
    """
    string = table_filename
    left_strip_patterns = ['^ +', '^[\d]+\-?', '^[\-\_]+']
    right_strip_patterns = [' +$', '\.yaml$', '\.tsv', '[\-\_]+$']
    while check_has_patterns(left_strip_patterns, string):
        for pattern in left_strip_patterns:
            string = re.sub(pattern, '', string)
    while check_has_patterns(right_strip_patterns, string):
        for pattern in right_strip_patterns:
            string = re.sub(pattern, '', string)
    string = re.sub('[\s\_\-]+', '_', string)
    return string.lower()
