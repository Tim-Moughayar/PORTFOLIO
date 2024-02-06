"""This program retrieves any requested tables from the Northwind database.

Instructions:
    Include the SQLite Northwind database in current directory.

    Script to create the SQLlite Northwind database: 
    https://en.wikiversity.org/wiki/Database_Examples/Northwind/SQLite

    Run program and enter an integer that corresponds with the desired table.
    
Output:
    The selected table's rows of data.
    
References:
    *https://en.wikiversity.org/wiki/Applied_Programming/databases/Python3_SQLite
    *https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-
    database-exists-in-python
"""
import sqlite3
import sys
from urllib.request import pathname2url


def get_tables(database):
    """Gets the names of tables in database.

    Args:
        database (str): database name

    Returns:
        list: Names of tables in database.

    """
    try:
        database_path = f'file:{pathname2url(database)}?mode=rw'
        connection = sqlite3.connect(database_path, uri=True)
    except:
        print(f"Unable to connect to {database}")
        raise

    sql = "SELECT name FROM sqlite_master WHERE type='table';"

    cursor = connection.cursor()

    cursor.execute(sql)
    connection.commit()
    tables_list = cursor.fetchall()
    connection.close()

    assert len(tables_list) > 0, "No tables in database"

    return tables_list


def get_choice(tables_list):
    """Displays table names and gets choice.

    Args:
        tables_list (list): table names from database

    Returns:
        single table name (str) or None

    """
    while True:
        try:
            assert len(tables_list) > 0, "No tables in table list"
            print("Enter a number to select table or press <Enter> to quit program:")
            for num, tablename in enumerate(tables_list):
                print(f"({num + 1}) {tablename[0]}")

            choice = input()
            choice = int(choice)
            table_selector = choice - 1

            if 1 <= choice <= len(tables_list):
                print()
                selected_table = tables_list[table_selector][0]
                return selected_table
            print(f"{choice} is not a valid choice.\n")

        except ValueError:
            if choice == "":
                return None
            print(f"ValueError: {choice} is not a valid choice.\n")

def display_table(selected_table, database):
    """Displays the chosen table.

    Args:
        selected_table (string): table chosen to get data from
        database (string): name of database

    Returns:
        None.

    """
    field_names = []

    try:
        database_path = f'file:{pathname2url(database)}?mode=rw'
        connection = sqlite3.connect(database_path, uri=True)
    except:
        print(f"Unable to connect to {database}")
        raise

    try:
        cursor = connection.cursor()

        sql = f"SELECT * FROM {selected_table};"
        cursor.execute(sql)

        field_metadata = cursor.description
        for field in field_metadata:
            field_names.append(field[0])

        rows = cursor.fetchall()

        max_length = calculate_max_length(field_names, None)

        for row in rows:
            max_length = calculate_max_length(row, max_length)

        print()
        print(f'Table: {selected_table}\n')
        formatted_row = format_row(field_names, max_length)
        print(f'Row # |  {formatted_row}\n')

        for num, row in enumerate(rows):
            formatted_row = format_row(row, max_length)
            print(f"{num + 1:<5} |  {formatted_row}")

        print()

    except Exception as exception:
        print(f"Error displaying tables.")
        print(exception)
        raise exception from exception
        
    finally:
        connection.close()


def calculate_max_length(data, max_length):
    """Caculates the char count of biggest string in given list.
    Args:
        data (list): multidimensional list containing rows of data.
        max_length (list): max length of previous list or None
    Returns:
        list: biggest items in list
    Raises:
        AssertionError: If list is empty
    """
    assert len(data) > 0, "List is empty."

    if max_length is None:
        max_length = []
        for iteration in data:
            max_length.append(0)

    for num, item in enumerate(data):
        if len(str(item)) > max_length[num]:
            max_length[num] = len(str(item))

    return max_length


def format_row(row, max_length):
    """Prints items from a list.
    Args:
        max_length (integer): Char count of biggest string in customers list.
        row (tuple): tuple that contains title and views.
    Returns:
        formatted_row (
    Raises:
        TypeError: If max_legnth list is empty.
        AssertionError: If row list is empty.
    """
    assert len(row) > 0, "List is empty."

    try:
        formatted_row = ''
        for num, column in enumerate(row):
            spaces = ' ' * (5 + max_length[num] - len(str(column)))
            new_row = f"{str(column)}{spaces}"
            formatted_row = f"{formatted_row}{new_row}"

        return formatted_row
    except IndexError as i_e:
        raise IndexError(
            f"Error printing output: {i_e}") from i_e
    

def main():  # pragma: no cover
    """Runs the main program logic."""

    database = ("Northwind.db")

    tables_list = get_tables(database)

    while True:
        selected_table = get_choice(tables_list)
        if selected_table is None:
            sys.exit("Exiting program...")

        display_table(selected_table, database)


if __name__ == "__main__":  # pragma: no cover
    main()
