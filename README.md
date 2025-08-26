# Lime Mini Project – Streaming Data Pipeline  

Lime Intelligence provides Business Intelligence as a Service (BIaaS), enabling organisations to unlock insights quickly.  
To demonstrate my fit for the **Data Engineer role**, I built a **streaming data pipeline** that simulates real-time traffic sensor data ingestion, processing, and visualisation.  

---

## 🎯 Objective  
Simulate a real-time data engineering workflow:  
- Ingest events from a traffic dataset.  
- Stream them through **Pub/Sub** into **BigQuery**.  
- Provide dashboards with **real-time metrics and geospatial insights** in Looker Studio.  

---

## 📊 Data Source  
Dataset: `sensor_obs2008.csv.gz` (traffic sensor readings from San Diego).  
Each row contains:  

- **timestamp** – event timestamp  
- **latitude & longitude** – sensor location  
- **lane / direction / highway** – sensor metadata  
- **speed** – vehicle speed reading  

---

## ⚙️ Architecture  

1. **FastAPI / Cloud Run**  
   - Replays historical CSV file as streaming events.  
   - Adjustable `speedFactor` (e.g., `60` = compress 1 hour into 1 minute).  
   - Publishes events to **Pub/Sub**.  

2. **Pub/Sub**  
   - Serves as the messaging backbone.  
   - Each event enriched with `event_id`, `sensor_id`, and `location` as `POINT(lon lat)`.  

3. **BigQuery**  
   - Stores raw events in `trafficData.averageSpeeds`.  
   - A **view** is created using `ST_GEOGFROMTEXT(location)` for mapping.  

4. **Looker Studio**  
   - Real-time dashboards:  
     - **Map of sensor speeds** (colour coded: 50+ = Blue, 60+ = Yellow, 70+ = Red).  
     - **Time-series of average speeds by hour**.  

---

## 📝 Example Record  

```json
{
  "event_id": "250822052509874382",
  "timestamp": "2008-11-01 03:55:00",
  "sensor_id": 9066,
  "speed": 63.4,
  "location": "POINT(-117.21645 32.807319)"
}
```

---

## 🛠️ BigQuery View  

To visualise sensor locations on a map, a view was created to parse the `location` string into a proper GEOGRAPHY column:  

```sql
CREATE OR REPLACE VIEW `yourqm.trafficData.traffic_view` AS
SELECT
  event_id,
  TIMESTAMP(timestamp) AS ts,
  sensor_id,
  speed,
  ST_GEOGFROMTEXT(location) AS geo_point
FROM
  `yourqm.trafficData.averageSpeeds`;
  ```

---

## 📚 Key Learnings  

- Built an end-to-end streaming architecture in GCP (**Pub/Sub → BigQuery → Looker Studio**).  
- Applied **geospatial data types** in BigQuery for mapping.  
- Designed dashboards showing **real-time traffic insights**.  
- Added **data quality checks** (deduplication, schema validation).  

---

## 🚀 Next Steps  

- Extend pipeline with **Dataflow** for windowed aggregations.  
- Apply **SCD2 modelling** for evolving sensor metadata.  
- Deploy reusable **CI/CD infrastructure** with Terraform.  

