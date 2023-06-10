# N3FJP Log to HTML

This script converts a Microsoft Access database file into a styled HTML page displaying a log of contacts. The table is sorted by date and includes a search bar for looking up contacts by callsign. It uses a TOML configuration file for ease of use.

## Installation

1. Clone this repository or download the files to your local machine.

2. Install the necessary Python packages. You can do this by running the following command in your terminal:

```bash
pip install pandas pyodbc 
```

#### This script was tested with Python 3.8. Other versions might work but are not guaranteed.

### Note:
You will also need the Microsoft Access Database Engine, which can be downloaded from the Microsoft Download Center. Please note that you need to install the version (32-bit or 64-bit) that matches your Python interpreter.

## Usage

Open the python script, go to line `10` and specify the path of the mdb database. 

Edit the HTML to your liking, starting on line `38`

Run the script from your terminal:
```bash
python mdb2html.py
```

Open the output file in your web browser to view the log.

# Uploading the HTML Log To A Web Host
For the sake of simplicity, you have the freedom to do this how you wish, or what best suits your workflow. 

I have provided the workflow For my personal [log](https://cameronheard.com/log):
- Set the output directory as shared under Windows
- Mounted that share on an Linux LXD container
- pass `neocities upload log.html` to a bash script. 
- Set up a cron job to run this script every five minutes. 


---

# In the works: 
Config files for easier configuration of what columns are displayed, page title, database directory, output file location, style, etc. 