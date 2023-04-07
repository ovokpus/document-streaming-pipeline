# Document Streaming
Data Streaming workflow that sends JSON data via an API, and processed downstream with data streaming applications, and then persisted in a NoSQL database instance. Finally, the data is consumed by a Streamlit Dashboard Application. 

![image](https://github.com/ovokpus/document-streaming-pipeline/blob/main/img/doc-streaming-banner.png)

---

### Tools and Technologies Utilized

1. Python client to generate and send streaming messages
2. Fast API to ingest streaming data
3. Apache Kafka message queue as a buffer
4. Apache Spark Structured Streaming to read messages from Kafka and write to MongoDB
5. MongoDB for persisting streaming messages, and Mongo Express for viewing data inside MongoDB
6. Streamlit dashboard for consuming data

## Application Architecture

![image](https://github.com/ovokpus/document-streaming-pipeline/blob/main/img/pipeline-architecture.png)

---

## Project Setup and prerequisites
1. WSL2 (Ubuntu Distro).
2. Any good IDE for Python (VSCode, Pycharm).
3. Docker and Docker Compose, with images for Spark, MongoDB, Mongo Express.
4. API testing tool, like Postman or Insomnia.

---

### Data Preparation
E-commerce data from a UK retailer, obtained from [Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data) and from the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/index.php)

---
### Build and deploy the Data API

fastAPI UI
![image](https://github.com/ovokpus/document-streaming-pipeline/blob/main/img/fastapi-ui.png)

1. Create Python [script](https://github.com/ovokpus/document-streaming-pipeline/blob/main/client/transformer.py) to transform the data from csv to json format, and an [api client](https://github.com/ovokpus/document-streaming-pipeline/blob/main/client/api-client.py) to generate data streams that are sent to the API.
2. Implement a [fastAPI server](https://github.com/ovokpus/document-streaming-pipeline/blob/main/api/app/main.py) to receive data from the client, as well as a simple backend script to send data into the kafka topic.
3. Fire up the API with the command below, and the output shows a succesful API startup
```bash
(venv) ubuntu@DESKTOP-QRVR3E3:~/document-streaming-pipeline/api/app$ uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/home/ubuntu/document-streaming-pipeline/api/app']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [11549] using StatReload
INFO:     Started server process [11551]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Build a docker container from Dockerfile for kafka producer, which contains the API
```bash
docker build -t api-ingest .
```

Then run the container to get the API online:

```bash
sudo docker run --rm --network document-streaming-pipeline_default --name my-api-ingest -p 80:80 api-ingest
```

---

### Set up and deploy Kafka

Start up the Kafka container with the `docker-compose` command:

```bash
ubuntu@DESKTOP-QRVR3E3:~/document-streaming-pipeline$ sudo docker-compose -f docker-compose-kafka.yml up
[sudo] password for ubuntu: 
Creating network "document-streaming-pipeline_default" with the default driver
Pulling zookeeper (bitnami/zookeeper:latest)...
latest: Pulling from bitnami/zookeeper
fddf0a981f52: Pull complete
Digest: sha256:43f2ddb6f5ecedfb309e692567ff16e15b9a9561ce829ae3afc20fa47fbfb36c
Status: Downloaded newer image for bitnami/zookeeper:latest
Pulling kafka (bitnami/kafka:latest)...
latest: Pulling from bitnami/kafka
f9587821537a: Pull complete
Digest: sha256:906c5fcc74b923a40608e8ce86d2211402f7e13e8c37eaaa977e3e4a11ea1d73
Status: Downloaded newer image for bitnami/kafka:latest
Creating document-streaming-pipeline_zookeeper_1 ... done
Creating document-streaming-pipeline_kafka_1     ... done
```
#### Kafka and Zookeeper

Apache Zookeeper provides a highly reliable control plane for distributed coordination of clustered applications through a hierarchical key-value store. Zookeeper provides distributed configuration services, synchronization services, leadership election for the clusters, and keeps a registry for naming the clusters.

According to this blog from [OpenLogic](https://www.openlogic.com/blog/using-kafka-zookeeper#:~:text=In%20general%2C%20ZooKeeper%20provides%20an,consumer%20groups%20%2Cand%20individual%20offsets.), Kafka and ZooKeeper work in conjunction to form a complete Kafka Cluster ⁠— with ZooKeeper providing the aforementioned distributed clustering services, and Kafka handling the actual data streams and connectivity to clients.  

In general, ZooKeeper provides an in-sync view of the Kafka cluster. Kafka, on the other hand, is dedicated to handling the actual connections from the clients (producers and consumers) as well as managing the topic logs, topic log partitions, consumer groups ,and individual offsets.

```bash
zookeeper_1  | 2023-03-18 12:22:30,020 [myid:1] - INFO  [main:o.a.z.s.p.FileTxnSnapLog@124] - zookeeper.snapshot.trust.empty : false
zookeeper_1  | 2023-03-18 12:22:30,033 [myid:1] - INFO  [main:o.a.z.ZookeeperBanner@42] - 
zookeeper_1  | 2023-03-18 12:22:30,033 [myid:1] - INFO  [main:o.a.z.ZookeeperBanner@42] -   ______                  _                                          
zookeeper_1  | 2023-03-18 12:22:30,034 [myid:1] - INFO  [main:o.a.z.ZookeeperBanner@42] -  |___  /                 | |                                         
zookeeper_1  | 2023-03-18 12:22:30,034 [myid:1] - INFO  [main:o.a.z.ZookeeperBanner@42] -     / /    ___     ___   | | __   ___    ___   _ __     ___   _ __   
zookeeper_1  | 2023-03-18 12:22:30,034 [myid:1] - INFO  [main:o.a.z.ZookeeperBanner@42] -    / /    / _ \   / _ \  | |/ /  / _ \  / _ \ | '_ \   / _ \ | '__|
zookeeper_1  | 2023-03-18 12:22:30,034 [myid:1] - INFO  [main:o.a.z.ZookeeperBanner@42] -   / /__  | (_) | | (_) | |   <  |  __/ |  __/ | |_) | |  __/ | |    
zookeeper_1  | 2023-03-18 12:22:30,034 [myid:1] - INFO  [main:o.a.z.ZookeeperBanner@42] -  /_____|  \___/   \___/  |_|\_\  \___|  \___| | .__/   \___| |_|
zookeeper_1  | 2023-03-18 12:22:30,035 [myid:1] - INFO  [main:o.a.z.ZookeeperBanner@42] -                                               | |                     
zookeeper_1  | 2023-03-18 12:22:30,035 [myid:1] - INFO  [main:o.a.z.ZookeeperBanner@42] -                                               |_|                     
zookeeper_1  | 2023-03-18 12:22:30,035 [myid:1] - INFO  [main:o.a.z.ZookeeperBanner@42] - 
zookeeper_1  | 2023-03-18 12:22:30,037 [myid:1] - INFO  [main:o.a.z.Environment@98] - Server environment:zookeeper.version=3.8.1-74db005175a4ec545697012f9069cb9dcc8cdda7, 
```


---

### Test API connectivity using Insomnia

Testing API requests against Kafka message topic consumption
![image](https://github.com/ovokpus/document-streaming-pipeline/blob/main/img/testing-sparkoutput-consumption.png)

You need to have a way to test the data getting in through the API and buffered in Kafka, as pictured above. 


Login to the container terminal for kafka, and run commands similar to the following, which are given as examples:

```bash
# Create Kafka topics called ingestion-topic and spark-output
./kafka-topics.sh --create --topic ingestion-topic --bootstrap-server localhost:9092
./kafka-topics.sh --create --topic spark-output --bootstrap-server localhost:9092

# List Kafka topics within the container
./kafka-topics.sh --list --bootstrap-server localhost:9092

# Open local consumer of topics
./kafka-console-consumer.sh --topic ingestion-topic --bootstrap-server localhost:9092
./kafka-console-consumer.sh --topic spark-output --bootstrap-server localhost:9092

# Open local producer
./kafka-console-producer.sh --topic ingestion-topic --bootstrap-server localhost:9092
```

---

Example of output in container:
```bash
 *  Executing task: docker exec -it 361555a8762cccc0b4037e8240f2e7f7fbfb169a7182d5ddfcdb8f2cbd202252 bash 

source /home/ubuntu/document-streaming-pipeline/venv/bin/activate
I have no name!@361555a8762c:/$ source /home/ubuntu/document-streaming-pipeline/venv/bin/activate
bash: /home/ubuntu/document-streaming-pipeline/venv/bin/activate: No such file or directory
I have no name!@361555a8762c:/$ cd /opt/bitnami/kafka/bin
I have no name!@361555a8762c:/opt/bitnami/kafka/bin$ 
Created topic ingestiontopic.
I have no name!@361555a8762c:/opt/bitnami/kafka/bin$ ./kafka-topics.sh --list --bootstrap-server localhost:9092
ingestiontopic
I have no name!@361555a8762c:/opt/bitnami/kafka/bin$ ./kafka-console-consumer.sh --topic ingestiontopic --bootstrap-server localhost:9092
{"InvoiceNo": 536365, "StockCode": "85123A", "Description": "WHITE HANGING HEART T-LIGHT HOLDER", "Quantity": 6, "InvoiceDate": "12-02-2010 08:26:00", "UnitPrice": 2.55, "CustomerID": 17850, "Country": "United Kingdom"}
{"InvoiceNo": 536365, "StockCode": "85123A", "Description": "WHITE HANGING HEART T-LIGHT HOLDER", "Quantity": 6, "InvoiceDate": "12-02-2010 08:26:00", "UnitPrice": 2.55, "CustomerID": 17850, "Country": "United Kingdom"}
```
The output shows messages being consumed by a kafka consumer, as they are sent in through the producer via the API backend.

---

### Setup and Deploy Spark Structured Streaming

Deploy spark structured streaming by starting the spark container:

```bash
docker-compose -f docker-compose-kafka-spark.yml up
```

Spark UI Dashboards, viewable in port 4040
![image](https://github.com/ovokpus/document-streaming-pipeline/blob/main/img/spark-ui-01.png)

![image](https://github.com/ovokpus/document-streaming-pipeline/blob/main/img/spark-ui-01.png)

Spark Streaming from Ingestion topic
![image](https://github.com/ovokpus/document-streaming-pipeline/blob/main/img/spark-streaming-from-ingestiontopic.png)

Within the Spark notebook, there is a batch function that passes the data within the message and takes the value portion and inserts them as columns into the MongoDB collection, making them look like a structured table within the Mongo Express UI

### Deploy MongoDB and Mongo Express
Spin up the docker-compose command for the file that contains the docker configurations for MongoDB and Mongo Express:

`docker-compose.yaml`
```yaml
zookeeper:
...

kafka:
...

spark:
...

mongo:
    container_name: mongo-dev
    image: mongo
    volumes:
      - ~/dockerdata/mongodb:/data/db    
    restart: on-failure
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
      MONGO_INITDB_DATABASE: auth
    networks:
      - document-streaming

  mongo-express:
    image: mongo-express
    restart: on-failure
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_SERVER: mongo-dev
      ME_CONFIG_MONGODB_ADMINUSERNAME: root
      ME_CONFIG_MONGODB_ADMINPASSWORD: example
      ME_CONFIG_BASICAUTH_USERNAME: admin
      ME_CONFIG_BASICAUTH_PASSWORD: tribes
    networks:
      - document-streaming
    depends_on:
      - mongo

    networks:
document-streaming:
    driver: bridge
  
```
Mongo Express User Interface, showing the data parsed in with a spark notebook
![image](https://github.com/ovokpus/document-streaming-pipeline/blob/main/img/mongo-express-ui.png)

---

### Create Dashboard UI with Streamlit
Streamlit is an easy-to-use tool, developed in Python, and mainly used to share data and machine learning web applications. It allows us to create beautiful frontend applications for visualizing and presenting data, and lets us do that with only a few lines of code:

```python
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
```

Streamlit UI
![image](https://github.com/ovokpus/document-streaming-pipeline/blob/main/img/streamlit%20dashboard.png)

The above application can be fired up with this command:

```bash
streamlit run ./frontend/streamlit.py [ARGUMENTS]
```

## Ideas for improvement and tradeoffs
To take this project even further we can consider the following design ideas, keeping in mind the tradeoffs between value provided, project timelines, as well as cost of resources and technical complexity to be employed in building this pipeline.

1. Containerizing the streamlit application
2. Adding a delivery API to separate MongoDB and streamlit
3 Hosting the entire pipeline application in the public cloud