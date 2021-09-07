"""
Automatically create a new jupyter notebook and bibliography
entry given a paper name and bibtex.
"""

import os
import PySimpleGUI as sg
import pybtex.database

BIB_NAME = "papers.bib"

# Layout of the info prompt
paper_info_prompt_layout = [
        [
            sg.Text("File Title:"),
            sg.InputText()
        ],
        [
            sg.Text("Bibtex Entry:"),
            sg.Multiline(size=(60,15))
        ],
        [
            sg.Button("Cancel"), 
            sg.Button("Ok", bind_return_key=True)
        ]
]

def get_paper_info():

    paper_info_prompt_window = sg.Window("Create a New Paper Notebook", paper_info_prompt_layout)

    while True:
        event, values = paper_info_prompt_window.read()

        if event == sg.WIN_CLOSED or event == "Cancel":
            paper_info_prompt_window.close()
            exit()
        elif event == "Ok":
            file_title = values[0]
            paper_bibtex_string = values[1]
            if file_title and paper_bibtex_string: # make sure data was entered into both cells
                paper_info_prompt_window.close()
                return file_title, paper_bibtex_string
            else:
                continue
        else:
            continue

def show_error_window(error_message):
    error_layout = [
            [sg.Text(error_message)],
            [sg.Button("Close", bind_return_key=True)]
    ]

    error_window = sg.Window("Error", error_layout)

    while True:
        event, values = error_window.read()
        if event in (sg.WIN_CLOSED, "Close"):
            error_window.close()
            exit()
        else:
            continue

def create_bibtex_entry(file_title, paper_bibtex_string):
    # convert bibtex string to bibtex object
    bib_data = pybtex.database.parse_string(paper_bibtex_string, "bibtex")
    old_key = next(iter(bib_data.entries))
    paper_bibtex_entry = bib_data.entries[old_key]
    # use file_title as new entry name
    paper_bibtex_entry.key = file_title

    return paper_bibtex_entry

def create_table_of_contents(full_bib):
    """
    Create a table of contents given the full bibliography
    """


def main():
    # get information
    file_title, paper_bibtex_string = get_paper_info()

    # clean file_title (remove any extension)
    file_title = os.path.splitext(file_title)[0]

    # create bibtex entry
    paper_bibtex_entry = create_bibtex_entry(file_title, paper_bibtex_string)

    # read in existing bibliography
    full_bib = pybtex.database.parse_file(BIB_NAME, bib_format="bibtex")

    if paper_bibtex_entry.key in full_bib.entries:
        # file_title is already used
        show_error_window("File title is already in use")
        # exits

    # add bibtex entry to bibliography
    full_bib.entries[paper_bibtex_entry.key] = paper_bibtex_entry

    # write new bibliography
    full_bib.to_file(BIB_NAME, bib_format="bibtex")

    # regenerate table of contents

    # generate new notebook

if __name__ == "__main__":
    main()
