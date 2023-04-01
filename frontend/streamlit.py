# from numpy import double
import streamlit as st
from pandas import DataFrame

# import numpy as np
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/", username='root', password='example')
mydb = myclient["docstreaming"]
mycol = mydb["invoices"]

st.title("Document Streaming App")
st.markdown("This app is used to stream documents from a CSV file to a :blue[MongoDB] database through :green[FastAPI],  :red[ Apache Kafka],  :blue[ Apache Spark Structured Streaming], and a :orange[Python] client.")
st.text("Microservices Architecture using Docker and Docker Compose")

# Input field for CustomerID
cust_id = st.sidebar.text_input("CustomerID:")

if cust_id:
    myquery = {"CustomerID": cust_id}
    mydoc = mycol.find(myquery, {"_id": 0, "StockCode": 0, "Description": 0, "Quantity": 0, "Country": 0, "UnitPrice": 0})
    
    df = DataFrame(mydoc)
    df.drop_duplicates(subset="InvoiceNo", keep='first', inplace=True)
    
    st.header("Output Customer Invoices")
    table2 = st.dataframe(data=df)

# Input field for Invoice number
inv_no = st.sidebar.text_input("InvoiceNo:")

if inv_no:
    myquery = { "InvoiceNo": inv_no }
    mydoc = mycol.find(myquery, {"_id": 0, "InvoiceDate": 0, "Country": 0, "CustomerID": 0})
    
    df = DataFrame(mydoc)
    
    reindexed = df.reindex(sorted(df.columns), axis=1)
    
    st.header("Output Invoice Items by InvoiceNo")
    table2 = st.dataframe(data=reindexed)