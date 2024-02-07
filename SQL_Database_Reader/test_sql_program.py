"""This file tests sql_program.py using pytest.

Run "pytest -vv" in the current directory to run these tests.

Run "coverage run -m pytest test_sql_program.py" and "coverage report" to display coverage.

pytest:      31 passed in 0.xx seconds
coverage:    100% coverage
"""
import os
import sqlite3
from urllib.request import pathname2url
import pytest
import sql_program

TABLES_LIST_TEST = ['Regions', 'Territories', 'Suppliers', 'sqlite_sequence','Categories',
                    'Products', 'Employees','Customers', 'Orders','OrderDetails', 
                    'InternationalOrders', 'EmployeesTerritories']
ROWS = [[1, 'Eastern'], [2, 'Western'], [3, 'Northern']]
FIELD_NAMES = ["RegionID", "RegionDescription"]
DATABASE = "database.db"


def create_table_queries():
    tables_list = ['Regions', 'EmployeesTerritories', "Categories"]
    
    for table in tables_list:
        sql = f"DROP TABLE IF EXISTS {table};"
        execute_sql(sql, False)

    sql = """        
        CREATE TABLE Regions(
            RegionID INT PRIMARY KEY NOT NULL,
            RegionDescription TEXT NOT NULL
        );
        """
    execute_sql(sql, False)

    sql = """
        CREATE TABLE Categories(
            CategoryID INT PRIMARY KEY NOT NULL,
            CategoryName TEXT NOT NULL,
            Description TEXT NOT NULL
        );
        """
    execute_sql(sql, False)

    sql = """
        CREATE TABLE EmployeesTerritories(
            EmployeeID INT PRIMARY KEY NOT NULL,
            TerritoryID INT NOT NULL
        );
        """
    execute_sql(sql, False)


def insert_queries():
    sql = "INSERT INTO Regions(RegionID, RegionDescription) VALUES(1, 'Eastern');"
    execute_sql(sql, False)

    sql = "INSERT INTO Regions(RegionID, RegionDescription) VALUES(2, 'Western');"
    execute_sql(sql, False)

    sql = "INSERT INTO Regions(RegionID, RegionDescription) VALUES(3, 'Northern');"
    execute_sql(sql, False)


def execute_sql(sql, fetch):
    """Executes the given sql statement.

    Args:
        sql (string): A valid SQL statement to execute.

    Returns:
        None.

    """
    try:
        connection = sqlite3.connect(DATABASE)
    except:  # pragma: no cover
        print(f"Unable to connect to {DATABASE}")
        raise

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        if fetch is True:  # pragma
            sql_results = cursor.fetchall()
            return sql_results
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
    connection2 = sqlite3.connect(DATABASE)
    connection2.close()

    with pytest.raises(AssertionError):
        sql_program.get_tables(DATABASE)

    os.remove(DATABASE)


def test_get_tables_return_correct_tables():

    create_table_queries()

    tables = sql_program.get_tables(DATABASE)
    assert tables == ['Regions', 'Categories', 'EmployeesTerritories']

    os.remove(DATABASE)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=GET CHOICE=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


def test_get_choice_returns_valid_input():
    input_values = [1]

    def input():
        return input_values.pop(0)

    sql_program.input = input
    assert sql_program.get_choice(TABLES_LIST_TEST, ' ') == 1


def test_get_choice_returns_ignores_invalid_input():
    input_values = ['foo', 2.9]

    def input():
        return input_values.pop(0)

    sql_program.input = input
    assert sql_program.get_choice(TABLES_LIST_TEST, ' ') == 2


def test_get_choice_rejects_outside_parameters():
    input_values = [0, 13, 3]

    def input(prompt=None):
        return input_values.pop(0)

    sql_program.input = input
    assert sql_program.get_choice(TABLES_LIST_TEST, ' ') == 3


def test_get_choice_return_none():
    input_values = [""]

    def input(prompt=None):
        return input_values.pop(0)

    sql_program.input = input
    assert sql_program.get_choice(TABLES_LIST_TEST, ' ') is None

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=GET TABLE DATA=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def test_get_table_data_returns_correct_data():
    create_table_queries()
    insert_queries()

    data = sql_program.get_table_data('Regions', DATABASE)
    assert data == [FIELD_NAMES, [(1, 'Eastern'), (2, 'Western'), (3, 'Northern')]]


def test_get_table_data_raises_with_invalid_db():
    with pytest.raises(Exception):
        sql_program.get_table_data("Regions", "invalid_name")


def test_get_table_data_raises_with_invalid_table_name():
    with pytest.raises(Exception):
        sql_program.get_table_data("invalid_name", DATABASE)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=DISPLAY TABLE=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def test_display_table_displays_correct_table(capsys):
    create_table_queries()
    insert_queries()

    sql_program.display_table("Regions", ROWS, FIELD_NAMES)
    captured = capsys.readouterr()
    assert captured.out == ('\nTable: Regions\n\nRow # |   RegionID     RegionDescription     \n\n1'
                            '     |   1            Eastern               \n2     '
                            '|   2            Western               \n3     |   3            '
                            'Northern              \n\n\n')

    os.remove(DATABASE)


def test_display_table_raises_with_empty_rows():
    with pytest.raises(AssertionError):
        sql_program.display_table("Regions", [], FIELD_NAMES)


def test_display_table_raises_with_empty_field_names():
    with pytest.raises(AssertionError):
        sql_program.display_table("Regions", ROWS, [])


def test_display_table_raises_with_invalid_rows():
    with pytest.raises(Exception):
        sql_program.display_table("Regions", None, FIELD_NAMES)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=MAX LENGTH=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def test_max_length_raises_with_empty_list():
    with pytest.raises(AssertionError):
        sql_program.calculate_max_length([], None)


def test_max_length_returns_correct_value():
    assert sql_program.calculate_max_length(['1', 'Eastern'], None) == [1, 7]


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=FORMAT ROW=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def test_format_row_returns_correct_info():
    formatted_row = sql_program.format_row(['1', 'Eastern'], [8, 17])
    assert formatted_row == '1            Eastern               '


def test_format_row_raises_with_empty_row_list():
    with pytest.raises(AssertionError):
        sql_program.format_row([], [8, 17])


def test_format_row_raises_with_empty_max_legnth_list():
    with pytest.raises(IndexError):
        sql_program.format_row(['1', 'Eastern'], [])

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=EXECUTE SQL=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


def test_execute_sql_properly_executes_sql():
    create_table_queries()

    sql = """INSERT INTO Regions("RegionID", "RegionDescription") VALUES(?,?);"""
    sql_program.execute_sql(sql, DATABASE, [1, 'Eastern'])

    sql = "SELECT * FROM Regions;"
    sql_results = execute_sql(sql, True)
    assert sql_results == [(1, 'Eastern')]

    os.remove(DATABASE)


def test_execute_sql_raises_exception_with_bad_sql(capsys):
    create_table_queries()
    sql = "invalid_sql"
    sql_program.execute_sql(sql, DATABASE, None)

    captured = capsys.readouterr()
    assert captured.out == ('Unable to execute: invalid_sql\nDue to: near '
                            '"invalid_sql": syntax error\n\n')


def test_execute_raises_with_invalid_db():
    with pytest.raises(Exception):
        sql_program.execute_sql("", "invalid_db", None)
    

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=INSERT RECORD=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


def test_insert_record_correctly_inserts():

    try:
        create_table_queries()

        input_values = ["1", "Eastern", "y",]

        def input():
            return input_values.pop(0)

        sql_program.input = input
        sql_program.insert_record(
            "Regions", ["RegionID", "RegionDescription"], DATABASE)

        sql = "SELECT * FROM Regions;"
        sql_results = execute_sql(sql, True)
        assert sql_results == [(1, 'Eastern')]
    finally:
        os.remove(DATABASE)


def test_insert_record_raises_assertion_with_no_fields():
    with pytest.raises(AssertionError):
        sql_program.insert_record("Regions", [], "database.db")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=UPDATE RECORD=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def test_update_record_raises_with_empty_rows():
    with pytest.raises(AssertionError):
        sql_program.update_record(DATABASE, "Regions", FIELD_NAMES, [])


def test_update_record_raises_with_empty_field_names():
    with pytest.raises(AssertionError):
        sql_program.update_record(DATABASE, "Regions", [], ROWS)


def test_update_record_correctly_updates():
    try:
        create_table_queries()
        insert_queries()

        input_values = ["2", "1", "Timbuktu", "y",]

        def input():
            return input_values.pop(0)

        sql_program.input = input
        sql_program.update_record(DATABASE, "Regions", FIELD_NAMES, ROWS)

        sql = "SELECT * FROM Regions;"
        sql_results = execute_sql(sql, True)
        assert sql_results == [(1, 'Timbuktu'), (2, 'Western'), (3, 'Northern')]
    finally:
        os.remove(DATABASE)


def test_update_record_raises_with_empty_input():
    try:
        create_table_queries()
        insert_queries()

        input_values = ["1", ""]

        def input():
            return input_values.pop(0)

        sql_program.input = input

        with pytest.raises(Exception):
            sql_program.update_record(DATABASE, "Regions", FIELD_NAMES, ROWS)
    finally:
        os.remove(DATABASE)


def test_update_record_goes_back_with_enter(capsys):
    input_values = [""]

    def input():
        return input_values.pop(0)

    sql_program.input = input

    sql_program.update_record(DATABASE, "Regions", FIELD_NAMES, ROWS)
    captured = capsys.readouterr()
    assert captured.out == ("Which field from 'Regions' do you want to update? Press <Enter> "
                            'to go back.\n(1) RegionID\n(2) RegionDescription\nGoing back...\n\n')


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=DELETE RECORD=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def test_delete_record_successful_delete():
    try:
        create_table_queries()
        insert_queries()

        input_values = ["1", "y"]

        def input():
            return input_values.pop(0)

        sql_program.input = input
        sql_program.delete_record(DATABASE, "Regions", FIELD_NAMES, ROWS)

        sql = "SELECT * FROM Regions;"
        sql_results = execute_sql(sql, True)
        assert sql_results == [(2, 'Western'), (3, 'Northern')]
    finally:
        os.remove(DATABASE)


def test_delete_record_goes_back_with_enter(capsys):
    input_values = [""]

    def input():
        return input_values.pop(0)

    sql_program.input = input

    sql_program.delete_record(DATABASE, "Regions", FIELD_NAMES, ROWS)
    captured = capsys.readouterr()
    assert captured.out == ("Which record from 'Regions' do you want to delete? Use row numbers. "
                            "Press <Enter> to go back.\n\nTable: Regions\n\nRow # |   RegionID     "
                            "RegionDescription     \n\n1     |   1          "
                            '  Eastern               \n2     |   2            Western               \n3     '
                            "|   3            Northern              \n\n\nRow number: \nGoing back...\n\n")
