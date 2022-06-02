from tokenize import maybe
from flask import Flask, render_template
import pyodbc

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/')
def tables():
    #set up HSI table
    headings_hsi=("SBSN","SPN","UUID","SP","cUUID","VIRTUAL_STATE","PARSED_DATE")
    data_hsi=display_table("IKEA_HSI",headings_hsi)
    #set up MP table
    headings_mp=("ST","PN","FWRI","BBLK","HWRI","SN","UUID","IPM","SSO","PWRM","PARSED_DATE")
    data_mp=display_table("IKEA_MP",headings_mp)
    return render_template("tables.html",headings_hsi=headings_hsi,data_hsi=data_hsi,headings_mp=headings_mp,data_mp=data_mp)


def display_table(table,columns)->list:

    try:
        #set up SQL server connection
        conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=LAPTOP-TMP50LAM;'
                        'Database=AdhocDB;'
                        'Trusted_Connection=yes;')
    
               
        cursor = conn.cursor()
        cursor.execute("SELECT " +",".join(list(columns)) + " FROM "+table)
        
        data_set=list(cursor.fetchall())
        
        cursor.close()
        return data_set	
	
    except Exception as e:
        print(e)
        
