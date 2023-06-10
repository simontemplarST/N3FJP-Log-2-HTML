import pandas as pd
import pyodbc
import os
import toml
import warning
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
# Generate the HTML page snippet including the search script
html = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{}</title>
  <link rel="stylesheet" type="text/css" href="{}">
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <style>
    /* Add your custom CSS styles here */
  </style>
</head>
<body>
  <h1>{}</h1>
  <input type="text" id="searchInput" placeholder="Search by Callsign">
  <table>
    <thead>
      <tr>
        <th>{}</th>
        <th>{}</th>
        <th>{}</th>
        <th>{}</th>
        <th>{}</th>
        <th>{}</th>
        <th>{}</th>
        <th>{}</th>
        <th>{}</th>
      </tr>
    </thead>
    <tbody>
      <!-- Table rows will be dynamically generated here -->
    </tbody>
  </table>
  <script>
    $(document).ready(function() {
      $("#searchInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("tbody tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
      });
    });
  </script>
</body>
</html>
'''

# Save the HTML snippet to a file
output_file = os.path.join(config['output_dir'], config['output_filename'])
with open(output_file, 'w') as f:
    f.write(html)

# Write the HTML page to a file
with open('log.html', 'w') as f:
    f.write(html_page)
