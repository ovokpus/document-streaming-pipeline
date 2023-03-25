from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import json
from pydantic import BaseModel

from datetime import datetime
from kafka import KafkaProducer, producer

class InvoiceItem(BaseModel):
    InvoiceNo: int
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: int
    Country: str
    

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/invoiceitem", status_code=status.HTTP_201_CREATED)
async def post_invoice_item(item: InvoiceItem):
    print("Message Received: ", item)
    try:
        date = datetime.strptime(item.InvoiceDate, '%d/%m/%Y %H:%M')
        print("Date as timestamp: ", date)
        
        # Replace date with new datetime
        item.InvoiceDate = date.strftime('%d-%m-%Y %H:%M:%S')
        print("new item date format: ", item.InvoiceDate)
        
        item_json = jsonable_encoder(item)
        
        json_string = json.dumps(item_json)
        print("json string: ", json_string)
        
        # Produce the message to Kafka
        produce_kafka_message(json_string)
        
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item_json)
    
    except ValueError as e:
        print("Error: ", e)
        raise HTTPException(status_code=400, detail="Invalid date format")
        # return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=item_json)

def produce_kafka_message(message):
    producer = KafkaProducer(bootstrap_servers='kafka:9092', acks=1)
    producer.send('ingestiontopic', message.encode('utf-8'))
    producer.flush()