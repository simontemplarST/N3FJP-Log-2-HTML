import pandas as pd
import pyodbc
import os
import configparser
import warnings
warnings.filterwarnings('ignore', 'pandas only supports SQLAlchemy')

# Read the configuration from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the values from the configuration
page_title = config.get('general', 'page_title')
database_path = config.get('general', 'database_path')
output_dir = config.get('general', 'output_dir')
output_filename = config.get('general', 'output_filename')
stylesheet = config.get('general', 'stylesheet')

fldBand = config.get('table_columns', 'fldBand')
fldCall = config.get('table_columns', 'fldCall')
fldMode = config.get('table_columns', 'fldMode')
fldRstR = config.get('table_columns', 'fldRstR')
fldRstS = config.get('table_columns', 'fldRstS')
fldSPCNum = config.get('table_columns', 'fldSPCNum')
fldDateStr = config.get('table_columns', 'fldDateStr')
fldTimeOnStr = config.get('table_columns', 'fldTimeOnStr')

# Convert the database path and output directory to the appropriate format
database_path = os.path.normpath(database_path)
output_dir = os.path.normpath(output_dir)


# Connect to the Access database
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    fr'DBQ={config.get("general", "database_path")};'
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
# Generate the HTML page snippet including the search script
html = (
    "<!DOCTYPE html>\n"
    "<html>\n"
    "<head>\n"
    "  <meta charset=\"UTF-8\">\n"
    f"  <title>{page_title}</title>\n"
    f'  <link rel="stylesheet" type="text/css" href="{stylesheet}">\n'
    '  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>\n'
    "  <style>\n"
    "    /* Add your custom CSS styles here */\n"
    "  </style>\n"
    "</head>\n"
    "<body>\n"
    f'  <h1>{page_title}</h1>\n'
    '  <input type="text" id="searchInput" placeholder="Search by Callsign">\n'
    "  <table>\n"
    "    <thead>\n"
    "      <tr>\n"
    f"        <th>{fldBand}</th>\n"
    f"        <th>{fldCall}</th>\n"
    f"        <th>{fldMode}</th>\n"
    f"        <th>{fldRstR}</th>\n"
    f"        <th>{fldRstS}</th>\n"
    f"        <th>{fldSPCNum}</th>\n"
    f"        <th>{fldDateStr}</th>\n"
    f"        <th>{fldTimeOnStr}</th>\n"
    "      </tr>\n"
    "    </thead>\n"
    "    <tbody>\n"
    "      <!-- Table rows will be dynamically generated here -->\n"
    "    </tbody>\n"
    "  </table>\n"
    '  <script>\n'
    "    $(document).ready(function() {\n"
    "      $('#searchInput').on('keyup', function() {\n"
    "        var value = $(this).val().toLowerCase();\n"
    "        $('tbody tr').filter(function() {\n"
    "          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);\n"
    "        });\n"
    "      });\n"
    "    });\n"
    "  </script>\n"
    "</body>\n"
    "</</html>\n"
)

# Save the HTML snippet to a file
output_file = os.path.join(config['output_dir'], config['output_filename'])
with open(output_file, 'w') as f:
    f.write(html)

# Write the HTML page to a file
with open('log.html', 'w') as f:
    f.write(html_page)
