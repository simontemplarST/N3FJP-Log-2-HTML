import pandas as pd
import pyodbc
import os
import warnings
warnings.filterwarnings('ignore', 'pandas only supports SQLAlchemy')

<<<<<<< Updated upstream
# Connect to the Access database
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\c\Documents\Affirmatech\N3FJP Software\ACLog\LogData.mdb;'
=======
# Read the configuration from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the values from the configuration
page_title = config.get('general', 'page_title')
database_path = config.get('general', 'database_path')
output_dir = config.get('general', 'output_dir')
output_filename = config.get('general', 'output_filename')
stylesheet = config.get('general', 'stylesheet')

fldBand = config.get('columns', 'fldBand')
fldCall = config.get('columns', 'fldCall')
fldMode = config.get('columns', 'fldMode')
fldRstR = config.get('columns', 'fldRstR')
fldRstS = config.get('columns', 'fldRstS')
fldSPCNum = config.get('columns', 'fldSPCNum')
fldDateStr = config.get('columns', 'fldDateStr')
fldTimeOnStr = config.get('columns', 'fldTimeOnStr')

# Convert the database path and output directory to the appropriate format
database_path = os.path.normpath(database_path)
output_dir = os.path.normpath(output_dir)


# Connect to the Access database
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    fr'DBQ={config.get("general", "database_path")};'
>>>>>>> Stashed changes
)
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
html_page = f"""
<!DOCTYPE html>
<html>
<head>
    <title>N0YEP's Log</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #2E3440;
            color: #D8DEE9;
            margin: 0;
            padding: 0;
        }}
        h1 {{
            text-align: center;
            color: #88C0D0;
        }}
        table {{
            table-layout: auto;
            margin: 100px auto;
           
            border-collapse: collapse;
        }}
        th, td {{
            padding: 0.5em;
            border: 1px solid #4C566A;
            text-align: left;
        }}
        th.Country, td.Country {{
            width: 100px;
        }}
        th {{
            background-color: #3B4252;
            color: #ECEFF4;
        }}
        tr:nth-child(even) {{
            background-color: #3B4252;
        }}
        #dropdown {{
            display: none;
        }}
        #searchInput {{
            display: block;
            width: 300px;
            margin: 20px auto;
        }}
    </style>
    <script>
        function searchTable() {{
            var input, filter, table, tr, td, i, txtValue;
            input = document.getElementById("searchInput");
            filter = input.value.toUpperCase();
            table = document.getElementsByClassName("top10")[0];
            tr = table.getElementsByTagName("tr");
            for (i = 0; i < tr.length; i++) {{
                td = tr[i].getElementsByTagName("td")[2]; // column index for "Call"
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
                td = tr[i].getElementsByTagName("td")[2]; // column index for "Call"
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
    <h1>N0YEP's Log</h1>
    <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for callsigns..">
    {html_table_top10}
    {html_table_rest}
</body>
</html>
"""

# Write the HTML page to a file
with open('log.html', 'w') as f:
    f.write(html_page)
