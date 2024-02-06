"""This file tests sql_program.py using pytest.

Run "pytest -vv" in the current directory to run these tests.

Run "coverage run -m pytest test_sql_program.py" and "coverage report" to display coverage.

pytest:      15 passed in 0.xx seconds
coverage:    100% coverage
"""
import os
import sqlite3
import pytest
import sql_program

tables_list_test = [('Regions',), ('Territories',), ('Suppliers',), ('sqlite_sequence',),
                    ('Categories',), ('Products',), ('Employees',
                                                     ), ('Customers',), ('Orders',),
                    ('OrderDetails',), ('InternationalOrders',), ('EmployeesTerritories',)]


def create_table_queries(database_name):
    sql = """
        CREATE TABLE Regions(
            RegionID INT PRIMARY KEY NOT NULL,
            RegionDescription TEXT NOT NULL
        );
        """
    execute_sql(sql, database_name)

    sql = """
        CREATE TABLE Categories(
            CategoryID INT PRIMARY KEY NOT NULL,
            CategoryName TEXT NOT NULL,
            Description TEXT NOT NULL
        );
        """
    execute_sql(sql, database_name)

    sql = """
        CREATE TABLE EmployeesTerritories(
            EmployeeID INT PRIMARY KEY NOT NULL,
            TerritoryID INT NOT NULL
        );
        """
    execute_sql(sql, database_name)


def insert_queries(database_name):
    sql = "INSERT INTO Regions(RegionID, RegionDescription) VALUES(1, 'Eastern');"
    execute_sql(sql, database_name)

    sql = "INSERT INTO Regions(RegionID, RegionDescription) VALUES(2, 'Western');"
    execute_sql(sql, database_name)

    sql = "INSERT INTO Regions(RegionID, RegionDescription) VALUES(3, 'Northern');"
    execute_sql(sql, database_name)


def execute_sql(sql, database_name):
    """Executes the given sql statement.

    Args:
        sql (string): A valid SQL statement to execute.

    Returns:
        None.

    """
    try:
        connection = sqlite3.connect(database_name)
    except:  # pragma: no cover
        print(f"Unable to connect to {database_name}")
        raise

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except Exception as exception:  # pragma: no cover
        print(f"Unable to execute {sql}")
        print(exception)
    finally:
        connection.close()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=GET TABLES=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def test_get_tables_raises_with_invalid_db():
    with pytest.raises(Exception):
        sql_program.get_tables("invalid_name")


def test_get_tables_raises_with_no_tables():
    database_name = "database.db"

    connection2 = sqlite3.connect(database_name)
    connection2.close()

    with pytest.raises(AssertionError):
        sql_program.get_tables(database_name)

    os.remove(database_name)


def test_get_database_name_return_correct_tables():
    database_name = "database.db"

    create_table_queries(database_name)

    tables = sql_program.get_tables(database_name)
    assert tables == [('Regions',), ('Categories',), ('EmployeesTerritories',)]

    os.remove(database_name)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=GET CHOICE=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


def test_get_choice_returns_valid_input():
    input_values = [1]

    def input():
        return input_values.pop(0)

    sql_program.input = input
    assert sql_program.get_choice(tables_list_test) == 'Regions'


def test_get_choice_returns_ignores_invalid_input():
    input_values = ['hi', 2.9]

    def input():
        return input_values.pop(0)

    sql_program.input = input
    assert sql_program.get_choice(tables_list_test) == 'Territories'


def test_get_choice_rejects_outside_parameters():
    input_values = [0, 13, 3]

    def input(prompt=None):
        return input_values.pop(0)

    sql_program.input = input
    assert sql_program.get_choice(tables_list_test) == 'Suppliers'


def test_get_choice_return_none():
    input_values = [""]

    def input(prompt=None):
        return input_values.pop(0)

    sql_program.input = input
    assert sql_program.get_choice(tables_list_test) is None


# # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=DISPLAY TABLE=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def test_display_table_displays_correct_table(capsys):
    database_name = "database.db"

    create_table_queries(database_name)
    insert_queries(database_name)

    sql_program.display_table("Regions", database_name)
    captured = capsys.readouterr()
    assert captured.out == ('\nTable: Regions\n\nRow # |  RegionID     RegionDescription     \n\n1'
                            '     |  1            Eastern               \n2     '
                            '|  2            Western               \n3     |  3            '
                            'Northern              \n\n')

    os.remove(database_name)


def test__raises_with_invalid_db():
    with pytest.raises(Exception):
        sql_program.display_table("Regions", "invalid_db")


def test__raises_with_invalid_table():
    database_name = "database.db"

    connection2 = sqlite3.connect(database_name)
    connection2.close()

    with pytest.raises(Exception):
        sql_program.display_table("invalid_table", database_name)

    os.remove(database_name)


# # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=MAX LENGTH=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def test_max_length_raises_with_empty_list():
    with pytest.raises(AssertionError):
        sql_program.calculate_max_length([], None)


def test_max_length_returns_correct_value():
    assert sql_program.calculate_max_length(['1', 'Eastern'], None) == [1, 7]


# # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=FORMAT ROW=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def test_format_row_returns_correct_info():
    formatted_row = sql_program.format_row(['1', 'Eastern'], [8, 17])
    assert formatted_row == '1            Eastern               '


def test_format_row_raises_with_empty_row_list():
    with pytest.raises(AssertionError):
        sql_program.format_row([], [8, 17])


def test_format_row_raises_with_empty_max_legnth_list():
    with pytest.raises(IndexError):
        sql_program.format_row(['1', 'Eastern'], [])
