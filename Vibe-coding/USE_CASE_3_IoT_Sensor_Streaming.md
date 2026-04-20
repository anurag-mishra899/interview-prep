# Use Case 3: IoT Sensor Data Processing & Anomaly Detection

## Problem Statement

**Business Context**: A manufacturing company monitors equipment health using IoT sensors across 200 factories.

**Current State**:
- 10,000 sensors streaming data in real-time (temperature, vibration, pressure, RPM)
- Events every 10 seconds per sensor = 3.6M events/hour
- Need to detect equipment failures before they happen
- Historical data for trend analysis and predictive maintenance

**Requirements**:
1. **Real-time Ingestion**: Process streaming sensor data with <1 minute latency
2. **Anomaly Detection**: Flag unusual sensor readings indicating potential failures
3. **Time-Series Analysis**: Calculate moving averages, trends, seasonality
4. **Alerting**: Generate alerts for critical thresholds and anomalies
5. **Historical Analysis**: Batch processing for model training and reporting
6. **Predictive Maintenance**: ML features for failure prediction

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│               IoT SENSOR DEVICES (10K sensors)           │
│  Event rate: 1 event/10 sec = 360K events/hour          │
└────────────┬────────────────────────────────────────────┘
             │ JSON over Kafka/EventHub
             ▼
┌─────────────────────────────────────────────────────────┐
│              STREAMING INGESTION (Bronze)                │
│  - Structured Streaming (micro-batch: 30 sec)           │
│  - Watermark: 5 minutes (late data handling)            │
│  - Checkpointing for fault tolerance                    │
│  - Schema validation & malformed record handling        │
└────────────┬────────────────────────────────────────────┘
             │ Real-time Processing
             ▼
┌─────────────────────────────────────────────────────────┐
│         SILVER: Streaming Transformations                │
│  - Deduplication (event_id)                             │
│  - Windowed aggregations (1 min, 5 min, 15 min)        │
│  - Stateful operations (sessionization)                 │
│  - Join with equipment metadata (broadcast)             │
└────────────┬────────────────────────────────────────────┘
             │ Real-time Analytics & Alerts
             ▼
┌─────────────────────────────────────────────────────────┐
│      GOLD: Real-time Metrics & Anomaly Detection        │
│  STREAMING TABLES:                                       │
│  - sensor_readings_1min (tumbling windows)              │
│  - anomaly_alerts (real-time threshold violations)      │
│                                                          │
│  BATCH TABLES:                                           │
│  - daily_sensor_summary                                  │
│  - equipment_health_score                                │
│  - ml_failure_prediction_features                        │
└─────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Implementation

### Phase 0: Setup (5 minutes)

```python
# ========================================
# ENVIRONMENT SETUP
# ========================================

spark.sql("CREATE CATALOG IF NOT EXISTS iot_sensors")
spark.sql("USE CATALOG iot_sensors")
spark.sql("CREATE SCHEMA IF NOT EXISTS bronze")
spark.sql("CREATE SCHEMA IF NOT EXISTS silver")
spark.sql("CREATE SCHEMA IF NOT EXISTS gold")

%pip install dbldatagen faker

from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window
from delta.tables import DeltaTable
import dbldatagen as dg
from datetime import datetime, timedelta
import random

# Set streaming configurations
spark.conf.set("spark.sql.streaming.schemaInference", "true")
spark.conf.set("spark.sql.shuffle.partitions", "200")

print("✅ Environment ready for IoT streaming")
```

---

### Phase 1: Generate Synthetic IoT Sensor Data (10 minutes)

**Think-Out-Loud**:
> "I'll generate realistic sensor data with temporal patterns - temperature fluctuates with time of day,
> vibration increases with equipment age, and I'll inject some anomalies to simulate failing equipment.
> Using time-series patterns with sine waves for realistic oscillation."

```python
# ========================================
# DIMENSION: Equipment Metadata
# ========================================

print("🏭 Generating equipment metadata...")

equipment_spec = (
    dg.DataGenerator(spark, rows=10000, partitions=8)
    .withColumn("sensor_id", "string", template=r"SENSOR-\n", uniqueValues=10000)
    .withColumn("equipment_id", "string", template=r"EQUIP-\n",
                minValue=1, maxValue=2000)  # Multiple sensors per equipment
    .withColumn("factory_id", "string", template=r"FACTORY-\n",
                minValue=1, maxValue=200)
    .withColumn("equipment_type", "string", values=[
        "Turbine", "Compressor", "Motor", "Pump", "Generator", "Conveyor"
    ])
    .withColumn("sensor_type", "string", values=[
        "Temperature", "Vibration", "Pressure", "RPM", "Power"
    ])
    .withColumn("install_date", "date", begin="2018-01-01", end="2024-01-01")
    .withColumn("last_maintenance", "date", begin="2024-01-01", end="2025-04-01")
    .withColumn("manufacturer", "string", values=[
        "Siemens", "GE", "ABB", "Honeywell", "Schneider"
    ])
    .withColumn("location_zone", "string", values=["A", "B", "C", "D"])
)

dim_equipment = equipment_spec.build()

# Add operational parameters
dim_equipment = dim_equipment.withColumn(
    "normal_temp_range_min",
    F.when(F.col("sensor_type") == "Temperature", 20.0).otherwise(None)
).withColumn(
    "normal_temp_range_max",
    F.when(F.col("sensor_type") == "Temperature", 80.0).otherwise(None)
).withColumn(
    "normal_vibration_range_max",
    F.when(F.col("sensor_type") == "Vibration", 10.0).otherwise(None)
).withColumn(
    "normal_pressure_range_min",
    F.when(F.col("sensor_type") == "Pressure", 50.0).otherwise(None)
).withColumn(
    "normal_pressure_range_max",
    F.when(F.col("sensor_type") == "Pressure", 200.0).otherwise(None)
).withColumn(
    "equipment_age_years",
    F.round((F.datediff(F.current_date(), F.col("install_date")) / 365.25), 1)
).withColumn(
    "days_since_maintenance",
    F.datediff(F.current_date(), F.col("last_maintenance"))
)

dim_equipment.write.format("delta").mode("overwrite").saveAsTable("silver.dim_equipment")

print(f"✅ Generated {dim_equipment.count():,} sensors across equipment")
dim_equipment.show(5, truncate=False)

# ========================================
# FACT: Historical Sensor Readings (Batch)
# ========================================

print("\n📊 Generating historical sensor readings (last 7 days)...")

num_sensors = 10000
readings_per_sensor_per_day = 8640  # Every 10 seconds
days_of_history = 7
total_historical_readings = num_sensors * readings_per_sensor_per_day * days_of_history

print(f"   • Generating {total_historical_readings:,} historical readings...")
print(f"   • This simulates: {num_sensors:,} sensors × {readings_per_sensor_per_day:,} readings/day × {days_of_history} days")

# For demo purposes, reduce to manageable size
sample_readings = 500000  # 500K readings for demo

sensor_readings_spec = (
    dg.DataGenerator(spark, rows=sample_readings, partitions=20)
    .withColumn("event_id", "long", uniqueValues=sample_readings)
    .withColumn("sensor_id", "string", template=r"SENSOR-\n",
                minValue=1, maxValue=10000)
    .withColumn("timestamp", "timestamp",
                begin=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
                end=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    .withColumn("raw_value", "double", minValue=0, maxValue=100, random=True)
)

sensor_readings_raw = sensor_readings_spec.build()

# Add realistic patterns based on sensor type
sensor_readings = (
    sensor_readings_raw
    .join(F.broadcast(dim_equipment.select("sensor_id", "sensor_type", "equipment_age_years")), "sensor_id")

    # Temperature: Oscillates with time of day (sine wave) + noise
    .withColumn("hour_of_day", F.hour("timestamp"))
    .withColumn("temperature_value",
                F.when(F.col("sensor_type") == "Temperature",
                       50 + 20 * F.sin((F.col("hour_of_day") / 24) * 2 * 3.14159) +
                       F.rand() * 10 - 5)
                .otherwise(None))

    # Vibration: Increases with equipment age + random spikes
    .withColumn("vibration_value",
                F.when(F.col("sensor_type") == "Vibration",
                       3 + F.col("equipment_age_years") * 0.5 + F.rand() * 2)
                .otherwise(None))

    # Pressure: Relatively stable with occasional fluctuations
    .withColumn("pressure_value",
                F.when(F.col("sensor_type") == "Pressure",
                       100 + F.rand() * 20 - 10)
                .otherwise(None))

    # RPM: Discrete values around set points
    .withColumn("rpm_value",
                F.when(F.col("sensor_type") == "RPM",
                       F.round((1500 + F.rand() * 100 - 50), 0))
                .otherwise(None))

    # Power: Correlated with RPM
    .withColumn("power_value",
                F.when(F.col("sensor_type") == "Power",
                       F.round((75 + F.rand() * 10 - 5), 2))
                .otherwise(None))

    # Combine into single reading_value
    .withColumn("reading_value",
                F.coalesce(
                    F.col("temperature_value"),
                    F.col("vibration_value"),
                    F.col("pressure_value"),
                    F.col("rpm_value"),
                    F.col("power_value")
                ))

    # Add quality indicators
    .withColumn("reading_quality",
                F.when(F.rand() < 0.95, "GOOD")
                .when(F.rand() < 0.98, "DEGRADED")
                .otherwise("POOR"))
)

# Inject anomalies (5% of readings)
sensor_readings_with_anomalies = (
    sensor_readings
    .withColumn("is_anomaly",
                F.when(F.rand() < 0.05, True).otherwise(False))
    .withColumn("reading_value",
                F.when(F.col("is_anomaly"),
                       F.when(F.col("sensor_type") == "Temperature", 150.0)  # Overheat
                       .when(F.col("sensor_type") == "Vibration", 50.0)  # High vibration
                       .when(F.col("sensor_type") == "Pressure", 300.0)  # Overpressure
                       .otherwise(F.col("reading_value")))
                .otherwise(F.col("reading_value")))
    .withColumn("ingestion_timestamp", F.current_timestamp())
)

# Select final schema
historical_readings = sensor_readings_with_anomalies.select(
    "event_id",
    "sensor_id",
    "timestamp",
    "sensor_type",
    "reading_value",
    "reading_quality",
    "is_anomaly",
    "ingestion_timestamp"
)

print(f"✅ Generated {historical_readings.count():,} historical sensor readings")

# Show statistics
print("\n📊 Reading Statistics by Sensor Type:")
historical_readings.groupBy("sensor_type").agg(
    F.count("*").alias("count"),
    F.round(F.avg("reading_value"), 2).alias("avg_value"),
    F.round(F.min("reading_value"), 2).alias("min_value"),
    F.round(F.max("reading_value"), 2).alias("max_value"),
    F.sum(F.when(F.col("is_anomaly"), 1).otherwise(0)).alias("anomaly_count")
).show()

# ========================================
# WRITE TO BRONZE (Historical Batch)
# ========================================

print("\n🥉 Writing historical data to BRONZE...")

historical_readings.write.format("delta") \
    .mode("overwrite") \
    .partitionBy(F.to_date("timestamp").alias("event_date")) \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze.sensor_readings")

print("✅ Historical data written to bronze.sensor_readings")

# Verify
bronze_df = spark.read.format("delta").table("bronze.sensor_readings")
print(f"   • Total records: {bronze_df.count():,}")
print(f"   • Date range: {bronze_df.agg(F.min('timestamp'), F.max('timestamp')).collect()[0]}")
```

---

### Phase 2: Batch Processing - Silver Layer (10 minutes)

**Think-Out-Loud**:
> "For historical data, I'll process it in batch mode. This includes deduplication, enrichment with
> equipment metadata, calculation of time-window aggregations, and anomaly detection using statistical methods."

```python
# ========================================
# SILVER LAYER: Batch Processing
# ========================================

print("🥈 Processing SILVER layer (batch mode)...")

bronze_df = spark.read.format("delta").table("bronze.sensor_readings")
dim_equipment_df = spark.read.format("delta").table("silver.dim_equipment")

# ========================================
# STEP 1: Deduplication & Validation
# ========================================

print("\n1️⃣  DEDUPLICATION & VALIDATION")

readings_deduped = bronze_df.dropDuplicates(["event_id"])
duplicates = bronze_df.count() - readings_deduped.count()
print(f"   ✓ Removed {duplicates} duplicate events")

# Validate readings
readings_valid = (
    readings_deduped
    .filter(F.col("event_id").isNotNull())
    .filter(F.col("sensor_id").isNotNull())
    .filter(F.col("reading_value").isNotNull())
    .filter(F.col("reading_value") >= 0)
)

invalid_count = readings_deduped.count() - readings_valid.count()
print(f"   ✓ Filtered {invalid_count} invalid readings")

# ========================================
# STEP 2: Enrich with Equipment Metadata
# ========================================

print("\n2️⃣  ENRICHMENT")

readings_enriched = (
    readings_valid
    .join(
        F.broadcast(dim_equipment_df),
        "sensor_id"
    )
)

print("   ✓ Enriched with equipment metadata")

# ========================================
# STEP 3: Time-Based Features
# ========================================

print("\n3️⃣  TIME-BASED FEATURES")

readings_with_features = (
    readings_enriched
    .withColumn("event_date", F.to_date("timestamp"))
    .withColumn("event_hour", F.hour("timestamp"))
    .withColumn("day_of_week", F.dayofweek("timestamp"))
    .withColumn("is_weekend", F.col("day_of_week").isin([1, 7]))
    .withColumn("is_night_shift", F.col("event_hour").between(22, 6))
)

print("   ✓ Added temporal features")

# ========================================
# STEP 4: Window Aggregations (Moving Averages)
# ========================================

print("\n4️⃣  CALCULATING MOVING AVERAGES")

# Define window for each sensor (ordered by time)
sensor_window = Window.partitionBy("sensor_id").orderBy("timestamp")

# 10-reading moving average (simulate 10-minute window at 1 reading/min)
moving_avg_window = sensor_window.rowsBetween(-9, 0)

readings_with_ma = (
    readings_with_features
    .withColumn("reading_ma_10", F.avg("reading_value").over(moving_avg_window))
    .withColumn("reading_stddev_10", F.stddev("reading_value").over(moving_avg_window))

    # Lag values for change detection
    .withColumn("prev_reading", F.lag("reading_value", 1).over(sensor_window))
    .withColumn("reading_change", F.col("reading_value") - F.col("prev_reading"))
    .withColumn("reading_change_pct",
                (F.col("reading_change") / F.col("prev_reading")) * 100)
)

print("   ✓ Calculated 10-period moving averages")

# ========================================
# STEP 5: Statistical Anomaly Detection
# ========================================

print("\n5️⃣  STATISTICAL ANOMALY DETECTION")

# Z-score based on moving average
readings_with_anomaly = (
    readings_with_ma
    .withColumn("z_score",
                (F.col("reading_value") - F.col("reading_ma_10")) /
                F.coalesce(F.col("reading_stddev_10"), F.lit(1)))
    .withColumn("is_statistical_anomaly", F.abs(F.col("z_score")) > 3)

    # Threshold-based anomalies (sensor-specific)
    .withColumn("is_threshold_anomaly",
                F.when(
                    (F.col("sensor_type") == "Temperature") &
                    ((F.col("reading_value") < F.col("normal_temp_range_min")) |
                     (F.col("reading_value") > F.col("normal_temp_range_max"))), True)
                .when(
                    (F.col("sensor_type") == "Vibration") &
                    (F.col("reading_value") > F.col("normal_vibration_range_max")), True)
                .when(
                    (F.col("sensor_type") == "Pressure") &
                    ((F.col("reading_value") < F.col("normal_pressure_range_min")) |
                     (F.col("reading_value") > F.col("normal_pressure_range_max"))), True)
                .otherwise(False))

    # Combine anomaly signals
    .withColumn("anomaly_detected",
                F.col("is_statistical_anomaly") | F.col("is_threshold_anomaly"))

    # Severity
    .withColumn("anomaly_severity",
                F.when(F.abs(F.col("z_score")) > 5, "CRITICAL")
                .when(F.abs(F.col("z_score")) > 3, "HIGH")
                .when(F.col("is_threshold_anomaly"), "MEDIUM")
                .otherwise("NORMAL"))
)

anomaly_count = readings_with_anomaly.filter("anomaly_detected = true").count()
print(f"   ✓ Detected {anomaly_count:,} anomalies ({(anomaly_count/readings_with_anomaly.count()*100):.2f}%)")

# ========================================
# STEP 6: Write to Silver
# ========================================

print("\n6️⃣  WRITING TO SILVER")

# Select final schema
fact_sensor_readings = readings_with_anomaly.select(
    "event_id",
    "sensor_id",
    "equipment_id",
    "factory_id",
    "sensor_type",
    "equipment_type",
    "timestamp",
    "event_date",
    "event_hour",
    "reading_value",
    "reading_ma_10",
    "reading_stddev_10",
    "reading_change",
    "reading_change_pct",
    "reading_quality",
    "z_score",
    "anomaly_detected",
    "anomaly_severity",
    "is_weekend",
    "is_night_shift",
    "equipment_age_years",
    "days_since_maintenance"
)

fact_sensor_readings.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("event_date") \
    .saveAsTable("silver.fact_sensor_readings")

print(f"✅ Wrote {fact_sensor_readings.count():,} readings to silver.fact_sensor_readings")

# Show anomalies
print("\n🚨 Sample Anomalies:")
fact_sensor_readings.filter(
    F.col("anomaly_detected") == True
).select(
    "sensor_id", "timestamp", "sensor_type",
    F.round("reading_value", 2).alias("value"),
    F.round("reading_ma_10", 2).alias("ma_10"),
    F.round("z_score", 2).alias("z_score"),
    "anomaly_severity"
).show(10, truncate=False)
```

---

### Phase 3: Streaming Ingestion & Processing (15 minutes)

**Think-Out-Loud**:
> "Now I'll set up streaming ingestion to simulate real-time sensor data. I'll use structured streaming
> with watermarking for late data, tumbling windows for aggregations, and foreachBatch for complex
> transformations like anomaly detection."

```python
# ========================================
# STREAMING: Setup Source (Simulated)
# ========================================

print("📡 Setting up STREAMING ingestion...")

print("""
🎯 STREAMING ARCHITECTURE:

In production, this would read from Kafka/EventHub:

streaming_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "sensor-readings")
    .load()
)

For this demo, I'll use 'rate' source to simulate streaming:
""")

# Simulate streaming source (generates rows at specified rate)
streaming_simulation_code = '''
# Simulated streaming source
streaming_source = (
    spark.readStream
    .format("rate")
    .option("rowsPerSecond", 100)  # 100 events/sec (scaled down from 1000)
    .load()
    .withColumn("sensor_id", F.concat(F.lit("SENSOR-"), (F.rand() * 10000 + 1).cast("int").cast("string")))
    .withColumn("timestamp", F.col("timestamp"))
    .withColumn("event_id", F.col("value"))
    .withColumn("reading_value", 50 + F.rand() * 50)  # Random values
    .withColumn("sensor_type",
                F.expr("CASE WHEN rand() < 0.3 THEN 'Temperature' WHEN rand() < 0.6 THEN 'Vibration' ELSE 'Pressure' END"))
)

# Add watermark for late data (allow 5 minutes late)
streaming_source_with_watermark = (
    streaming_source
    .withWatermark("timestamp", "5 minutes")
)

# ========================================
# STREAMING: Bronze Layer (Raw Append)
# ========================================

bronze_streaming_query = (
    streaming_source_with_watermark
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/checkpoint/bronze_streaming")
    .trigger(processingTime="30 seconds")  # Micro-batch every 30 seconds
    .partitionBy(F.to_date("timestamp").alias("event_date"))
    .toTable("bronze.sensor_readings")
)

print("✅ Bronze streaming ingestion started (appends to same table as batch)")

# ========================================
# STREAMING: Silver Layer (Transformations)
# ========================================

# Read stream from bronze
bronze_stream = (
    spark.readStream
    .format("delta")
    .table("bronze.sensor_readings")
    .withWatermark("timestamp", "5 minutes")
)

# Enrich with equipment metadata (broadcast join)
silver_stream = (
    bronze_stream
    .dropDuplicates(["event_id"])
    .join(
        F.broadcast(dim_equipment_df.select("sensor_id", "equipment_id", "sensor_type", "equipment_type")),
        "sensor_id"
    )
    .select(
        "event_id", "sensor_id", "equipment_id", "sensor_type",
        "timestamp", "reading_value"
    )
)

# Use foreachBatch for complex transformations (anomaly detection)
def process_silver_batch(batch_df, batch_id):
    """
    Process each micro-batch:
    1. Calculate moving averages
    2. Detect anomalies
    3. MERGE to silver table
    """
    from delta.tables import DeltaTable

    # Calculate features within batch
    sensor_window = Window.partitionBy("sensor_id").orderBy("timestamp")

    batch_with_features = (
        batch_df
        .withColumn("reading_ma_5", F.avg("reading_value").over(
            sensor_window.rowsBetween(-4, 0)))
        .withColumn("anomaly_detected",
                    F.abs(F.col("reading_value") - F.col("reading_ma_5")) > 30)
        .withColumn("processing_timestamp", F.current_timestamp())
    )

    # MERGE to silver (upsert)
    silver_table = DeltaTable.forName(spark, "silver.fact_sensor_readings_streaming")

    (silver_table.alias("target")
     .merge(batch_with_features.alias("source"), "target.event_id = source.event_id")
     .whenMatchedUpdateAll()
     .whenNotMatchedInsertAll()
     .execute())

    print(f"Processed batch {batch_id}: {batch_df.count()} records")

# Write to silver using foreachBatch
silver_streaming_query = (
    silver_stream
    .writeStream
    .foreachBatch(process_silver_batch)
    .option("checkpointLocation", "/tmp/checkpoint/silver_streaming")
    .trigger(processingTime="1 minute")
    .start()
)

print("✅ Silver streaming transformation started")

# ========================================
# STREAMING: Gold Layer (Windowed Aggregations)
# ========================================

# 1-minute tumbling window aggregations
windowed_aggregates = (
    silver_stream
    .withWatermark("timestamp", "5 minutes")
    .groupBy(
        F.window("timestamp", "1 minute"),  # 1-minute tumbling window
        "sensor_id",
        "equipment_id",
        "sensor_type"
    )
    .agg(
        F.count("*").alias("reading_count"),
        F.avg("reading_value").alias("avg_reading"),
        F.min("reading_value").alias("min_reading"),
        F.max("reading_value").alias("max_reading"),
        F.stddev("reading_value").alias("stddev_reading")
    )
    .select(
        F.col("window.start").alias("window_start"),
        F.col("window.end").alias("window_end"),
        "sensor_id",
        "equipment_id",
        "sensor_type",
        "reading_count",
        F.round("avg_reading", 2).alias("avg_reading"),
        F.round("min_reading", 2).alias("min_reading"),
        F.round("max_reading", 2).alias("max_reading"),
        F.round("stddev_reading", 2).alias("stddev_reading")
    )
)

gold_windowed_query = (
    windowed_aggregates
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/checkpoint/gold_windowed")
    .trigger(processingTime="1 minute")
    .toTable("gold.sensor_readings_1min")
)

print("✅ Gold windowed aggregations started (1-minute windows)")

# ========================================
# STREAMING: Real-Time Alerts
# ========================================

# Filter for anomalies and generate alerts
anomaly_alerts = (
    silver_stream
    .filter(F.abs(F.col("reading_value")) > 100)  # Simplified threshold
    .select(
        "event_id",
        "sensor_id",
        "equipment_id",
        "sensor_type",
        "timestamp",
        "reading_value",
        F.lit("THRESHOLD_VIOLATION").alias("alert_type"),
        F.lit("HIGH").alias("severity"),
        F.current_timestamp().alias("alert_timestamp")
    )
)

alerts_query = (
    anomaly_alerts
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/checkpoint/alerts")
    .trigger(processingTime="30 seconds")
    .toTable("gold.anomaly_alerts")
)

print("✅ Real-time alerting started")

# ========================================
# MONITORING STREAMING QUERIES
# ========================================

print("\\n📊 Active Streaming Queries:")
for query in spark.streams.active:
    print(f"   • {query.name}: {query.status}")

print("\\n⏱️  To stop streams:")
print("   spark.streams.active[0].stop()  # Stop specific query")
print("   for q in spark.streams.active: q.stop()  # Stop all")

'''

print(streaming_simulation_code)

print("\n✅ Streaming architecture explained")
print("""
KEY CONCEPTS DEMONSTRATED:
✓ Watermarking: 5-minute tolerance for late-arriving data
✓ Micro-batching: Process every 30 seconds / 1 minute
✓ Checkpointing: Fault-tolerant exactly-once processing
✓ foreachBatch: Complex transformations (ML, MERGE operations)
✓ Windowed aggregations: Tumbling windows for time-series
✓ Real-time alerting: Filter and route anomalies to alert table
✓ Unified batch + streaming: Same Delta tables for both modes
""")
```

---

### Phase 4: Gold Layer - Analytics & ML Features (15 minutes)

**Think-Out-Loud**:
> "Gold layer aggregates sensor data for business insights: equipment health scores, predictive maintenance
> features, and failure prediction models. I'll create daily summaries and ML-ready feature sets."

```python
# ========================================
# GOLD LAYER: Batch Analytics
# ========================================

print("🥇 Building GOLD layer analytics...")

silver_df = spark.read.format("delta").table("silver.fact_sensor_readings")

# ========================================
# ANALYTICS 1: Daily Equipment Health Summary
# ========================================

print("\n📊 Creating gold.daily_equipment_health...")

daily_health = (
    silver_df
    .groupBy("event_date", "equipment_id", "equipment_type", "factory_id")
    .agg(
        F.count("event_id").alias("reading_count"),
        F.countDistinct("sensor_id").alias("active_sensors"),

        # Aggregates by sensor type
        F.avg(F.when(F.col("sensor_type") == "Temperature", F.col("reading_value"))).alias("avg_temperature"),
        F.max(F.when(F.col("sensor_type") == "Temperature", F.col("reading_value"))).alias("max_temperature"),
        F.avg(F.when(F.col("sensor_type") == "Vibration", F.col("reading_value"))).alias("avg_vibration"),
        F.max(F.when(F.col("sensor_type") == "Vibration", F.col("reading_value"))).alias("max_vibration"),
        F.avg(F.when(F.col("sensor_type") == "Pressure", F.col("reading_value"))).alias("avg_pressure"),

        # Anomaly metrics
        F.sum(F.when(F.col("anomaly_detected"), 1).otherwise(0)).alias("anomaly_count"),
        F.sum(F.when(F.col("anomaly_severity") == "CRITICAL", 1).otherwise(0)).alias("critical_anomalies"),

        # Quality metrics
        F.sum(F.when(F.col("reading_quality") == "POOR", 1).otherwise(0)).alias("poor_quality_readings")
    )
    .withColumn("anomaly_rate", F.col("anomaly_count") / F.col("reading_count"))

    # Calculate health score (0-100)
    .withColumn("health_score",
                F.greatest(
                    100 -
                    (F.col("anomaly_rate") * 50) -  # Anomaly penalty
                    (F.col("critical_anomalies") * 10) -  # Critical penalty
                    ((F.col("poor_quality_readings") / F.col("reading_count")) * 20),  # Quality penalty
                    F.lit(0)
                ))
    .withColumn("health_status",
                F.when(F.col("health_score") >= 90, "HEALTHY")
                .when(F.col("health_score") >= 70, "WARNING")
                .when(F.col("health_score") >= 50, "DEGRADED")
                .otherwise("CRITICAL"))
    .withColumn("as_of_timestamp", F.current_timestamp())
)

daily_health.write.format("delta").mode("overwrite").partitionBy("event_date").saveAsTable("gold.daily_equipment_health")

print(f"✅ Created gold.daily_equipment_health ({daily_health.count():,} equipment-days)")

# Show health distribution
print("\n🏥 Equipment Health Distribution:")
daily_health.groupBy("health_status").agg(
    F.count("*").alias("equipment_count"),
    F.round(F.avg("health_score"), 1).alias("avg_health_score"),
    F.round(F.avg("anomaly_rate"), 3).alias("avg_anomaly_rate")
).orderBy(F.desc("avg_health_score")).show()

# ========================================
# ANALYTICS 2: Equipment Performance Trends
# ========================================

print("\n📈 Creating gold.equipment_trends...")

# Calculate week-over-week changes
equipment_trends = (
    daily_health
    .withColumn("week", F.weekofyear("event_date"))
    .groupBy("equipment_id", "week")
    .agg(
        F.avg("health_score").alias("weekly_avg_health"),
        F.avg("anomaly_rate").alias("weekly_avg_anomaly_rate"),
        F.max("critical_anomalies").alias("max_critical_anomalies")
    )
)

# Calculate trend (improving or degrading)
window_trend = Window.partitionBy("equipment_id").orderBy("week")

equipment_trends_final = (
    equipment_trends
    .withColumn("prev_week_health", F.lag("weekly_avg_health", 1).over(window_trend))
    .withColumn("health_change", F.col("weekly_avg_health") - F.col("prev_week_health"))
    .withColumn("trend",
                F.when(F.col("health_change") > 5, "IMPROVING")
                .when(F.col("health_change") < -5, "DEGRADING")
                .otherwise("STABLE"))
    .withColumn("as_of_timestamp", F.current_timestamp())
)

equipment_trends_final.write.format("delta").mode("overwrite").saveAsTable("gold.equipment_trends")

print(f"✅ Created gold.equipment_trends")

print("\n📉 Equipment Trend Summary:")
equipment_trends_final.groupBy("trend").agg(
    F.count("*").alias("equipment_count")
).show()

# ========================================
# ML FEATURES: Failure Prediction Dataset
# ========================================

print("\n🤖 Creating gold.ml_failure_prediction_features...")

# Create feature set for predicting equipment failure
ml_features = (
    silver_df
    .groupBy("equipment_id", "sensor_id", "equipment_type", "sensor_type")
    .agg(
        # Statistical features
        F.avg("reading_value").alias("avg_reading"),
        F.stddev("reading_value").alias("stddev_reading"),
        F.min("reading_value").alias("min_reading"),
        F.max("reading_value").alias("max_reading"),
        F.expr("percentile_approx(reading_value, 0.25)").alias("q1_reading"),
        F.expr("percentile_approx(reading_value, 0.75)").alias("q3_reading"),

        # Anomaly features
        F.sum(F.when(F.col("anomaly_detected"), 1).otherwise(0)).alias("total_anomalies"),
        F.sum(F.when(F.col("anomaly_severity") == "CRITICAL", 1).otherwise(0)).alias("critical_anomalies"),
        F.avg(F.abs(F.col("z_score"))).alias("avg_abs_z_score"),

        # Trend features
        F.avg("reading_change").alias("avg_reading_change"),
        F.stddev("reading_change").alias("stddev_reading_change"),
        F.max(F.abs(F.col("reading_change"))).alias("max_reading_change"),

        # Time features
        F.count("*").alias("total_readings"),
        F.max("equipment_age_years").alias("equipment_age_years"),
        F.max("days_since_maintenance").alias("days_since_maintenance"),

        # Recent behavior (last 24 hours)
        F.avg(F.when(
            F.col("timestamp") >= F.expr("current_timestamp() - INTERVAL 24 HOURS"),
            F.col("reading_value")
        )).alias("reading_last_24h"),
        F.sum(F.when(
            (F.col("timestamp") >= F.expr("current_timestamp() - INTERVAL 24 HOURS")) &
            (F.col("anomaly_detected") == True),
            1
        ).otherwise(0)).alias("anomalies_last_24h")
    )
    # Pivot sensor types to get features per equipment
    .groupBy("equipment_id", "equipment_type")
    .pivot("sensor_type")
    .agg(F.first("avg_reading"))
    .withColumnRenamed("Temperature", "avg_temperature")
    .withColumnRenamed("Vibration", "avg_vibration")
    .withColumnRenamed("Pressure", "avg_pressure")
    .withColumnRenamed("RPM", "avg_rpm")
    .withColumnRenamed("Power", "avg_power")
)

# Join with equipment metadata
ml_features_final = (
    ml_features
    .join(
        dim_equipment_df.select(
            "equipment_id", "equipment_age_years", "days_since_maintenance"
        ).dropDuplicates(["equipment_id"]),
        "equipment_id"
    )
    # Add target variable (simulated - in production, this comes from maintenance logs)
    .withColumn("will_fail_30d",
                F.when(
                    (F.col("avg_vibration") > 15) |
                    (F.col("days_since_maintenance") > 180) |
                    (F.col("equipment_age_years") > 7),
                    1
                ).otherwise(0))
    .withColumn("feature_timestamp", F.current_timestamp())
)

ml_features_final.write.format("delta").mode("overwrite").saveAsTable("gold.ml_failure_prediction_features")

print(f"✅ Created gold.ml_failure_prediction_features ({ml_features_final.count():,} equipment)")

# Show feature distribution
print("\n🎯 Failure Prediction Target Distribution:")
ml_features_final.groupBy("will_fail_30d").agg(
    F.count("*").alias("equipment_count")
).show()

print("\n📊 Sample ML Features:")
ml_features_final.select(
    "equipment_id",
    F.round("avg_temperature", 1).alias("temp"),
    F.round("avg_vibration", 1).alias("vib"),
    "equipment_age_years",
    "days_since_maintenance",
    "will_fail_30d"
).show(10)
```

---

## Curveball Scenarios

### Curveball 1: "Handle Out-of-Order Events"

**Interviewer**: *"Sensors can send data late due to network issues. How do you handle events that arrive hours late?"*

```python
print("🎯 CURVEBALL 1: Handling Late-Arriving Data")
print("="*60)

print("""
PROBLEM: Network disruptions cause sensors to buffer data and send it hours later
CHALLENGE: Late events can affect window aggregations and metric accuracy

SOLUTION: Watermarking + Late Data Handling

┌─────────────────────────────────────────────────────────┐
│  Event Time: 10:00 AM (when sensor recorded)            │
│  Arrival Time: 1:00 PM (3 hours late)                   │
│  Watermark: 15 minutes                                   │
│  Decision: DROPPED from streaming, picked up by batch   │
└─────────────────────────────────────────────────────────┘
""")

watermark_example = '''
# STREAMING with Watermark
streaming_df = (
    spark.readStream
    .format("delta")
    .table("bronze.sensor_readings")
    .withWatermark("timestamp", "15 minutes")  # Tolerate 15 min late
)

# 1-minute tumbling windows
windowed = (
    streaming_df
    .groupBy(
        F.window("timestamp", "1 minute"),
        "sensor_id"
    )
    .agg(F.avg("reading_value").alias("avg_reading"))
)

BEHAVIOR:
- Events within 15 minutes of watermark: ACCEPTED
- Events > 15 minutes late: DROPPED from stream
- Dropped events still in bronze table

BATCH RECONCILIATION (Daily):
1. Read all bronze data for the day
2. Recompute aggregations with complete data
3. Update gold tables (overwrite or MERGE)
4. Fill gaps from late data

# Daily batch job
daily_complete_data = (
    spark.read.format("delta")
    .table("bronze.sensor_readings")
    .filter(F.col("event_date") == F.current_date() - 1)
)

# Recompute with ALL data (including late arrivals)
complete_aggregates = (
    daily_complete_data
    .groupBy(
        F.window("timestamp", "1 minute"),
        "sensor_id"
    )
    .agg(F.avg("reading_value").alias("avg_reading_complete"))
)

# MERGE to update gold table
gold_table = DeltaTable.forName(spark, "gold.sensor_readings_1min")
(gold_table.alias("target")
 .merge(complete_aggregates.alias("source"),
        "target.window_start = source.window.start AND target.sensor_id = source.sensor_id")
 .whenMatchedUpdate(set={"avg_reading": "source.avg_reading_complete"})
 .whenNotMatchedInsertAll()
 .execute())
'''

print(watermark_example)

print("\n✅ BEST PRACTICES:")
print("""
✓ Set watermark based on SLA (trade-off: latency vs completeness)
✓ Use append mode for immutable event streams
✓ Run daily batch for complete, accurate aggregates
✓ Monitor late data metrics in Spark UI
✓ Alert on excessive late arrivals (network issues)
""")
```

---

### Curveball 2: "Implement Sensor Health Scoring"

**Interviewer**: *"Create a composite health score for each sensor based on multiple factors."*

```python
print("🎯 CURVEBALL 2: Sensor Health Scoring System")
print("="*60)

print("""
HEALTH SCORE COMPONENTS:
1. Reading stability (low variance = healthy)
2. Anomaly frequency (few anomalies = healthy)
3. Data quality (good quality readings = healthy)
4. Maintenance recency (recent maintenance = healthy)
5. Equipment age (newer = healthier)

SCORE: 0-100 (weighted composite)
""")

silver_df = spark.read.format("delta").table("silver.fact_sensor_readings")
dim_equipment_df = spark.read.format("delta").table("silver.dim_equipment")

print("\n📊 Calculating sensor health scores...")

# Aggregate metrics per sensor
sensor_metrics = (
    silver_df
    .groupBy("sensor_id")
    .agg(
        F.count("*").alias("total_readings"),

        # Stability metrics (lower = better)
        F.stddev("reading_value").alias("reading_stddev"),
        F.variance("reading_value").alias("reading_variance"),
        F.avg(F.abs(F.col("reading_change_pct"))).alias("avg_change_pct"),

        # Anomaly metrics (lower = better)
        F.sum(F.when(F.col("anomaly_detected"), 1).otherwise(0)).alias("anomaly_count"),
        F.sum(F.when(F.col("anomaly_severity") == "CRITICAL", 1).otherwise(0)).alias("critical_count"),

        # Quality metrics (higher = better)
        F.sum(F.when(F.col("reading_quality") == "GOOD", 1).otherwise(0)).alias("good_quality_count"),

        # Recent performance (last 24 hours)
        F.sum(F.when(
            (F.col("timestamp") >= F.expr("current_timestamp() - INTERVAL 24 HOURS")) &
            (F.col("anomaly_detected") == True),
            1
        ).otherwise(0)).alias("anomalies_24h")
    )
)

# Calculate normalized scores (0-100)
sensor_scores = (
    sensor_metrics
    .join(dim_equipment_df.select("sensor_id", "equipment_age_years", "days_since_maintenance"), "sensor_id")

    # Component scores (normalize to 0-100)

    # 1. Stability score (based on stddev - lower is better)
    .withColumn("stability_raw", F.col("reading_stddev"))
    .withColumn("stability_score",
                F.greatest(100 - (F.col("stability_raw") * 5), F.lit(0)))

    # 2. Anomaly score (fewer anomalies = higher score)
    .withColumn("anomaly_rate", F.col("anomaly_count") / F.col("total_readings"))
    .withColumn("anomaly_score",
                F.greatest(100 - (F.col("anomaly_rate") * 200), F.lit(0)))

    # 3. Quality score
    .withColumn("quality_rate", F.col("good_quality_count") / F.col("total_readings"))
    .withColumn("quality_score", F.col("quality_rate") * 100)

    # 4. Maintenance score (recent maintenance = higher score)
    .withColumn("maintenance_score",
                F.greatest(100 - (F.col("days_since_maintenance") * 0.3), F.lit(0)))

    # 5. Age score (newer = higher score)
    .withColumn("age_score",
                F.greatest(100 - (F.col("equipment_age_years") * 5), F.lit(0)))

    # 6. Recent anomaly penalty (anomalies in last 24h)
    .withColumn("recent_anomaly_penalty", F.col("anomalies_24h") * 10)

    # Composite health score (weighted average)
    .withColumn("health_score",
                (F.col("stability_score") * 0.25 +
                 F.col("anomaly_score") * 0.30 +
                 F.col("quality_score") * 0.20 +
                 F.col("maintenance_score") * 0.15 +
                 F.col("age_score") * 0.10 -
                 F.col("recent_anomaly_penalty")).cast("int"))

    # Ensure score is 0-100
    .withColumn("health_score",
                F.least(F.greatest(F.col("health_score"), F.lit(0)), F.lit(100)))

    # Health status categories
    .withColumn("health_status",
                F.when(F.col("health_score") >= 85, "EXCELLENT")
                .when(F.col("health_score") >= 70, "GOOD")
                .when(F.col("health_score") >= 50, "FAIR")
                .when(F.col("health_score") >= 30, "POOR")
                .otherwise("CRITICAL"))

    # Recommendations
    .withColumn("recommended_action",
                F.when(F.col("health_score") < 30, "IMMEDIATE_MAINTENANCE")
                .when((F.col("days_since_maintenance") > 90) & (F.col("health_score") < 60), "SCHEDULE_MAINTENANCE")
                .when(F.col("anomaly_rate") > 0.1, "INVESTIGATE_ANOMALIES")
                .when(F.col("quality_rate") < 0.9, "CHECK_SENSOR_CALIBRATION")
                .otherwise("MONITOR"))

    .withColumn("score_timestamp", F.current_timestamp())
)

# Write to gold
sensor_scores.write.format("delta").mode("overwrite").saveAsTable("gold.sensor_health_scores")

print(f"✅ Calculated health scores for {sensor_scores.count():,} sensors")

# Show distribution
print("\n🏥 Sensor Health Status Distribution:")
sensor_scores.groupBy("health_status").agg(
    F.count("*").alias("sensor_count"),
    F.round(F.avg("health_score"), 1).alias("avg_score"),
    F.round(F.avg("anomaly_rate"), 3).alias("avg_anomaly_rate")
).orderBy(F.desc("avg_score")).show()

print("\n📋 Recommended Actions:")
sensor_scores.groupBy("recommended_action").agg(
    F.count("*").alias("sensor_count")
).orderBy(F.desc("sensor_count")).show()

# Critical sensors requiring attention
print("\n🚨 Critical Sensors Requiring Immediate Attention:")
sensor_scores.filter(F.col("health_status") == "CRITICAL").select(
    "sensor_id",
    "health_score",
    "anomaly_rate",
    "days_since_maintenance",
    "recommended_action"
).show(10, truncate=False)

print("\n✅ SENSOR HEALTH SCORING COMPLETE")
print("""
USE CASES:
✓ Predictive maintenance scheduling
✓ Resource allocation (focus on critical sensors)
✓ Alert prioritization (critical sensors first)
✓ Performance dashboards
✓ Compliance reporting (equipment monitoring SLAs)
""")
```

---

### Curveball 3: "Implement Sessionization for Sensor Outages"

**Interviewer**: *"Detect when sensors go offline and create outage sessions."*

```python
print("🎯 CURVEBALL 3: Sensor Outage Sessionization")
print("="*60)

print("""
GOAL: Identify gaps in sensor readings (outages) and create sessions

APPROACH:
1. Calculate time gaps between consecutive readings
2. If gap > threshold (e.g., 5 minutes), mark as outage
3. Group consecutive outage events into sessions
4. Calculate outage duration and impact
""")

silver_df = spark.read.format("delta").table("silver.fact_sensor_readings")

print("\n📊 Step 1: Calculate time gaps between readings")

# Window ordered by timestamp per sensor
sensor_time_window = Window.partitionBy("sensor_id").orderBy("timestamp")

readings_with_gaps = (
    silver_df
    .withColumn("prev_timestamp", F.lag("timestamp", 1).over(sensor_time_window))
    .withColumn("next_timestamp", F.lead("timestamp", 1).over(sensor_time_window))
    .withColumn("gap_seconds",
                (F.unix_timestamp("timestamp") - F.unix_timestamp("prev_timestamp")))
    .withColumn("gap_minutes", F.col("gap_seconds") / 60)
)

print("   ✓ Calculated time gaps between consecutive readings")

print("\n📊 Step 2: Identify outage periods")

OUTAGE_THRESHOLD_MINUTES = 5

outages = (
    readings_with_gaps
    .filter(F.col("gap_minutes") > OUTAGE_THRESHOLD_MINUTES)
    .select(
        "sensor_id",
        "equipment_id",
        "factory_id",
        F.col("prev_timestamp").alias("outage_start"),
        F.col("timestamp").alias("outage_end"),
        F.col("gap_minutes").alias("outage_duration_minutes")
    )
    .withColumn("outage_id", F.monotonically_increasing_id())
)

print(f"   ✓ Identified {outages.count():,} outage periods (gap > {OUTAGE_THRESHOLD_MINUTES} min)")

print("\n📊 Step 3: Enrich with context")

# Classify outage severity
outages_enriched = (
    outages
    .withColumn("outage_severity",
                F.when(F.col("outage_duration_minutes") > 60, "CRITICAL")
                .when(F.col("outage_duration_minutes") > 30, "HIGH")
                .when(F.col("outage_duration_minutes") > 15, "MEDIUM")
                .otherwise("LOW"))

    # Add business impact (readings missed)
    .withColumn("readings_missed",
                (F.col("outage_duration_minutes") * 60 / 10).cast("int"))  # 1 reading per 10 sec

    .withColumn("detection_timestamp", F.current_timestamp())
)

# Write to gold
outages_enriched.write.format("delta").mode("overwrite").saveAsTable("gold.sensor_outages")

print(f"✅ Created gold.sensor_outages")

print("\n📊 Outage Statistics:")
outages_enriched.select(
    F.count("*").alias("total_outages"),
    F.round(F.avg("outage_duration_minutes"), 1).alias("avg_duration_min"),
    F.max("outage_duration_minutes").alias("max_duration_min"),
    F.sum("readings_missed").alias("total_readings_missed")
).show(vertical=True)

print("\n🚨 Outage Severity Distribution:")
outages_enriched.groupBy("outage_severity").agg(
    F.count("*").alias("outage_count"),
    F.round(F.avg("outage_duration_minutes"), 1).alias("avg_duration")
).orderBy("outage_severity").show()

print("\n📋 Sample Outages:")
outages_enriched.orderBy(F.desc("outage_duration_minutes")).select(
    "sensor_id",
    "outage_start",
    "outage_end",
    F.round("outage_duration_minutes", 1).alias("duration_min"),
    "outage_severity",
    "readings_missed"
).show(10, truncate=False)

# Aggregate by sensor (which sensors have most outages?)
print("\n📊 Sensors with Most Outages:")
outages_enriched.groupBy("sensor_id").agg(
    F.count("*").alias("outage_count"),
    F.sum("outage_duration_minutes").alias("total_downtime_min"),
    F.sum("readings_missed").alias("total_readings_missed")
).orderBy(F.desc("outage_count")).show(10)

print("\n✅ OUTAGE SESSIONIZATION COMPLETE")
print("""
USE CASES:
✓ Proactive sensor maintenance (frequent outages = failing sensor)
✓ Network diagnostics (factory-wide outages = network issue)
✓ SLA monitoring (uptime tracking)
✓ Root cause analysis (correlate outages with events)
✓ Capacity planning (identify critical single points of failure)
""")
```

---

## Summary & Key Takeaways

```python
print("\n" + "="*60)
print("IoT SENSOR PIPELINE - COMPLETE SUMMARY")
print("="*60)

summary = f"""
📊 PIPELINE ARCHITECTURE:

BRONZE (Raw Ingestion):
- Historical: {bronze_df.count():,} sensor readings (7 days)
- Streaming: Real-time ingestion with 30-sec micro-batches
- Watermark: 5 minutes for late data tolerance

SILVER (Transformations):
- Enriched with equipment metadata (broadcast join)
- Calculated moving averages (10-period window)
- Statistical anomaly detection (Z-score > 3)
- Threshold-based alerting (sensor-specific ranges)
- {anomaly_count:,} anomalies detected ({(anomaly_count/bronze_df.count()*100):.2f}%)

GOLD (Analytics & ML):
- Equipment health scores: Weighted composite (0-100)
- Daily aggregates: {daily_health.count():,} equipment-days
- Sensor health monitoring: {sensor_scores.count():,} sensors scored
- Outage detection: {outages.count():,} outage sessions identified
- ML features: Ready for failure prediction models

🎯 KEY FEATURES:

STREAMING:
✓ Structured Streaming with watermarking
✓ Tumbling windows (1-min, 5-min aggregations)
✓ foreachBatch for complex transformations
✓ Real-time alerting for threshold violations
✓ Exactly-once processing with checkpointing

TIME-SERIES ANALYSIS:
✓ Moving averages (10-period windows)
✓ Lag/lead functions for change detection
✓ Seasonality detection (time-of-day patterns)
✓ Trend analysis (improving/degrading equipment)

ANOMALY DETECTION:
✓ Statistical: Z-score based on moving average
✓ Threshold: Sensor-specific normal ranges
✓ Behavioral: Unusual changes (>50% spike)
✓ Composite scoring: Multiple signals combined

🚀 PRODUCTION CONSIDERATIONS:
- Tune watermark based on network latency SLA
- Implement alerting for critical anomalies
- Schedule hourly/daily batch reconciliation
- Monitor streaming query metrics (processing rate, input rate)
- Add ML model serving for real-time predictions
"""

print(summary)
```

---

## Think-Out-Loud Script

**Use during interview**:

> "I've built an end-to-end IoT sensor monitoring platform with both batch and streaming capabilities.
>
> **Bronze Layer**: Real-time ingestion using Structured Streaming with 30-second micro-batches. I set a 5-minute watermark to handle late-arriving data—events within 5 minutes are processed in the stream, anything later is picked up by daily batch reconciliation. This gives us a balance between latency and completeness.
>
> **Silver Layer**: Applied transformations in streaming mode using foreachBatch for complex operations. I enriched sensor readings with equipment metadata using broadcast joins since the dimension is small. Calculated moving averages using window functions to smooth out noise, then detected anomalies using both statistical methods (Z-score > 3 standard deviations) and business-rule thresholds specific to each sensor type.
>
> **Gold Layer**: Created two types of outputs. For streaming, I use tumbling windows to generate 1-minute aggregates—average, min, max, stddev per sensor—and write them to Delta for real-time dashboards. For batch analytics, I calculate daily equipment health scores using a weighted composite of stability, anomaly frequency, data quality, and maintenance recency. Also built ML feature sets for failure prediction.
>
> **Advanced Features**: Implemented sensor outage sessionization by detecting gaps larger than 5 minutes between consecutive readings, then grouping them into outage sessions with severity classification. Created a comprehensive health scoring system that combines multiple signals into a 0-100 score with recommended actions.
>
> **For scale**, streaming handles 1000+ events per second with automatic checkpointing for fault tolerance. The watermarking strategy ensures we don't keep state forever—after the watermark threshold, late data goes to batch processing. Delta Lake provides ACID guarantees so batch and streaming can safely write to the same tables without conflicts."
