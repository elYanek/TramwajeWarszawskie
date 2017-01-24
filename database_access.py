## -*- coding: utf-8 -*-
import psycopg2
import sys

#połączenie do bazy na VM na dellu. - testowe.



class DbConnection(object):
    """Class to manage database operations."""

    #tymczasowo wartości zahardkodowane
    host = ''
    port = ''
    db_name = ''
    user = ''
    password = ''

    def __init__(self):
        self.conn = psycopg2.connect(host=self.host,
                                     port=self.port,
                                     database=self.db_name,
                                     user=self.user,
                                     password=self.password)

        self.cur = self.conn.cursor()

    @staticmethod
    def __translate_time(value):
        """Function to translate time dependen on inserted value."""
        if value == 1:
            return "minute"
        else:
            return "minutes"

    def insert_point(self ,coord, SRID):
        """Create SQL querry to insert point to geometry column."""
        sql_insert = "SELECT ST_SetSRID(ST_MakePoint({0}, {1}),{2})"

        executed_sql = sql_insert.format(coord[0], coord[1], SRID)

        return executed_sql

    def show_table(self, table):
        """Show all table attributes."""

        #Base function SQL expression.
        sql_insert = "SELECT * FROM {0};"

        self.cur.execute(sql_insert.format(table))

        for c in self.cur:
            print(c)

    def add_value(self, table, *args):
        """Adding values to all columns in table.
            User should know fields and them order
            while he is inserting values.
        """
        #Base function SQL expression.
        sql_insert = "INSERT INTO {0} VALUES ({1});"

        values_list = []

        for arg in args:
            values_list.append(arg)

        values = ', '.join(values_list)

        executed_sql = sql_insert.format(table, values)

        print(executed_sql)
        self.cur.execute(executed_sql)

        #czy nie oddzielic?
        self.conn.commit()

    def add_values_from_dict(self, table, conv_dict):
        """Adding values to defined columns
        using dictionary on insert value."""

        sql_insert = "INSERT INTO {0} ({1}) VALUES ({2});"

        fields_list = []
        values_list = []

        for tram in conv_dict:
            fields_list.append(tram)
            values_list.append(conv_dict[tram])

        fields = ', '.join(fields_list)
        values = ', '.join(values_list)

        executed_sql = sql_insert.format(table, fields, values)

        #print(executed_sql)
        self.cur.execute(executed_sql)

        self.conn.commit()

    def clear_table(self, table):
        """Delete all values from table"""

        sql_insert = "DELETE FROM {0};"

        executed_sql = sql_insert.format(table)

        self.cur.execute(executed_sql)

        self.conn.commit()

    def clear_values_by_time(self, table, time_field, minutes):
        """Delete values if they are older then choosen interval."""

        sql_insert = "DELETE FROM {0} WHERE {0}.{1} < (now() - interval '{2} {3}');"

        executed_sql = sql_insert.format(table, time_field, minutes, self.__translate_time(minutes))

        self.cur.execute(executed_sql)

        self.conn.commit()

    def close_db_comminucation(self):
        """Close cursor and connection with database."""
        self.cur.close()
        self.conn.close()

    # funkcje na wyświetlanie/pobieranie schematów
    def get_columns(self, table_name):
        """Print column name and datatype (for this moment) for specyfic table."""
        sql_insert = "SELECT column_name, data_type " \
                     "FROM information_schema.columns " \
                     "WHERE table_name = '{0}'"

        executed_sql = sql_insert.format(table_name)

        self.cur.execute(executed_sql)

        for c in self.cur:
            print(c)
