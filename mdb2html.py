import pandas as pd
import pyodbc
import os
import toml
warnings.filterwarnings('ignore', 'pandas only supports SQLAlchemy')

# Load configuration from file
config = toml.load("config.toml")

# Connect to the Access database
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    fr'DBQ={config["database_path"]};'
)
cnxn = pyodbc.connect(conn_str)

# Form the SQL query
columns = ', '.join(config["columns"])
sql = f"SELECT {columns} FROM tblContacts ORDER BY fldDateStr DESC, fldTimeOnStr DESC"

df = pd.read_sql_query(sql, cnxn)

# Rename the columns according to config
df.rename(columns=config["column_names"], inplace=True)

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
     <link rel="stylesheet" href="{config['general']['stylesheet']}">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
        $(document).ready(function(){
            $("#searchInput").on("keyup", function() {
                var value = $(this).val().toLowerCase();
                $("#myTable tr").filter(function() {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                });
            });
            $("#toggleButton").click(function(){
                $("#restTable").toggle();
            });
        });
    </script>
</head>
<body>
    <div class="container">
        <h1>{config["page_title"]}</h1>
        <input id="searchInput" type="text" placeholder="Search by callsign..">
        <button id="toggleButton">Show/Hide Older Contacts</button>
        {html_table_top10}
        <div id="restTable" style="display: none;">
            {html_table_rest}
        </div>
    </div>
</body>
</html>

"""

# Write the HTML page to a file
with open('log.html', 'w') as f:
    f.write(html_page)
