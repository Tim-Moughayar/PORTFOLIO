"""This program gets tables from the Northwind database and displays them. The user
can select one of the tables and it will display all the records for that table.
The user then has the option to insert, update, or delete a row in the database.

Instructions:
    Include Northwind.db in the current directory.

    Script to create the SQLlite Northwind database: 
    https://en.wikiversity.org/wiki/Database_Examples/Northwind/SQLite

    Run program and enter an integer that corresponds with the desired table
    
Output:
    The selected table's rows of data.
    
References:
    *https://en.wikiversity.org/wiki/Applied_Programming/databases/Python3_SQLite
    *https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-
    database-exists-in-python
    *https://betterprogramming.pub/stop-using-or-to-test-multiple-values-against-
    a-variable-in-python-abe0a77c287a

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
    tables_list = []

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
    raw_tables = cursor.fetchall()
    connection.close()

    assert len(raw_tables) > 0, "No tables in database"

    for table in raw_tables:
        tables_list.append(table[0])

    return tables_list


def get_choice(options, prompt):
    """Displays table names and gets choice.

    Args:
        options (list): list of tables from database
        prompt (str): prompt for choice

    Returns:
        table name (str) or None

    """
    while True:
        try:
            assert len(options) > 0, "No tables in table list"
            
            print(prompt)
            
            for num, option in enumerate(options):
                print(f"({num + 1}) {option}")

            choice = input()
            choice = int(choice)

            if 1 <= choice <= len(options):
                print()
                return choice
            print(f"{choice} is not a valid choice.\n")

        except ValueError:
            if choice == "":
                return None
            print(f"ValueError: {choice} is not a valid choice.\n")


def get_table_data(selected_table, database):
    field_names_and_rows = []
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

        field_names_and_rows.append(field_names)
        field_names_and_rows.append(rows)

    except Exception as exception:
        print("Error displaying tables.")
        print(exception)
        raise exception from exception
    finally:
        connection.close()

    return field_names_and_rows


def display_table(selected_table, rows, field_names):
    """Displays the chosen table.

    Args:
        selected_table (string): table chosen to get data from
        database (string): name of database

    Returns:
        None.

    """
    assert len(rows) > 0, "Error displaying table, rows list is empty."
    assert len(field_names) > 0, "Error displaying table, field names list is empty."

    try:
        space = ' ' * len(str(len(rows)))
        max_length = calculate_max_length(field_names, None)

        for row in rows:
            max_length = calculate_max_length(row, max_length)

        print()
        print(f'Table: {selected_table}\n')
        formatted_row = format_row(field_names, max_length)
        print(f'Row #{space}|   {formatted_row}\n')

        for num, row in enumerate(rows):
            formatted_row = format_row(row, max_length)
            print(f"{num + 1:<2}{space}   |   {formatted_row}")

        print("\n")

    except Exception as exception: # pragma: no cover
        print("Error displaying tables.")
        print(exception)
        raise exception from exception


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


def execute_sql(sql, database_name, values):
    """Executes the given sql statement.

    Args:
        sql (string): A valid SQL statement to execute.
        database_name (string): The name of the database
        values (list): a list of values or None 
        depending sql statement inserts into the database.

    Returns:
        None.

    """
    try:
        database_path = f'file:{pathname2url(database_name)}?mode=rw'
        connection = sqlite3.connect(database_path, uri=True)
    except:
        print(f"Unable to connect to {database_name}")
        raise

    try:
        cursor = connection.cursor()
        if values is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, values)
        connection.commit()
    except Exception as exception:
        print(f"Unable to execute: {sql}")
        print(f"Due to: {exception}")
        print()
    finally:
        connection.close()


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


def insert_record(selected_table, field_names, database_name):
    """Inserts data into the selected table.

    Args:
        selected_table (string): table name
        field_names (list): list of field names
        database_name (string): database name used to connect database

    Returns:
        None.

    """
    assert len(field_names) > 0, "Table has no fields."

    values = []

    print(f"Enter the values you want to insert into {selected_table}. ")

    while True:
        for name in field_names:
            print(f"{name}:")
            value = input()
            values.append(value)
            print()

        while True:
            print("Proceed with insert? y/n")
            for num, name in enumerate(field_names):
                print(f"{name}: {values[num]}", end=' ')
            print()
            proceed = input()
            if proceed in {'y', 'n'}:
                break
        break   # pragma: no cover

    if proceed == 'y':
        question_placeholders = len(field_names) * '?,'
        field_names_str = ', '.join(field_names)

        sql = (f"INSERT INTO {selected_table}({field_names_str})"
               f"VALUES({question_placeholders[:-1]});")
        execute_sql(sql, database_name, values)


def update_record(database_name, selected_table, field_names, rows):
    """Updates record in selected field and table.

    Args:
        selected_table (string): table name
        field_names (list): list of field names
        database_name (string): database name used to connect database

    Returns:
        None.

    """
    assert len(field_names) > 0, "Table has no fields."
    assert len(rows) > 0, "Error displaying table, rows list is empty."

    while True:
        prompt = (f"Which field from '{selected_table}' do you want to update? "
                "Press <Enter> to go back.")
        choice = get_choice(field_names, prompt)
        if choice is None:
            print("Going back...\n")
            break

        selected_field = field_names[choice - 1]

        try:
            print("Which row do you want to update? Use row numbers.")
            for num, row in enumerate(rows):
                print(f"({num + 1}) {row[choice - 1]}")
            
            row_number = input()
            row_number = int(row_number) - 1

            current_value = rows[row_number][choice - 1]

            print(f"What do you want to update '{current_value}' to?")
            new_value = input()

            while True:
                print(f"Confirm change from '{current_value}' to '{new_value}'? y/n")
                proceed = input()
                if proceed in {'y', 'n'}:
                    break
                
            if proceed == 'y':
                sql = (f"UPDATE {selected_table} SET {selected_field} = '{new_value}' "
                        f"WHERE {field_names[0]} = '{rows[row_number][0]}';")
                execute_sql(sql, database_name, None)
            break
        except Exception: # pragma: no cover
            print("Error: invalid input.")


def delete_record(database_name, selected_table, field_names, rows):
    while True:
        try:
            print(f"Which record from '{selected_table}' do you want to delete? Use row numbers. "
                "Press <Enter> to go back.")
            display_table(selected_table, rows, field_names)
            print("Row number: ")
            raw_input = input()
            if raw_input == '':
                print("Going back...\n")
                break

            row_number = int(raw_input) - 1

            if row_number < 0:
                raise Exception # pragma: no cover

            while True:
                print(f"Confirm deletion of {rows[row_number]} from {selected_table}'? y/n")
                proceed = input()
                if proceed in {'y', 'n'}:
                    break

            if proceed == 'y':
                sql = f"DELETE FROM {selected_table} WHERE {field_names[0]} = '{rows[row_number][0]}'"
                execute_sql(sql, database_name, None)
            break
        except Exception: # pragma: no cover
            print(f"Error: {raw_input} is invalid.")


def main():  # pragma: no cover
    """Runs the main program logic."""

    database_name = "Northwind.db"

    tables_list = get_tables(database_name)

    while True:
        prompt = "Enter a number to select table or press <Enter> to quit program:"
        choice = get_choice(tables_list, prompt)
        if choice is None:
            sys.exit("Exiting program...")
        
        selected_table = tables_list[choice - 1]

        meta_data_and_rows = get_table_data(selected_table, database_name)

        field_names = meta_data_and_rows[0]
        rows = meta_data_and_rows[1]

        display_table(selected_table, rows, field_names)

        while True:
            prompt = (f"Enter a number to either INSERT, UPDATE or DELETE a row in '{selected_table}'. "
                      "Press <Enter> to choose a different table.")
            options = ["Insert", "Update", "Delete"]
            choice = get_choice(options, prompt)
            if choice is None:
                break

            selected_option = options[choice - 1]

            if selected_option == "Insert":
                insert_record(selected_table, field_names, database_name)

            if selected_option == "Update":
                update_record(database_name, selected_table, field_names, rows)

            if selected_option == "Delete":
                delete_record(database_name, selected_table, field_names, rows)

            meta_data_and_rows = get_table_data(selected_table, database_name)
            rows = meta_data_and_rows[1]


if __name__ == "__main__":  # pragma: no cover
    main()
