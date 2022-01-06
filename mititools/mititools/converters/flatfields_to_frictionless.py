
from ..name_manipulation import create_table_filename


def convert(fields_table, tables_table):
    provider= FlatToFDProvider(fields_table, tables_table)
    resources = [
        {
            'table_name' : table_record['Name'],
            'filename' : create_table_filename(table_record['Name']),
            'fields' : [
                {
                    'column_name' : field_record['Column name'],
                    'title' : field_record['Column label'],
                    'type_string' : field_record['Data type'],
                    'data_format' : field_record['Data format'],
                    'description' : field_record['Description'],
                }
                for index_field, field_record in provider.fields_of(table_record)
            ],
            'primary_key' : table_record['Primary key'],
            'foreign_keys' : [
                {
                    'source_column' : field_record['Column name'],
                    'target_table' : field_record['Foreign table'],
                    'target_column' : field_record['Foreign key'],
                }
                for index_field, field_record in provider.foreign_fields_of(table_record)
            ],
            'has_foreign_keys' : len([e for e in provider.foreign_fields_of(table_record)]) > 0,
        }
        for index_table, table_record in provider.tables()
    ]

    top_variables = {
        'data_package_name' : 'data-package-name',
        'globally_unique_data_package_identifier' : 'globally unique data package identifier',
        'data_package_title' : 'data package title',
        'resources' : resources,
    }

    return top_variables


class FlatToFDProvider:
    def __init__(self, fields_table, tables_table):
        self.fields_table = fields_table
        self.tables_table = tables_table

    def fields_of(self, table_record):
        df = self.fields_table
        condition = (df['Table'] == table_record['Name'])
        return df[condition].iterrows()

    def foreign_fields_of(self, table_record):
        df = self.fields_table
        condition = (df['Table'] == table_record['Name']) & (df['Foreign key'] != '')
        return df[condition].iterrows()

    def tables(self):
        return self.tables_table.iterrows()
