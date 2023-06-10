# N3FJP Log to HTML

This script converts a Microsoft Access database file into a styled HTML page displaying a log of contacts. The table is sorted by date and includes a search bar for looking up contacts by callsign. It uses a TOML configuration file for ease of use.

## Installation

1. Clone this repository or download the files to your local machine.

2. Install the necessary Python packages. You can do this by running the following command in your terminal:

```bash
pip install pandas pyodbc toml
```

#### This script was tested with Python 3.8. Other versions might work but are not guaranteed.

### Note:
You will also need the Microsoft Access Database Engine, which can be downloaded from the Microsoft Download Center. Please note that you need to install the version (32-bit or 64-bit) that matches your Python interpreter.

## Usage

Update the config.toml file with the path to your database, the desired page title, and the desired output path and filename. For example:

```database_path = "C:\\Users\\c\\Documents\\Affirmatech\\N3FJP Software\\ACLog\\LogData.mdb"
page_title = "N0YEP's Log"
output_path = "log.html"
```

Run the script from your terminal:
```bash
python mdb2html.py
```

Open the output file in your web browser to view the log.

# Uploading the HTML Log To A Web Host
For the sake of simplicity, you have the freedom to do this how you wish, or what best suits your workflow. 

I have provided the workflow For my personal log [here](https://cameronheard.com/log):
- Set the N3FJP database directory as "shared" under Windows
- Mounted that share on a Linux LXD container
- Wrote a bash script that runs: mdb2html.py and after that is ran, it waits 2 seconds for python to end the current PID, and then it runs `neocities upload log.html` from the directory I specified. 
    - I wrote some logic in there to say if the share is inaccessable to halt execution of the script from that point, as there is no data available. 
- Set up a cron job to run this script every five minutes. 
