import sys
import subprocess
import win32gui
import win32process
import pandas as pd
import pyodbc
import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Hide the command prompt window
def hide_console_window():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    _, pid = win32process.GetWindowThreadProcessId(window)
    subprocess.call(['taskkill', '/F', '/PID', str(pid)], creationflags=subprocess.CREATE_NO_WINDOW)

# Connect to the Access database
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=Y:\LogData.mdb;'
)

def generate_html(output_file):
    cnxn = pyodbc.connect(conn_str)
    sql = "SELECT fldBand, fldCall, fldMode, fldRstR, fldRstS, fldSPCNum, fldDateStr, fldTimeOnStr FROM tblContacts ORDER BY fldDateStr DESC, fldTimeOnStr DESC"
    df = pd.read_sql_query(sql, cnxn)

    # Rename the columns
    df = df.rename(columns={
        'fldBand': 'Band',
        'fldCall': 'Call',
        'fldMode': 'Mode',
        'fldRstR': 'S',
        'fldRstS': 'R',
        'fldSPCNum': 'Country',
        'fldDateStr': 'Date',
        'fldTimeOnStr': 'Time'
    })

    # Split the dataframe into two parts: top 10 rows and the rest
    df_top10 = df.head(10)
    df_rest = df.tail(len(df) - 10)

    # Generate the HTML tables
    html_table_top10 = df_top10.to_html(classes='top10', index=False)
    html_table_rest = df_rest.to_html(classes='rest', index=False)

    # Create the HTML page
    css_file = css_var.get()
    css_path = os.path.join('CSS', css_file)
    css_link = f'    <link rel="stylesheet" type="text/css" href="{css_path}">\n'

    html_page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>N0YEP's Log</title>
        {css_link}
        <script>
            function searchTable() {{
                var input, filter, table, tr, td, i, txtValue;
                input = document.getElementById("searchInput");
                filter = input.value.toUpperCase();
                table = document.getElementsByClassName("top10")[0];
                tr = table.getElementsByTagName("tr");
                for (i = 0; i < tr.length; i++) {{
                    td = tr[i].getElementsByTagName("td")[1]; // column index for "Call"
                    if (td) {{
                        txtValue = td.textContent || td.innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {{
                            tr[i].style.display = "";
                        }} else {{
                            tr[i].style.display = "none";
                        }}
                    }}
                }}
                table = document.getElementsByClassName("rest")[0];
                tr = table.getElementsByTagName("tr");
                for (i = 0; i < tr.length; i++) {{
                    td = tr[i].getElementsByTagName("td")[1]; // column index for "Call"
                    if (td) {{
                        txtValue = td.textContent || td.innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {{
                            tr[i].style.display = "";
                        }} else {{
                            tr[i].style.display = "none";
                        }}
                    }}
                }}
            }}
        </script>
    </head>
    <body>
        <center><h1>N0YEP's Log</h1></center>
        <center><input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for callsigns.."><center>
        {html_table_top10}
        {html_table_rest}
    </body>
    </html>
    """

    with open(output_file, 'w') as f:
        f.write(html_page)

def run_script():
    output_file = file_path.get()
    generate_html(output_file)

    interval = int(time_var.get()) * 60 * 1000  # Convert minutes to milliseconds
    threading.Timer(interval, run_script).start()  # Run the script at the specified interval

def select_output_file():
    file_path.set(filedialog.asksaveasfilename(defaultextension='.html', filetypes=[('HTML Files', '*.html')]))

# Hide the command prompt window
if sys.argv[-1] != '-noconsole':
    hide_console_window()

# Create the GUI
root = tk.Tk()
root.title("Log to HTML Converter")

file_path = tk.StringVar()
css_var = tk.StringVar()
time_var = tk.StringVar(value='10')  # Default interval value

# Output File
output_file_label = ttk.Label(root, text="Output File:")
output_file_label.grid(row=0, column=0, sticky="w")

output_file_entry = ttk.Entry(root, textvariable=file_path)
output_file_entry.grid(row=0, column=1)

output_file_button = ttk.Button(root, text="Select", command=select_output_file)
output_file_button.grid(row=0, column=2)

# CSS Dropdown
css_label = ttk.Label(root, text="CSS Style:")
css_label.grid(row=1, column=0, sticky="w")

css_dropdown = ttk.Combobox(root, textvariable=css_var, state="readonly")
css_dropdown.grid(row=1, column=1)
css_dropdown['values'] = os.listdir('CSS')
css_dropdown.current(0)

# Time Interval Dropdown
time_label = ttk.Label(root, text="Interval (minutes):")
time_label.grid(row=2, column=0, sticky="w")

time_dropdown = ttk.Combobox(root, textvariable=time_var, state="readonly")
time_dropdown.grid(row=2, column=1)
time_dropdown['values'] = ('1', '5', '10', '15', '30', '60')
time_dropdown.current(2)  # Set default interval to 10 minutes

# Generate HTML Button
generate_button = ttk.Button(root, text="Generate HTML", command=run_script)
generate_button.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
