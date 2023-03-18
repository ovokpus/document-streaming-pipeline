from kafka import KafkaConsumer

def kafka_python_consumer():
    consumer = KafkaConsumer('ingestiontopic', bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print("Message Received: ", message.value)
    
print("Start consuming messages")

# start the consumer
kafka_python_consumer()

print("Done consuming messages")