# Business case: Document Streaming Pipeline

**Order events from an online store, streamed through Kafka and Spark into a live dashboard.**

## Who buys this

The buyer is the data or platform lead at an online retailer, or any business that emits a steady flow of JSON events (orders, clicks, device readings) and wants them visible within seconds instead of the next morning. The users are operations and merchandising staff watching the dashboard, and the engineers who run the pipeline.

## The problem and what it costs

Nightly batch reports mean the business finds out about a problem a day late: a product selling out, a spike in one country, a payment provider failing. Streaming fixes the delay, and Apache Kafka is the standard buffer for it. The Kafka project says more than 80% of Fortune 100 companies use it ([Apache Kafka](https://kafka.apache.org/)).

I found no reliable public figure for the cost of a day's reporting delay in retail, so this case doesn't claim one.

## How the repo solves it

| Need | What in the repo does it |
|---|---|
| Realistic event data | `client/transformer.py` turns the UK online-retail transactions dataset ([Kaggle / UCI](https://www.kaggle.com/datasets/carrie1/ecommerce-data)) into one JSON document per line. `client/api-client.py` posts them. |
| An ingestion endpoint | A FastAPI service in `api/` that validates the JSON and publishes to Kafka |
| A buffer that absorbs bursts | Apache Kafka (`docker-compose-kafka.yml`) |
| Continuous processing | Spark Structured Streaming reads from Kafka and writes to MongoDB (`ApacheSpark/` notebooks) |
| Storage and inspection | MongoDB, with Mongo Express |
| A live view | A Streamlit dashboard over MongoDB |

## Use-case scenarios

All of these organisations are fictional.

1. **An online gift retailer during the holiday peak.** Orders stream into the dashboard as they arrive. The merchandising team sees which stock codes are moving and restocks the same day.
2. **A customer-service lead** looks up one customer's invoices in MongoDB seconds after they are placed, instead of waiting for the nightly load.
3. **A marketplace adding a second consumer.** The fraud-screening service subscribes to the same Kafka topic, so a new use doesn't need a new integration.

## ROI: a worked model (illustrative)

These figures are **illustrative assumptions**.

| Input | Value | Basis |
|---|---|---|
| Stock-outs a year on fast-moving lines that same-day visibility would catch | 20 | Assumption |
| Gross margin lost per stock-out day | US$1,500 | Assumption |
| Days of stock-out avoided per caught event | 1 | Assumption |

Avoided loss: 20 × $1,500 × 1 = **US$30,000 a year**, against the cost of running Kafka, Spark and MongoDB (or their managed equivalents) and an engineer's time to operate them. For a small shop that may be a poor trade. The case gets stronger with event volume and with each additional consumer of the same stream.

## Path to production

1. Move from notebooks to a packaged, deployed Spark job with checkpointing.
2. Add a schema registry and dead-letter handling for malformed events.
3. Put the dashboard behind authentication, and add a delivery API between MongoDB and Streamlit, as the README itself suggests.
4. Consider managed Kafka and MongoDB to reduce operating load.

## Risks and limits

- **This is one of the weaker cases.** The repo is a learning project with notebooks and manual setup steps, and it has no tests. The architecture is standard and sound, but the code is a starting point.
- Streaming costs more to run than batch. Only use it where a delay of hours actually matters.
- The dataset is historical retail data from 2010 and 2011, replayed as a stream.

## Sources

- Apache Kafka project home page: https://kafka.apache.org/
- UK online retail dataset (Kaggle, from the UCI repository): https://www.kaggle.com/datasets/carrie1/ecommerce-data
