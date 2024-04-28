"""This program displays a text editor using tkinter.
It allows users to Save and Open text files.

Resources:
    https://tkinter.com/create-font-chooser-app-python-tkinter-gui-tutorial-192/

Contributers:
    Timothy El Moughayar

"""

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import font


class Root(tk.Tk):
    """This class creates root window for text editor program.

    Attributes
    ----------

    file_path : str
        path of file that's being used

    text_content : str
        text that's on the page

    Methods
    -------

    open_font_chooser()
        Creates Font Chooser window and changes text's font

    open_about_box()
        Creates About box and finds word count of file

    new_file()
        Clears file path and text from page

    save_file()
        Saves current file

    save_as_file()
        Opens save as dialogue box and saves the current document as a new file

    open_file()
        Opens file and displays it on the page

    copy_text(keyboard_shortcut=True)
        Copies selected text to clipboard

    cut_text(keyboard_shortcut=True)
        Cuts selected text to clipboard

    paste_text()
        Pastes text from clipboard

    _update_title()
        Sets title of Root window to file name. If there is no file open,
        title is set to 'Untitled'.

    """

    _main_menu = None
    _copied_text = None
    _file_path = None

    @property
    def file_path(self):
        """Get file path.

        Returns:
            str: file path
        """
        return self._file_path

    @file_path.setter
    def file_path(self, new_file_path):
        """Set file path and update title.

        Args:
            new_file_path (str): new file path

        """
        self._file_path = new_file_path
        self._update_title()

    @property
    def text_content(self):
        """Get all the text from text editor page."""
        return self._text_frame.text

    def __init__(self, *args, **kwargs):
        """Create root object and set up root window."""
        tk.Tk.__init__(self, *args, **kwargs)

        self.file_path = None
        self.geometry("700x800")

        # Creates top navigation
        self._main_menu = MainMenu(self)

        # Creates text editor page
        self._text_frame = TextFrame(self)
        self._text_frame.pack(expand=True, fill=tk.BOTH)

    def open_font_chooser(self):
        """Create Font Chooser window and change text's font."""
        font_chooser = FontChooser(self)

        # if "Ok" was pressed, change font
        if font_chooser.ok_pressed:
            self._text_frame.change_font(font_chooser.selected_font)

    def open_about_box(self):
        """Create About box and find word count of file."""
        word_count = len(self.text_content.split())
        AboutBox(self, self.file_path, word_count)

    def new_file(self):
        """Clear file path and text from page."""
        self._text_frame.text = ""
        self.file_path = None

    def save_file(self):
        # If there's no file open, then it opens save as dialogue box
        if self.file_path is None:
            self.save_as_file()

        # Save to current file
        else:
            text_file = open(self.file_path, 'w', encoding="utf-8")
            text_file.write(self._text_frame.text)
            text_file.close()

    def save_as_file(self):
        """Open save as dialogue box and save the current
        document as a new file.
        """
        # Opens save as dialog box
        new_file_path = filedialog.asksaveasfilename(defaultextension=".*",
                                                    initialpath="C:/Documents/",
                                                    title="Save As",
                                                    filetypes=("Text Document", "*.txt"))

        # If Cancel wasn't pressed, then read file onto page
        if new_file_path:
            self.file_path = new_file_path
            text_file = open(self.file_path, 'w', encoding="utf-8")
            text_file.write(self._text_frame.text)
            text_file.close()

    def open_file(self):
        """Open file and display it on the page."""
        new_file_path = filedialog.askopenfilename(
            filetypes=(("Text Files", "*.txt"), ))

        # If Cancel wasn't pressed, then read file onto page
        if new_file_path:
            self.file_path = new_file_path
            with open(new_file_path, 'r', encoding="utf-8") as text_file:
                file_contents = text_file.read()
                self._text_frame.text = file_contents

    def copy_text(self, keyboard_shortcut=True):
        """Copie selected text to clipboard.

        Args:
            keyboard_shortcut (bool):
                indicates whether or not keyboard shortcut
                was used (defualt True)
        """
        # Check if keyboard shorcut used
        if keyboard_shortcut:
            # Copy text from clipboard
            self._copied_text = self.clipboard_get()
        else:
            # Copies selected text and adds it to the clipboard
            try:
                self._copied_text = self._text_frame.selection_get()
                self.clipboard_clear()
                self.clipboard_append(self._copied_text)
            except tk.TclError:
                pass

    def cut_text(self, keyboard_shortcut=True):
        """Cut selected text to clipboard.

        Args:
            keyboard_shortcut (bool):
                indicates whether or not keyboard shortcut was used (defualt True)
        """
        # Check if keyboard shorcut used
        if keyboard_shortcut:
            # Copy text from clipboard
            self._copied_text = self.clipboard_get()
        else:
            try:
                # Copies and deletes selected text and adds it to the clipboard
                self._copied_text = self._text_frame.selection_get()
                self._text_frame.selection_deleter()
                self.clipboard_clear()
                self.clipboard_append(self._copied_text)
            except tk.TclError:
                pass

    def paste_text(self):
        """Paste text from clipboard."""
        self._copied_text = self.clipboard_get()
        self._text_frame.paste_text(self._copied_text)

    def _update_title(self):
        """Set title of Root window to file name. If there is no file open,
        title is set to 'Untitled'.
        """
        if self.file_path is None:
            filename = "Untitled"
        else:
            filename = os.path.basename(self.file_path)

        title = f"{filename} - Macrohard Word"
        self.title(title)


class MainMenu(tk.Menu):
    """Create Main menu top navigation bar that contains file, edit,
        format, and help menus.
    ...

    Attributes
    ----------
    root : class
        the root window

    """

    @property
    def root(self):
        """Get root."""
        return self._root

    def __init__(self, root, *args, **kwargs):
        """Create nav bar with menu items."""
        tk.Menu.__init__(self, root, *args, **kwargs)
        self._root = root

        # Creates menu items
        file_menu = FileMenu(self, tearoff=0)
        edit_menu = EditMenu(self, tearoff=0)
        format_menu = FormatMenu(self, tearoff=0)
        help_menu = HelpMenu(self, tearoff=0)

        # Adds dropdown menus to menu bar
        self.add_cascade(label="File", menu=file_menu)
        self.add_cascade(label="Edit", menu=edit_menu)
        self.add_cascade(label="Format", menu=format_menu)
        self.add_cascade(label="Help", menu=help_menu)

        root.config(menu=self)


class FileMenu(tk.Menu):
    """Create File menu to give option to save, open, and
    create new files.
    """

    def __init__(self, *args, **kwargs):
        tk.Menu.__init__(self, *args, **kwargs)
        self.add_command(label="New", command=self.master.root.new_file)
        self.add_command(label="Save", command=self.master.root.save_file)
        self.add_command(
            label="Save as", command=self.master.root.save_as_file)
        self.add_command(label="Open", command=self.master.root.open_file)
        self.add_command(label="Exit", command=self.master.quit)


class EditMenu(tk.Menu):
    """Create dropdown edit menu for copy, paste, and cut options."""
    def __init__(self, *args, **kwargs):
        tk.Menu.__init__(self, *args, **kwargs)

        # Adds Cut, Copy, and Paste to the edit dropdown menu
        self.add_command(label="Cut", command=lambda:
                         self.master.root.cut_text(False),
                         accelerator="(Ctrl+x)")
        self.add_command(label="Copy", command=lambda:
                         self.master.root.copy_text(False),
                         accelerator="(Ctrl+c)")
        self.add_command(label="Paste", command=lambda:
                         self.master.root.paste_text(),
                         accelerator="(Ctrl+v)")

        # Creates keyboard shorcuts for Cut, Copy and Paste commands
        self.bind("<Control-Key-x>", self.master.root.cut_text)
        self.bind("<Control-Key-c>", self.master.root.copy_text)
        self.bind("<Control-Key-v>", self.master.root.paste_text)


class FormatMenu(tk.Menu):
    """Create dropdown Format menu that includes a Font picker."""
    def __init__(self, *args, **kwargs):
        tk.Menu.__init__(self, *args, **kwargs)
        self.add_command(
            label="Fonts", command=self.master.root.open_font_chooser)


class HelpMenu(tk.Menu):
    """Create dropdown Help menu with an About option."""
    def __init__(self, *args, **kwargs):
        tk.Menu.__init__(self, *args, **kwargs)
        self.add_command(
            label="About", command=self.master.root.open_about_box)


class TextFrame(tk.Frame):
    """Create text area for editing text.
    ...

    Attributes
    ----------
    text : str
        the text on the page

    Methods
    -------
    selection_deleter()
        Deletes highlighted/selected text
    paste_text(selected_text)
        Inserts the given text at the cursor
    change_font(selected_font)
        Changes text to selected font
    """

    _text_area = None

    @property
    def text(self):
        """Get text content of page."""
        return self._text_area.get(1.0, tk.END)

    @text.setter
    def text(self, value):
        """Delete the text on page and set it to given value."""
        self._text_area.delete(1.0, tk.END)
        self._text_area.insert(tk.END, str(value))

    def __init__(self, *args, **kwargs):
        """Create the text area and scrollbars."""
        tk.Frame.__init__(self, *args, **kwargs)

        # Sets current font's properties
        self.current_font = font.Font(family="Helvetica", size="12")

        text_frame = tk.Frame(self)

        # Creates text area
        self._text_area = tk.Text(text_frame, wrap="none",
                                  borderwidth=0,
                                  font=self.current_font,
                                  undo=True, selectbackground="light blue",
                                  selectforeground="black")

        # Creates vertical and horizontal scroll bars
        v_scrollbar = tk.Scrollbar(text_frame, orient="vertical",
                                   command=self._text_area.yview)
        h_scrollbar = tk.Scrollbar(text_frame, orient="horizontal",
                                   command=self._text_area.xview)

        # Makes scroll bars control the text area's position
        self._text_area.configure(yscrollcommand=v_scrollbar.set,
                                  xscrollcommand=h_scrollbar.set)

        # Places text editing area in text frame
        self._text_area.grid(row=0, column=0, sticky="nsew")

        # Places scrollbars in text frame
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configures row and columns for alignment
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Places text frame in root window
        text_frame.pack(side="top", fill="both", expand=True)

        # Places cursor in text area
        self._text_area.focus_set()

    def selection_deleter(self):
        """Delete highlighted/selected text."""
        self._text_area.delete("sel.first", "sel.last")

    def paste_text(self, selected_text):
        """Insert the given text at the cursor.

        Args:
            selected_text (str): text that has been selected
        """
        # Gets postion of the curor
        position = self._text_area.index(tk.INSERT)

        # Inserts the selected text at the cursor's position
        self._text_area.insert(position, selected_text)

    def change_font(self, selected_font):
        """Change text to selected font."""
        self.current_font.config(family=selected_font)


class FontChooser(tk.Toplevel):
    """Create font chooser window where users can
    select different fonts.
    ...

    Attributes
    ----------
    selected_font : str
        font selected from font list box
    ok_pressed : bool
        True if Ok button pressed, False otherwise

    Methods
    -------
    add_widgets()
        Creates, then places font selection box, "Cancel" button,
        and "Ok" button into Font Picker window
    _cancel_click()
        Closes Font Picker window and sets ok_pressed to false
    _ok_click()
        Changes text to selected font and closes window
    _set_properties()
        Sets the Font Picker window properties
    """

    _ok_pressed = False
    _selected_font = None

    @property
    def selected_font(self):
        """Get font selected from font list box."""
        return self._selected_font

    @property
    def ok_pressed(self):
        """Get status on if "ok" was pressed."""
        return self._ok_pressed

    def __init__(self, *args, **kwargs):
        """Create window, set window properties, and add widgets."""
        super().__init__(*args, **kwargs, padx=10, pady=10)

        self._set_properties()
        self._add_widgets()
        self.wait_window()

    def _add_widgets(self):
        """Create and place font selection box, "Cancel" button,
        and "Ok" button into Font Picker window.
        """
        label = tk.Label(self, text="Choose Font:")
        label.grid(row=0, column=0, sticky=tk.W)

        # Creates and places "Ok" button
        ok_button = tk.Button(self,
                              text="OK",
                              command=self._ok_click)
        ok_button.grid(row=2, column=2, sticky=tk.E, padx=(100, 0))

        # Creates and places "Cancel" button
        cancel_button = tk.Button(self,
                                  text="Cancel",
                                  command=self._cancel_click)
        cancel_button.grid(row=2, column=3, sticky=tk.E)

        # Creates and places list box for fonts
        self.my_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.my_listbox.grid(row=1, column=0, columnspan=5, sticky=tk.E+tk.W)

        # Automatically focuses on font selection box
        self.my_listbox.focus_set()

        # Populates the font selection box
        for f in font.families():
            self.my_listbox.insert('end', f)

        # Keboard shorcuts
        self.bind("<Return>", self._ok_click)
        self.bind("<Escape>", self._cancel_click)

    def _cancel_click(self, event=None):
        """Close Font Picker window."""
        self._ok_pressed = False
        self.destroy()

    def _ok_click(self, event=None):
        """Get the selected font and close Font Picker window."""
        self._selected_font = self.my_listbox.get(
            self.my_listbox.curselection())
        self._ok_pressed = True
        self.destroy()

    def _set_properties(self):
        """Set the Font Picker window properties."""
        self.resizable(False, False)
        width = 268
        height = 225

        self.title("Font Chooser")
        x = (self.master.winfo_screenwidth() - width) // 2
        y = (self.master.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")


class AboutBox(tk.Toplevel):
    """Create About Box that displays name, path, size, and word count of the file."""

    _name = None
    _path = None
    _file_size = None
    _word_count = None

    @property
    def file_size(self):
        """Get the file size.

        Returns:
            str: the file size which includes size type. 
        """
        return self._file_size

    @file_size.setter
    def file_size(self, value):
        """Set size of file in Bytes and convert to Kilobytes or
        Megabytes if necessary.
        """
        # If size of file over 1000 Bytes, it converts to KB
        # and rounds it to the 2nd decimal
        if value > 1000:
            value = round(value / 1024, 2)
            self._file_size = f"{value} KB"

            # If size of file over 1000 KB, it converts to MB
            # and rounds it to the 2nd decimal
            if value > 1000:
                value = round(value / 1024, 2)
                self._file_size = f"{value} MB"
        else:
            self._file_size = f"{value} Bytes"

    def __init__(self, root, file_path, word_count, *args, **kwargs):
        """Create About box and widgets."""
        super().__init__(*args, **kwargs, padx=10, pady=10)

        self._set_properties()
        self._add_widgets(file_path, word_count)
        self.wait_window()

    def _add_widgets(self, file_path, word_count):
        """Add info and ok button to window."""
        # If no file open, ask user to open or save file
        if file_path is None:
            label = tk.Label(
                self, text="Save or Open a file.", padx=50, pady=50)
            label.pack()
        # Displays the info and ok button.
        else:
            self._word_count = word_count
            self.set_about_info(file_path)

            keys = ["Name:", "Path:", "Size:", "Words:"]
            values = [self._name, self._path,
                      self._file_size, self._word_count]

            # Concatenates info to Labels
            for i, key in enumerate(keys):
                label = tk.Label(self,
                                 text=f"{key}\t{values[i]}")
                label.grid(row=i, column=0, sticky=tk.W)

            # Creates Ok button that closes window
            ok_button = tk.Button(self,
                                  text="OK",
                                  command=self._close_box)
            ok_button.grid(row=5, column=1, sticky=tk.E)

            # Return and Escape keys close window
            self.bind("<Return>", self._close_box)
            self.bind("<Escape>", self._close_box)

    def _close_box(self):
        """Close About window."""
        self.destroy()

    def _set_properties(self):
        """Set the About window properties."""
        self.title("About")
        self.resizable(False, False)

    def set_about_info(self, file_path):
        """Set the name, path and size of file."""
        stats = os.stat(file_path)

        self._name = os.path.basename(file_path)
        self._path = file_path
        self.file_size = stats.st_size


if __name__ == "__main__":
    root = Root()
    root.mainloop()
