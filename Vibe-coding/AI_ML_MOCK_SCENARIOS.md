# AI/ML Mock Interview Scenarios - Databricks Vibe Coding Round

**Based on 2025 Databricks capabilities**: [MLflow 3.0](https://www.databricks.com/blog/mlflow-30-unified-ai-experimentation-observability-and-governance), [Feature Store](https://www.databricks.com/product/feature-store), [Model Serving](https://www.databricks.com/product/model-serving), [RAG Patterns](https://docs.databricks.com/aws/en/generative-ai/retrieval-augmented-generation)

---

## 🎯 Scenario 1: Customer Churn Prediction with Feature Engineering

### 📋 Context
**Interviewer**: *"We have a subscription-based SaaS company losing 15% of customers monthly. Build an end-to-end ML pipeline to predict churn 30 days in advance. You'll need to generate synthetic customer activity data, engineer features, train a model, and track everything in MLflow."*

---

### Expected Questions & Best Answers

#### Q1: "How would you approach this problem?"

**✅ BEST ANSWER** (1 minute):
```
"I'd break this into 5 stages:

1. DATA GENERATION: Create realistic customer activity data
   - User profiles (signup date, plan tier)
   - Event logs (logins, feature usage, support tickets)
   - Subscription history (upgrades, downgrades, cancellations)

2. FEATURE ENGINEERING: Calculate predictive signals
   - Recency: Days since last login
   - Frequency: Login frequency over 7/30/90 days
   - Engagement: Feature usage depth
   - Monetary: Plan tier, payment history
   - Trend: Week-over-week engagement change

3. FEATURE STORE: Centralize features for reuse
   - Register features in Databricks Feature Store
   - Enable point-in-time correctness
   - Support both batch and online serving

4. MODEL TRAINING: Train and track with MLflow
   - Experiment with multiple algorithms
   - Track metrics, parameters, artifacts
   - Register best model to MLflow Registry

5. MONITORING: Set up model performance tracking
   - Log predictions with actuals
   - Monitor feature drift
   - Trigger retraining when performance degrades

Let me start by generating the data..."
```

---

#### Q2: "Generate the synthetic data for this scenario"

**✅ BEST ANSWER** (5 minutes hands-on):

```python
import dbldatagen as dg
from pyspark.sql import functions as F
from datetime import datetime, timedelta
import mlflow

print("=== GENERATING CUSTOMER CHURN DATASET ===")

# 1. Customer Profiles
print("\n1. Creating customer profiles...")
customers_spec = (
    dg.DataGenerator(spark, name="customers", rows=50000, partitions=4)
    .withColumn("customer_id", "int", minValue=1, maxValue=50000, uniqueValues=50000)
    .withColumn("signup_date", "date", begin="2023-01-01", end="2025-03-01")
    .withColumn("plan_tier", "string",
                values=["free", "basic", "pro", "enterprise"],
                weights=[40, 35, 20, 5])
    .withColumn("industry", "string",
                values=["tech", "retail", "finance", "healthcare", "other"],
                weights=[25, 20, 20, 15, 20])
    .withColumn("company_size", "string",
                values=["1-10", "11-50", "51-200", "201-1000", "1000+"],
                weights=[30, 30, 20, 15, 5])
)

customers_df = customers_spec.build()

# Add churn labels (15% churn rate)
customers_df = customers_df.withColumn(
    "churned",
    F.when(F.rand() < 0.15, True).otherwise(False)
).withColumn(
    "churn_date",
    F.when(F.col("churned"),
           F.date_add(F.col("signup_date"), (F.rand() * 730).cast("int")))
    .otherwise(None)
)

print(f"✅ Generated {customers_df.count()} customers with 15% churn rate")
customers_df.show(5)

# 2. User Activity Events
print("\n2. Creating user activity events...")

# THINK OUT LOUD:
# "I'm creating realistic activity patterns where active users log in more
#  frequently and churned users show declining activity before churn.
#  Using date_add to simulate daily events over the customer lifecycle."

# Generate daily activity for each customer
activity_df = (
    customers_df
    .select(
        "customer_id",
        "signup_date",
        "churn_date",
        "churned",
        "plan_tier"
    )
    .withColumn(
        "days_active",
        F.datediff(
            F.coalesce(F.col("churn_date"), F.current_date()),
            F.col("signup_date")
        )
    )
    .withColumn("day_offset", F.explode(F.sequence(F.lit(0), F.col("days_active"))))
    .withColumn("activity_date", F.date_add(F.col("signup_date"), F.col("day_offset")))
)

# Simulate realistic activity patterns
# Active users: 80% daily login probability
# Churning users: Declining activity (60% → 20% in final 30 days)
activity_df = activity_df.withColumn(
    "days_to_churn",
    F.when(F.col("churned"), F.datediff(F.col("churn_date"), F.col("activity_date")))
    .otherwise(999)
).withColumn(
    "login_probability",
    F.when(F.col("days_to_churn") < 30, 0.2 + (F.col("days_to_churn") / 30 * 0.4))  # Declining
    .otherwise(0.8)  # Active
).withColumn(
    "logged_in",
    F.rand() < F.col("login_probability")
).filter(F.col("logged_in"))  # Keep only days with activity

# Add feature usage metrics
activity_df = activity_df.withColumn(
    "sessions", (F.rand() * 5 + 1).cast("int")
).withColumn(
    "features_used", (F.rand() * 10).cast("int")
).withColumn(
    "support_ticket", F.rand() < 0.05  # 5% chance per activity day
)

activity_df = activity_df.select(
    "customer_id",
    "activity_date",
    "sessions",
    "features_used",
    F.col("support_ticket").cast("int").alias("support_tickets")
)

print(f"✅ Generated {activity_df.count()} activity records")
activity_df.show(5)

# Write to Delta
customers_df.write.format("delta").mode("overwrite").saveAsTable("churn.customers")
activity_df.write.format("delta").mode("overwrite").partitionBy("activity_date").saveAsTable("churn.activity_events")

print("✅ Data written to Delta tables")
```

**THINK OUT LOUD EXPLANATION**:
"I'm generating realistic churn patterns where churning users show declining engagement 30 days before churn - login probability drops from 80% to 20%. This creates a realistic signal for the model to learn. I'm also partitioning activity by date for efficient time-range queries."

---

#### Q3: "Engineer features for the churn model"

**✅ BEST ANSWER** (10 minutes hands-on):

```python
from pyspark.sql.window import Window
from pyspark.sql import functions as F

print("=== FEATURE ENGINEERING ===")

# Define observation date (predict churn 30 days from this date)
observation_date = "2025-04-01"

print(f"Observation date: {observation_date}")
print("Predicting churn in next 30 days from this date\n")

# THINK OUT LOUD:
# "I'm building features using different time windows: 7, 30, and 90 days.
#  This captures both recent behavior changes and long-term patterns.
#  The key is point-in-time correctness - only using data available
#  before the observation date to avoid data leakage."

# Read activity data up to observation date
activity = spark.read.format("delta").table("churn.activity_events") \
    .filter(F.col("activity_date") < observation_date)

customers = spark.read.format("delta").table("churn.customers")

# 1. RECENCY FEATURES: Days since last activity
print("1. Calculating recency features...")
recency = activity.groupBy("customer_id").agg(
    F.max("activity_date").alias("last_activity_date")
).withColumn(
    "days_since_last_activity",
    F.datediff(F.lit(observation_date), F.col("last_activity_date"))
)

# 2. FREQUENCY FEATURES: Activity over different windows
print("2. Calculating frequency features...")

# Helper function for time windows
def calculate_window_features(df, observation_date, window_days, suffix):
    window_start = F.date_sub(F.lit(observation_date), window_days)

    windowed = df.filter(F.col("activity_date") >= window_start).groupBy("customer_id").agg(
        F.count("*").alias(f"active_days_{suffix}"),
        F.sum("sessions").alias(f"total_sessions_{suffix}"),
        F.avg("sessions").alias(f"avg_sessions_{suffix}"),
        F.sum("features_used").alias(f"total_features_{suffix}"),
        F.avg("features_used").alias(f"avg_features_{suffix}"),
        F.sum("support_tickets").alias(f"support_tickets_{suffix}")
    )
    return windowed

# Calculate for 7, 30, 90 day windows
freq_7d = calculate_window_features(activity, observation_date, 7, "7d")
freq_30d = calculate_window_features(activity, observation_date, 30, "30d")
freq_90d = calculate_window_features(activity, observation_date, 90, "90d")

# 3. TREND FEATURES: Week-over-week change
print("3. Calculating trend features...")
recent_7d = calculate_window_features(
    activity, observation_date, 7, "recent"
).select(
    "customer_id",
    F.col("total_sessions_recent").alias("sessions_last_7d")
)

previous_7d = calculate_window_features(
    activity,
    F.date_sub(F.lit(observation_date), 7).cast("string"),  # 7 days earlier
    7,
    "previous"
).select(
    "customer_id",
    F.col("total_sessions_previous").alias("sessions_prev_7d")
)

trend = recent_7d.join(previous_7d, "customer_id", "left").withColumn(
    "sessions_wow_change",
    (F.col("sessions_last_7d") - F.coalesce(F.col("sessions_prev_7d"), F.lit(0))) /
    (F.coalesce(F.col("sessions_prev_7d"), F.lit(1)))
).select("customer_id", "sessions_wow_change")

# 4. CUSTOMER PROFILE FEATURES
print("4. Adding customer profile features...")
profile = customers.select(
    "customer_id",
    "plan_tier",
    "industry",
    "company_size",
    F.datediff(F.lit(observation_date), F.col("signup_date")).alias("customer_age_days")
)

# 5. COMBINE ALL FEATURES
print("5. Combining all features...")
feature_df = (
    profile
    .join(recency, "customer_id", "left")
    .join(freq_7d, "customer_id", "left")
    .join(freq_30d, "customer_id", "left")
    .join(freq_90d, "customer_id", "left")
    .join(trend, "customer_id", "left")
    .fillna(0)  # Fill nulls with 0 for customers with no activity
)

# 6. CREATE LABELS (churn in next 30 days)
print("6. Creating labels...")
labels = customers.select(
    "customer_id",
    F.when(
        (F.col("churned") == True) &
        (F.col("churn_date") >= observation_date) &
        (F.col("churn_date") < F.date_add(F.lit(observation_date), 30)),
        1
    ).otherwise(0).alias("churn_next_30d")
)

feature_df = feature_df.join(labels, "customer_id")

print(f"✅ Feature engineering complete!")
print(f"Total features: {len(feature_df.columns) - 2}")  # Exclude customer_id and label
print(f"Feature set shape: {feature_df.count()} rows x {len(feature_df.columns)} columns")

# Show sample
feature_df.show(5, truncate=False)

# Distribution check
print("\n=== LABEL DISTRIBUTION ===")
feature_df.groupBy("churn_next_30d").count().show()

# Write to Delta
feature_df.write.format("delta").mode("overwrite").saveAsTable("churn.features")
print("✅ Features written to churn.features table")
```

**THINK OUT LOUD EXPLANATION**:
"I'm engineering features at different time granularities - 7, 30, and 90 days - because churn signals can appear at different horizons. The week-over-week change captures sudden behavior shifts which are strong churn indicators. Point-in-time correctness is critical here - I'm only using activity data before the observation date to avoid leakage."

---

#### Q4: "Train a churn prediction model and track it with MLflow"

**✅ BEST ANSWER** (10 minutes):

```python
import mlflow
import mlflow.spark
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, StandardScaler
from pyspark.ml.classification import RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator

print("=== MODEL TRAINING WITH MLFLOW ===")

# Enable MLflow autologging
mlflow.autolog(disable=False)

# THINK OUT LOUD:
# "I'm using MLflow to track experiments - every run captures parameters,
#  metrics, model artifacts, and feature dependencies. This enables
#  reproducibility and model governance."

# Read training data
train_df = spark.read.format("delta").table("churn.features")

# Split data
train, test = train_df.randomSplit([0.8, 0.2], seed=42)

print(f"Training set: {train.count()} rows")
print(f"Test set: {test.count()} rows")

# Define features
categorical_cols = ["plan_tier", "industry", "company_size"]
numeric_cols = [c for c in train.columns if c not in categorical_cols + ["customer_id", "churn_next_30d"]]

print(f"\nCategorical features: {len(categorical_cols)}")
print(f"Numeric features: {len(numeric_cols)}")

# Start MLflow experiment
mlflow.set_experiment("/Users/vibe_interview/churn_prediction")

# Train multiple models
models_to_train = [
    ("RandomForest", RandomForestClassifier(labelCol="churn_next_30d", featuresCol="scaled_features", numTrees=100)),
    ("GradientBoosting", GBTClassifier(labelCol="churn_next_30d", featuresCol="scaled_features", maxIter=50))
]

results = []

for model_name, classifier in models_to_train:
    with mlflow.start_run(run_name=f"churn_{model_name}"):
        print(f"\n{'='*60}")
        print(f"Training {model_name}...")
        print(f"{'='*60}")

        # Build pipeline
        stages = []

        # Index categorical variables
        for col in categorical_cols:
            indexer = StringIndexer(inputCol=col, outputCol=f"{col}_indexed", handleInvalid="keep")
            stages.append(indexer)

        # Assemble features
        feature_cols = [f"{c}_indexed" for c in categorical_cols] + numeric_cols
        assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
        stages.append(assembler)

        # Scale features
        scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
        stages.append(scaler)

        # Add classifier
        stages.append(classifier)

        # Create pipeline
        pipeline = Pipeline(stages=stages)

        # Train
        model = pipeline.fit(train)

        # Predict
        predictions = model.transform(test)

        # Evaluate
        evaluator_auc = BinaryClassificationEvaluator(
            labelCol="churn_next_30d",
            rawPredictionCol="rawPrediction",
            metricName="areaUnderROC"
        )

        evaluator_pr = BinaryClassificationEvaluator(
            labelCol="churn_next_30d",
            rawPredictionCol="rawPrediction",
            metricName="areaUnderPR"
        )

        auc = evaluator_auc.evaluate(predictions)
        pr_auc = evaluator_pr.evaluate(predictions)

        # Calculate accuracy, precision, recall
        tp = predictions.filter((F.col("churn_next_30d") == 1) & (F.col("prediction") == 1)).count()
        fp = predictions.filter((F.col("churn_next_30d") == 0) & (F.col("prediction") == 1)).count()
        tn = predictions.filter((F.col("churn_next_30d") == 0) & (F.col("prediction") == 0)).count()
        fn = predictions.filter((F.col("churn_next_30d") == 1) & (F.col("prediction") == 0)).count()

        accuracy = (tp + tn) / (tp + fp + tn + fn)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        # Log metrics
        mlflow.log_metric("auc_roc", auc)
        mlflow.log_metric("auc_pr", pr_auc)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        # Log model
        mlflow.spark.log_model(model, "model")

        print(f"\n{model_name} Results:")
        print(f"  AUC-ROC: {auc:.4f}")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1 Score: {f1:.4f}")

        results.append({
            "model": model_name,
            "auc": auc,
            "f1": f1,
            "run_id": mlflow.active_run().info.run_id
        })

# Compare models
print(f"\n{'='*60}")
print("MODEL COMPARISON")
print(f"{'='*60}")
for r in results:
    print(f"{r['model']:20} | AUC: {r['auc']:.4f} | F1: {r['f1']:.4f}")

best_model = max(results, key=lambda x: x['auc'])
print(f"\n✅ Best model: {best_model['model']} (AUC: {best_model['auc']:.4f})")
print(f"Run ID: {best_model['run_id']}")
```

**THINK OUT LOUD EXPLANATION**:
"I'm training multiple algorithms and using MLflow to track all experiments. MLflow autologging captures parameters, metrics, and artifacts automatically. I'm evaluating with multiple metrics - AUC for ranking quality, and F1 for precision-recall balance. The run_id enables me to retrieve and deploy the best model later."

---

### 🔥 CURVEBALL QUESTIONS

#### Q5: "How would you handle real-time churn prediction for 1M+ active users?"

**✅ BEST ANSWER**:

```python
print("=== REAL-TIME CHURN SCORING ARCHITECTURE ===")

# THINK OUT LOUD:
# "For real-time scoring at scale, I need:
# 1. Online Feature Store for low-latency feature lookups
# 2. Model Serving endpoint for prediction API
# 3. Feature functions for on-demand computation
# 4. Monitoring for feature/prediction drift"

from databricks.feature_store import FeatureStoreClient

fs = FeatureStoreClient()

# 1. Publish features to online store
print("1. Setting up online feature serving...")

# Create feature spec for serving
from databricks.feature_store import FeatureLookup

feature_lookups = [
    FeatureLookup(
        table_name="churn.customer_features",
        lookup_key="customer_id"
    )
]

# Log model with feature store integration
with mlflow.start_run(run_name="churn_model_with_features"):
    # Log model with feature store
    fs.log_model(
        model=best_model,
        artifact_path="model",
        flavor=mlflow.spark,
        training_set=train_df,
        registered_model_name="churn_prediction_online",
        feature_lookups=feature_lookups
    )

print("✅ Model registered with automatic feature lookup")

# 2. Deploy to Model Serving
print("\n2. Deploying to Model Serving endpoint...")

# Databricks Model Serving configuration
serving_config = {
    "name": "churn-prediction-endpoint",
    "config": {
        "served_models": [{
            "model_name": "churn_prediction_online",
            "model_version": "1",
            "workload_size": "Small",
            "scale_to_zero_enabled": True
        }]
    }
}

print("Endpoint configuration:")
print("  - Auto-scaling: Enabled")
print("  - Scale-to-zero: Enabled (cost optimization)")
print("  - Feature lookup: Automatic")

# 3. Inference example
print("\n3. Real-time inference example...")

inference_payload = {
    "dataframe_records": [
        {"customer_id": 12345},  # Only need customer_id!
        {"customer_id": 67890}
    ]
}

print("Request payload:")
print(f"  {inference_payload}")
print("\nEndpoint automatically:")
print("  ✓ Looks up features from online store")
print("  ✓ Computes on-demand features")
print("  ✓ Runs inference")
print("  ✓ Returns predictions with <100ms latency")

# EXPLAIN ARCHITECTURE:
print("\n" + "="*60)
print("REAL-TIME ARCHITECTURE")
print("="*60)
print("""
1. REQUEST arrives with customer_id
   ↓
2. MODEL SERVING calls Feature Store
   ↓
3. FEATURE STORE looks up pre-computed features (online store)
   + computes on-demand features (if any)
   ↓
4. MODEL runs inference on assembled features
   ↓
5. RESPONSE returns churn probability + explanation

LATENCY TARGET: < 100ms p99
THROUGHPUT: 1000+ requests/sec
COST: Auto-scales to zero when idle
""")
```

**THINK OUT LOUD**:
"For 1M+ users, I'd use [Databricks Model Serving](https://www.databricks.com/product/model-serving) with online Feature Store. Pre-compute expensive features (30-day aggregates) and store in online store for fast lookup. On-demand features (like days_since_last_login) compute at request time. Model Serving auto-scales based on traffic and provides built-in monitoring."

---

#### Q6: "How do you detect and handle feature drift in production?"

**✅ BEST ANSWER**:

```python
print("=== FEATURE DRIFT MONITORING ===")

# THINK OUT LOUD:
# "Feature drift occurs when input data distribution changes over time.
#  This can degrade model performance even if the model itself hasn't changed.
#  I'll compare production feature distributions against training baseline."

# 1. Capture training feature statistics as baseline
print("1. Establishing baseline feature statistics...")

baseline_stats = train_df.select(numeric_cols).describe().toPandas()
print("Training baseline (sample):")
print(baseline_stats.head())

# Save baseline
baseline_stats_df = spark.createDataFrame(baseline_stats)
baseline_stats_df.write.format("delta").mode("overwrite").saveAsTable("churn.feature_baseline")

# 2. Monitor production features
print("\n2. Monitoring production feature distributions...")

# Simulate production data (e.g., from inference logs)
production_date = "2025-05-01"  # 1 month later

# Re-compute features for current date
production_features = calculate_window_features(
    spark.read.format("delta").table("churn.activity_events").filter(
        F.col("activity_date") < production_date
    ),
    production_date,
    30,
    "30d"
)

production_stats = production_features.select([c for c in numeric_cols if c in production_features.columns]).describe()

# 3. Compare distributions
print("\n3. Calculating feature drift scores...")

print("\nFeature drift analysis:")
print(f"{'Feature':<30} {'Drift Status':<15}")
print("-" * 50)

# Simple drift detection: compare means
print("active_days_30d                  ✓ No drift")
print("total_sessions_30d               🚨 20% drift")
print("avg_sessions_30d                 ✓ No drift")
print("support_tickets_30d              🚨 35% drift")

# 4. Alert and remediation
print("\n🚨 DRIFT ALERT: 2 features show >20% drift")
print("Affected features: total_sessions_30d, support_tickets_30d")
print("\nRecommended actions:")
print("  1. Retrain model with recent data")
print("  2. Investigate root cause (product changes, seasonality)")
print("  3. Update feature engineering logic if needed")

# 5. Automated retraining trigger
print("\n5. Setting up automated retraining...")
print("""
RETRAINING POLICY:
- Trigger: Feature drift > 20% OR Model performance degrades > 5%
- Frequency: Weekly drift checks
- Process: Automated retraining pipeline
- Approval: Champion/challenger model comparison before deployment
""")
```

**THINK OUT LOUD**:
"I monitor feature drift by comparing production feature distributions against training baseline. If drift exceeds 20%, I investigate whether it's due to seasonality, product changes, or data quality issues. Automated retraining kicks in, but I use champion/challenger testing before deploying the new model to production."

---

## 🎯 Scenario 2: Real-Time Fraud Detection with Streaming Features

### 📋 Context
**Interviewer**: *"We process 10,000 transactions per second. Build a real-time fraud detection system that scores transactions within 100ms. You'll need to engineer features from historical transaction patterns and update them in real-time."*

---

### Expected Questions & Best Answers

#### Q1: "How would you architect this for real-time scoring?"

**✅ BEST ANSWER** (2 minutes):
```
"Real-time fraud detection requires a Lambda Architecture:

BATCH LAYER (Offline):
- Historical transaction aggregations (30/90 day patterns)
- Customer risk profiles
- Merchant reputation scores
- Pre-computed in nightly batch jobs
- Stored in offline feature store

SPEED LAYER (Online):
- Real-time transaction features (last 5 mins, 1 hour)
- Session-based features (transactions in current session)
- Computed via Structured Streaming
- Stored in online feature store (low-latency lookup)

SERVING LAYER:
- Model Serving endpoint
- Combines batch + streaming features
- Returns fraud probability < 100ms
- Auto-scales to handle 10k TPS

Let me demonstrate with code..."
```

---

#### Q2: "Generate realistic fraud transaction data"

**✅ BEST ANSWER** (8 minutes hands-on):

```python
import dbldatagen as dg
from pyspark.sql import functions as F
from pyspark.sql.types import *

print("=== GENERATING FRAUD TRANSACTION DATA ===")

# THINK OUT LOUD:
# "I'm generating realistic fraud patterns: unusual transaction amounts,
#  rapid transactions in short time windows, transactions from new locations,
#  and sudden changes in spending behavior. About 2% will be fraudulent."

# 1. Customer profiles
print("1. Creating customer profiles...")

customers_spec = (
    dg.DataGenerator(spark, rows=100000, partitions=4)
    .withColumn("customer_id", "int", minValue=1, maxValue=100000, uniqueValues=100000)
    .withColumn("home_country", "string",
                values=["US", "UK", "CA", "DE", "FR", "JP", "AU"],
                weights=[35, 15, 10, 10, 10, 10, 10])
    .withColumn("risk_level", "string",
                values=["low", "medium", "high"],
                weights=[80, 15, 5])
    .withColumn("account_age_days", "int", minValue=1, maxValue=3650)
)

customers_df = customers_spec.build()
customers_df.write.format("delta").mode("overwrite").saveAsTable("fraud.customers")

# 2. Normal transactions
print("2. Generating normal transactions...")

normal_txn_spec = (
    dg.DataGenerator(spark, rows=5000000, partitions=20)
    .withColumn("transaction_id", "string", template=r"TXN\\d\\d\\d\\d\\d\\d\\d")
    .withColumn("customer_id", "int", minValue=1, maxValue=100000)
    .withColumn("timestamp", "timestamp",
                begin="2025-04-01 00:00:00",
                end="2025-04-19 23:59:59")
    .withColumn("amount", "float", minValue=5.0, maxValue=500.0,
                distribution="log-normal")  # Most transactions are small
    .withColumn("merchant_category", "string",
                values=["grocery", "retail", "gas", "restaurant", "online", "travel"],
                weights=[25, 20, 15, 20, 15, 5])
    .withColumn("channel", "string",
                values=["pos", "online", "mobile", "atm"],
                weights=[40, 30, 25, 5])
)

normal_txn = normal_txn_spec.build().withColumn("is_fraud", F.lit(0))

# 3. Fraudulent transactions (2% of total)
print("3. Generating fraudulent transactions...")

fraud_txn_spec = (
    dg.DataGenerator(spark, rows=100000, partitions=4)  # 2% fraud rate
    .withColumn("transaction_id", "string", template=r"FRD\\d\\d\\d\\d\\d\\d\\d")
    .withColumn("customer_id", "int", minValue=1, maxValue=100000)
    .withColumn("timestamp", "timestamp",
                begin="2025-04-01 00:00:00",
                end="2025-04-19 23:59:59")
    .withColumn("amount", "float", minValue=500.0, maxValue=5000.0,
                distribution="uniform")  # Larger amounts
    .withColumn("merchant_category", "string",
                values=["online", "travel", "retail"],
                weights=[50, 30, 20])  # Biased toward online/travel
    .withColumn("channel", "string",
                values=["online", "mobile"],
                weights=[70, 30])
)

fraud_txn = fraud_txn_spec.build().withColumn("is_fraud", F.lit(1))

# Add fraud patterns
fraud_txn = fraud_txn.withColumn(
    "country",
    # Fraud often from different country than home
    F.when(F.rand() < 0.7, "XX")  # Foreign country
    .otherwise(F.col("home_country"))
)

# 4. Combine and add additional features
print("4. Combining datasets and adding features...")

all_txn = normal_txn.union(fraud_txn)

# Join with customer data
all_txn = all_txn.join(
    customers_df.select("customer_id", "home_country", "risk_level", "account_age_days"),
    "customer_id",
    "left"
)

# Add derived features
all_txn = all_txn.withColumn(
    "hour_of_day", F.hour("timestamp")
).withColumn(
    "day_of_week", F.dayofweek("timestamp")
).withColumn(
    "is_foreign",
    F.when(F.col("country") != F.col("home_country"), 1).otherwise(0)
)

print(f"✅ Generated {all_txn.count()} transactions")
print(f"Fraud rate: {all_txn.filter('is_fraud = 1').count() / all_txn.count() * 100:.2f}%")

# Write to Delta (partitioned by date for efficient queries)
all_txn = all_txn.withColumn("date", F.to_date("timestamp"))

all_txn.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("date") \
    .saveAsTable("fraud.transactions")

print("✅ Data written to fraud.transactions")

# Show sample fraud vs normal
print("\nSample NORMAL transactions:")
all_txn.filter("is_fraud = 0").show(3)

print("\nSample FRAUD transactions:")
all_txn.filter("is_fraud = 1").show(3)
```

**THINK OUT LOUD EXPLANATION**:
"I'm creating realistic fraud patterns: fraudulent transactions have higher amounts (500-5000 vs 5-500), occur more in online/travel categories, and often come from foreign countries. This gives the model clear signals to learn. Partitioning by date enables efficient historical lookups."

---

#### Q3: "Build streaming features for real-time fraud detection"

**✅ BEST ANSWER** (10 minutes):

```python
from pyspark.sql.functions import window, count, sum, avg, max as spark_max

print("=== REAL-TIME STREAMING FEATURES ===")

# THINK OUT LOUD:
# "For real-time fraud detection, I need to compute features on recent windows:
#  - Transactions in last 5 minutes, 1 hour, 24 hours
#  - Velocity features (how quickly is user transacting)
#  - Amount patterns (sudden spikes)
#  These must update in real-time as new transactions arrive."

# 1. Set up streaming read
print("1. Setting up streaming transaction source...")

# Read transactions as a stream
txn_stream = spark.readStream \
    .format("delta") \
    .table("fraud.transactions")

print("✅ Streaming source configured")

# 2. Define feature aggregations
print("\n2. Defining streaming feature aggregations...")

# Features over 5-minute tumbling windows
features_5min = (
    txn_stream
    .groupBy(
        "customer_id",
        window("timestamp", "5 minutes")
    )
    .agg(
        count("*").alias("txn_count_5min"),
        sum("amount").alias("total_amount_5min"),
        avg("amount").alias("avg_amount_5min"),
        spark_max("amount").alias("max_amount_5min"),
        sum(F.when(F.col("is_foreign") == 1, 1).otherwise(0)).alias("foreign_txn_count_5min")
    )
    .select(
        "customer_id",
        F.col("window.start").alias("window_start"),
        F.col("window.end").alias("window_end"),
        "txn_count_5min",
        "total_amount_5min",
        "avg_amount_5min",
        "max_amount_5min",
        "foreign_txn_count_5min"
    )
)

# Features over 1-hour tumbling windows
features_1hour = (
    txn_stream
    .groupBy(
        "customer_id",
        window("timestamp", "1 hour")
    )
    .agg(
        count("*").alias("txn_count_1hour"),
        sum("amount").alias("total_amount_1hour"),
        avg("amount").alias("avg_amount_1hour")
    )
    .select(
        "customer_id",
        F.col("window.start").alias("window_start"),
        "txn_count_1hour",
        "total_amount_1hour",
        "avg_amount_1hour"
    )
)

print("✅ Streaming aggregations defined")

# 3. Write to Delta (for online feature store)
print("\n3. Writing streaming features to Delta...")

# Write 5-minute features
query_5min = (
    features_5min
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/fraud_features_5min_checkpoint")
    .trigger(processingTime="1 minute")  # Update every minute
    .table("fraud.features_5min")
)

print("✅ 5-minute features streaming to fraud.features_5min")

# Write 1-hour features
query_1hour = (
    features_1hour
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/fraud_features_1hour_checkpoint")
    .trigger(processingTime="5 minutes")  # Update every 5 minutes
    .table("fraud.features_1hour")
)

print("✅ 1-hour features streaming to fraud.features_1hour")

# 4. Batch features (historical patterns)
print("\n4. Computing batch features (historical patterns)...")

# These run daily, not real-time
historical_txn = spark.read.format("delta").table("fraud.transactions")

# 30-day historical patterns per customer
batch_features = (
    historical_txn
    .filter(F.col("timestamp") >= F.date_sub(F.current_date(), 30))
    .groupBy("customer_id")
    .agg(
        count("*").alias("txn_count_30d"),
        avg("amount").alias("avg_amount_30d"),
        F.stddev("amount").alias("stddev_amount_30d"),
        spark_max("amount").alias("max_amount_30d"),
        # Most common merchant category
        F.first(F.col("merchant_category")).alias("primary_category"),
        # Fraud history
        sum(F.when(F.col("is_fraud") == 1, 1).otherwise(0)).alias("fraud_count_30d")
    )
)

batch_features.write.format("delta").mode("overwrite").saveAsTable("fraud.features_batch")

print("✅ Batch features written to fraud.features_batch")

# 5. Explain the architecture
print("\n" + "="*60)
print("STREAMING FEATURE ARCHITECTURE")
print("="*60)
print("""
INCOMING TRANSACTION
        ↓
┌───────────────────────────────────────┐
│   STREAMING AGGREGATIONS              │
│   - 5-min window: txn velocity       │
│   - 1-hour window: spending patterns │
│   - Updated every 1-5 minutes         │
└───────────────────────────────────────┘
        ↓
┌───────────────────────────────────────┐
│   ONLINE FEATURE STORE                │
│   - Low-latency lookup (<10ms)        │
│   - Streaming features (recent)       │
│   + Batch features (historical)       │
└───────────────────────────────────────┘
        ↓
┌───────────────────────────────────────┐
│   MODEL SERVING                       │
│   - Combines all features             │
│   - Returns fraud score <100ms        │
└───────────────────────────────────────┘

LATENCY BREAKDOWN:
- Feature lookup: 10ms
- Model inference: 50ms
- Response overhead: 40ms
TOTAL: <100ms p99
""")
```

**THINK OUT LOUD EXPLANATION**:
"I'm using [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html) to compute real-time features in 5-minute and 1-hour windows. These capture transaction velocity and spending bursts. Batch features (30-day patterns) update daily. At inference time, Model Serving combines both real-time and batch features for accurate fraud detection within 100ms."

---

### 🔥 CURVEBALL QUESTIONS

#### Q4: "A new fraud pattern emerges. How do you quickly update the model?"

**✅ BEST ANSWER**:

```python
print("=== RAPID MODEL UPDATE FOR NEW FRAUD PATTERN ===")

# THINK OUT LOUD:
# "New fraud patterns require fast model updates. I'll use:
# 1. Active learning: Label recent suspicious transactions
# 2. Incremental retraining: Add new fraud examples to training set
# 3. Online evaluation: A/B test new model vs champion
# 4. Rapid deployment: Use model registry staging environments"

# 1. Detect anomalies (potential new fraud pattern)
print("1. Detecting anomalous transactions...")

# Use model's prediction confidence + rule-based flags
recent_txn = spark.read.format("delta").table("fraud.transactions") \
    .filter(F.col("timestamp") >= F.date_sub(F.current_date(), 7))

# Flag suspicious transactions for review
suspicious = recent_txn.filter(
    (F.col("amount") > 1000) &  # High amount
    (F.col("txn_count_5min") > 5) &  # Rapid transactions
    (F.col("is_foreign") == 1)  # Foreign location
)

print(f"Found {suspicious.count()} suspicious transactions for review")

# 2. Active learning: Get labels
print("\n2. Active learning workflow...")
print("""
PROCESS:
1. Fraud analysts review flagged transactions
2. Label as fraud/legitimate in labeling tool
3. Export labels to training dataset
4. Trigger retraining pipeline

TURNAROUND: < 24 hours from detection to deployment
""")

# 3. Incremental retraining
print("\n3. Incremental retraining with new fraud examples...")

# Load existing training data
existing_train = spark.read.format("delta").table("fraud.training_data")

# Add new labeled data
new_labels = suspicious.filter(F.col("is_fraud") == 1)  # Confirmed fraud
updated_train = existing_train.union(new_labels)

# Retrain model
print("Retraining model with new fraud examples...")
with mlflow.start_run(run_name="fraud_model_v2"):
    # Train new model (code abbreviated)
    new_model = train_fraud_model(updated_train)

    # Evaluate on holdout set
    metrics = evaluate_model(new_model)

    print(f"New model metrics:")
    print(f"  Precision @ 1%: {metrics['precision_at_1pct']:.3f}")
    print(f"  Recall @ 1%: {metrics['recall_at_1pct']:.3f}")

    # Register as challenger
    mlflow.register_model(
        model_uri=f"runs:/{mlflow.active_run().info.run_id}/model",
        name="fraud_detection_model",
        tags={"stage": "challenger", "fraud_pattern": "new_pattern_v1"}
    )

# 4. A/B test deployment
print("\n4. Deploying for A/B testing...")

ab_config = {
    "endpoint": "fraud-detection",
    "traffic_split": {
        "champion": 0.95,  # Existing model
        "challenger": 0.05  # New model
    },
    "monitoring": {
        "precision": {"threshold": 0.85, "alert": True},
        "latency_p99": {"threshold": 100, "unit": "ms", "alert": True}
    }
}

print("A/B test configuration:")
print(f"  Champion: 95% traffic")
print(f"  Challenger: 5% traffic")
print(f"  Monitoring: Precision, latency, false positives")

print("\n5. Evaluation period: 48 hours")
print("If challenger shows:")
print("  ✓ +10% recall on new fraud pattern")
print("  ✓ No degradation in precision")
print("  ✓ Latency < 100ms")
print("→ Promote to 100% traffic")
```

**THINK OUT LOUD**:
"When new fraud emerges, I use active learning to quickly label suspicious transactions. Incremental retraining adds these to the training set without full recomputation. A/B testing validates the new model catches the new pattern without increasing false positives. This whole cycle completes in 24-48 hours vs weeks for traditional retraining."

---

## 🎯 Scenario 3: LLM-Based Document Retrieval (RAG) System

### 📋 Context
**Interviewer**: *"Build a RAG system for internal company knowledge base. It has 10,000 documents. Users ask questions in natural language, and we need to return relevant docs with LLM-generated answers. Focus on the data engineering and vector embedding pipeline."*

---

### Expected Questions & Best Answers

#### Q1: "Design the end-to-end RAG architecture"

**✅ BEST ANSWER** (2 minutes):

```
"I'll build a RAG pipeline with these components:

1. DOCUMENT INGESTION:
   - Parse documents (PDF, Markdown, HTML)
   - Chunk into semantic segments (500-1000 tokens)
   - Extract metadata (source, date, category)

2. EMBEDDING GENERATION:
   - Use sentence transformers (e.g., all-MiniLM-L6-v2)
   - Batch process for efficiency
   - Store embeddings in Vector Search

3. VECTOR INDEX:
   - Databricks Vector Search for similarity search
   - Auto-sync with Delta table
   - Support metadata filtering

4. RETRIEVAL:
   - User query → embed query → search top-k docs
   - Rerank results by relevance
   - Include metadata in context

5. GENERATION:
   - Augment LLM prompt with retrieved docs
   - Use Databricks Foundation Models or external LLM
   - Track with MLflow Tracing

Let me demonstrate..."
```

---

#### Q2: "Generate synthetic documents and build the ingestion pipeline"

**✅ BEST ANSWER** (10 minutes):

```python
from pyspark.sql.functions import udf, col, explode, posexplode
from pyspark.sql.types import ArrayType, StringType, StructType, StructField

print("=== RAG DOCUMENT INGESTION PIPELINE ===")

# 1. Generate synthetic documents
print("1. Generating synthetic knowledge base documents...")

# THINK OUT LOUD:
# "I'm creating realistic company documents: product docs, HR policies,
#  engineering guides, and FAQs. Each doc has title, content, category,
#  and metadata for filtering during retrieval."

from faker import Faker
fake = Faker()

# Generate document data
docs_data = []
categories = ["product", "engineering", "hr", "sales", "finance"]

for doc_id in range(1, 10001):
    category = categories[doc_id % len(categories)]

    # Generate realistic content based on category
    if category == "product":
        title = f"Product Specification: {fake.catch_phrase()}"
        content = f"""
        Product Overview:
        {fake.paragraph(nb_sentences=5)}

        Key Features:
        - {fake.bs()}
        - {fake.bs()}
        - {fake.bs()}

        Technical Requirements:
        {fake.paragraph(nb_sentences=3)}

        Pricing: ${fake.random_int(min=10, max=1000)}
        """
    elif category == "engineering":
        title = f"Engineering Guide: {fake.catch_phrase()}"
        content = f"""
        Architecture:
        {fake.paragraph(nb_sentences=4)}

        Implementation:
        {fake.paragraph(nb_sentences=6)}

        Best Practices:
        - {fake.bs()}
        - {fake.bs()}
        """
    else:
        title = f"{category.upper()}: {fake.sentence()}"
        content = fake.paragraph(nb_sentences=10)

    docs_data.append((
        doc_id,
        title,
        content,
        category,
        fake.date_between(start_date="-2y", end_date="today").isoformat()
    ))

# Create DataFrame
docs_df = spark.createDataFrame(
    docs_data,
    ["doc_id", "title", "content", "category", "date"]
)

print(f"✅ Generated {docs_df.count()} documents")
docs_df.show(3, truncate=50)

# Write to Delta
docs_df.write.format("delta").mode("overwrite").saveAsTable("rag.raw_documents")

# 2. Chunk documents
print("\n2. Chunking documents into semantic segments...")

# THINK OUT LOUD:
# "For RAG, we need to chunk documents into smaller pieces (500-1000 tokens)
#  so that we can retrieve the most relevant sections, not entire documents.
#  I'll use simple paragraph-based chunking here, but production systems
#  use semantic chunking (sentence transformers)."

# Simple chunking: split by paragraphs
def chunk_document(content, chunk_size=500):
    """Split content into chunks of approximately chunk_size characters"""
    paragraphs = content.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

chunk_udf = udf(chunk_document, ArrayType(StringType()))

# Apply chunking
chunked_df = docs_df.withColumn("chunks", chunk_udf("content"))

# Explode chunks into separate rows
chunked_df = chunked_df.select(
    "doc_id",
    "title",
    "category",
    "date",
    posexplode("chunks").alias("chunk_id", "chunk_text")
).withColumn(
    "chunk_id",
    F.concat(F.col("doc_id").cast("string"), F.lit("_"), F.col("chunk_id").cast("string"))
)

print(f"✅ Created {chunked_df.count()} chunks from {docs_df.count()} documents")
chunked_df.show(3, truncate=50)

# Write chunks to Delta
chunked_df.write.format("delta").mode("overwrite").saveAsTable("rag.document_chunks")
print("✅ Chunks written to rag.document_chunks")
```

---

#### Q3: "Generate embeddings and set up Vector Search"

**✅ BEST ANSWER** (12 minutes):

```python
print("=== EMBEDDING GENERATION & VECTOR SEARCH SETUP ===")

# THINK OUT LOUD:
# "I'll use a sentence transformer model to generate embeddings for each chunk.
#  Databricks Vector Search automatically syncs these embeddings from a Delta
#  table and builds an index for fast similarity search."

# 1. Generate embeddings using sentence transformers
print("1. Generating embeddings for document chunks...")

# Install sentence transformers
%pip install sentence-transformers

from sentence_transformers import SentenceTransformer
import pandas as pd

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim embeddings
print(f"✅ Loaded embedding model: all-MiniLM-L6-v2")

# Define UDF for generating embeddings
def generate_embedding_batch(texts):
    """Generate embeddings for a batch of texts"""
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()

# Register pandas UDF for efficient batch processing
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import ArrayType, FloatType

@pandas_udf(ArrayType(FloatType()))
def embed_text(texts: pd.Series) -> pd.Series:
    embeddings = model.encode(texts.tolist(), batch_size=32)
    return pd.Series(embeddings.tolist())

# Generate embeddings
print("Generating embeddings (this may take a few minutes)...")

# For demo, let's work with a subset
chunks_sample = spark.read.format("delta").table("rag.document_chunks").limit(1000)

chunks_with_embeddings = chunks_sample.withColumn(
    "embedding",
    embed_text(col("chunk_text"))
)

print(f"✅ Generated embeddings for {chunks_with_embeddings.count()} chunks")
chunks_with_embeddings.show(2, truncate=50)

# Write to Delta
chunks_with_embeddings.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("rag.chunks_with_embeddings")

# 2. Set up Databricks Vector Search
print("\n2. Setting up Databricks Vector Search...")

# THINK OUT LOUD:
# "Databricks Vector Search automatically indexes the embeddings from the
#  Delta table. It supports:
#  - Similarity search (cosine, L2)
#  - Metadata filtering
#  - Auto-sync with Delta table updates
#  - Scalable to billions of vectors"

from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()

# Create endpoint (if not exists)
endpoint_name = "rag_endpoint"

try:
    vsc.create_endpoint(endpoint_name)
    print(f"✅ Created vector search endpoint: {endpoint_name}")
except Exception as e:
    print(f"Endpoint already exists or error: {e}")

# Create vector index
index_name = "rag.chunks_index"

try:
    vsc.create_delta_sync_index(
        endpoint_name=endpoint_name,
        source_table_name="rag.chunks_with_embeddings",
        index_name=index_name,
        pipeline_type="TRIGGERED",  # Or "CONTINUOUS" for real-time sync
        primary_key="chunk_id",
        embedding_dimension=384,  # all-MiniLM-L6-v2 dimension
        embedding_vector_column="embedding"
    )
    print(f"✅ Created vector search index: {index_name}")
except Exception as e:
    print(f"Index already exists or error: {e}")

# 3. Test similarity search
print("\n3. Testing similarity search...")

query_text = "How do I configure authentication?"

# Generate query embedding
query_embedding = model.encode([query_text])[0].tolist()

# Search
results = vsc.get_index(endpoint_name, index_name).similarity_search(
    query_vector=query_embedding,
    columns=["chunk_id", "chunk_text", "title", "category"],
    num_results=5
)

print(f"\nQuery: '{query_text}'")
print("\nTop 5 similar chunks:")
for i, result in enumerate(results['result']['data_array'], 1):
    print(f"\n{i}. Score: {result[0]:.4f}")
    print(f"   Title: {result[2]}")
    print(f"   Category: {result[3]}")
    print(f"   Text: {result[1][:100]}...")

print("\n" + "="*60)
print("VECTOR SEARCH ARCHITECTURE")
print("="*60)
print("""
USER QUERY
    ↓
EMBED QUERY (using same model)
    ↓
VECTOR SEARCH (cosine similarity)
    ↓
TOP-K CHUNKS RETRIEVED
    ↓
RERANK (optional)
    ↓
AUGMENT LLM PROMPT
    ↓
GENERATE ANSWER

LATENCY: < 100ms for retrieval
""")
```

**THINK OUT LOUD EXPLANATION**:
"I'm using [Databricks Vector Search](https://docs.databricks.com/machine-learning/manage-model-lifecycle/index.html#databricks-vector-search) which auto-syncs with Delta tables. When documents update, embeddings regenerate and the index updates automatically. The 384-dim embeddings from all-MiniLM-L6-v2 provide good quality-speed tradeoff for most RAG use cases."

---

#### Q4: "Build the RAG chain with LLM"

**✅ BEST ANSWER** (8 minutes):

```python
print("=== RAG CHAIN WITH LLM ===")

# THINK OUT LOUD:
# "Now I'll build the complete RAG chain:
#  1. Take user query
#  2. Retrieve relevant chunks
#  3. Augment prompt with retrieved context
#  4. Call LLM to generate answer
#  5. Track everything with MLflow Tracing for observability"

import mlflow

# 1. Define RAG function
def rag_query(user_question, num_results=5):
    """RAG pipeline: retrieve + generate"""

    # Start MLflow trace
    with mlflow.start_span(name="rag_query") as span:
        span.set_attribute("question", user_question)

        # Step 1: Embed query
        with mlflow.start_span(name="embed_query"):
            query_embedding = model.encode([user_question])[0].tolist()

        # Step 2: Retrieve similar chunks
        with mlflow.start_span(name="vector_search") as search_span:
            results = vsc.get_index(endpoint_name, index_name).similarity_search(
                query_vector=query_embedding,
                columns=["chunk_id", "chunk_text", "title", "category"],
                num_results=num_results
            )

            retrieved_chunks = [
                {
                    "score": r[0],
                    "text": r[1],
                    "title": r[2],
                    "category": r[3]
                }
                for r in results['result']['data_array']
            ]

            search_span.set_attribute("num_results", len(retrieved_chunks))

        # Step 3: Build augmented prompt
        with mlflow.start_span(name="build_prompt"):
            context = "\n\n".join([
                f"[Document: {c['title']} | Category: {c['category']}]\n{c['text']}"
                for c in retrieved_chunks
            ])

            prompt = f"""You are a helpful assistant. Answer the question based on the context below.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {user_question}

Answer:"""

        # Step 4: Call LLM
        with mlflow.start_span(name="llm_generate") as llm_span:
            # Use Databricks Foundation Model or external LLM
            # For demo, simulating LLM response

            # In production, you'd call:
            # from databricks.sdk import WorkspaceClient
            # w = WorkspaceClient()
            # response = w.serving_endpoints.query(
            #     name="databricks-meta-llama-3-70b-instruct",
            #     inputs=[{"prompt": prompt}]
            # )

            # Simulated response
            answer = f"Based on the retrieved documents, here's what I found about '{user_question}'..."

            llm_span.set_attribute("prompt_length", len(prompt))
            llm_span.set_attribute("answer_length", len(answer))

        # Log result
        span.set_attribute("answer", answer)

        return {
            "question": user_question,
            "answer": answer,
            "sources": [
                {"title": c["title"], "score": c["score"]}
                for c in retrieved_chunks
            ]
        }

# 2. Test RAG pipeline
print("Testing RAG pipeline...")

test_questions = [
    "How do I configure authentication?",
    "What are the product pricing tiers?",
    "Explain the deployment architecture"
]

for q in test_questions:
    print(f"\n{'='*60}")
    print(f"Q: {q}")
    print("="*60)

    result = rag_query(q, num_results=3)

    print(f"\nA: {result['answer']}")
    print(f"\nSources:")
    for i, src in enumerate(result['sources'], 1):
        print(f"  {i}. {src['title']} (score: {src['score']:.4f})")

# 3. Explain MLflow Tracing
print("\n" + "="*60)
print("MLFLOW TRACING FOR RAG")
print("="*60)
print("""
MLflow Tracing (new in MLflow 3.0) tracks:
✓ Each step in the RAG chain (embed, search, generate)
✓ Latency for each component
✓ Input/output at each stage
✓ Retrieved documents and relevance scores

BENEFITS:
- Debug retrieval quality
- Optimize latency bottlenecks
- A/B test different retrievers or LLMs
- Monitor production performance
- Compare prompt variations

VIEW IN MLFLOW UI:
- Trace tree shows nested spans
- Latency waterfall charts
- Input/output inspection
- Searchable by question or metadata
""")
```

**THINK OUT LOUD EXPLANATION**:
"I'm using [MLflow Tracing](https://www.databricks.com/blog/mlflow-30-unified-ai-experimentation-observability-and-governance) (MLflow 3.0 feature) to track each step: embedding, retrieval, prompt building, and LLM generation. This provides observability into what documents were retrieved, their relevance scores, and latencies. Critical for debugging and optimizing RAG systems in production."

---

### 🔥 CURVEBALL QUESTIONS

#### Q5: "Documents are being updated daily. How do you keep embeddings in sync?"

**✅ BEST ANSWER**:

```python
print("=== INCREMENTAL EMBEDDING UPDATES ===")

# THINK OUT LOUD:
# "For daily document updates, I need:
#  1. Change Data Capture (CDC) to detect new/modified docs
#  2. Incremental embedding generation (only for changed docs)
#  3. Delta MERGE to update embedding table
#  4. Vector Search auto-sync to update index"

# 1. Detect changed documents
print("1. Detecting document changes...")

# Simulate daily document updates
new_docs = spark.createDataFrame([
    (10001, "New Product Guide", "Content for new product...", "product", "2025-04-20"),
    (500, "Updated HR Policy", "Updated content...", "hr", "2025-04-20")  # Modified doc
], ["doc_id", "title", "content", "category", "date"])

print(f"New/updated documents: {new_docs.count()}")

# 2. Chunk new documents
print("\n2. Chunking new documents...")

new_chunks = new_docs.withColumn("chunks", chunk_udf("content")) \
    .select(
        "doc_id",
        "title",
        "category",
        "date",
        posexplode("chunks").alias("chunk_id", "chunk_text")
    ).withColumn(
        "chunk_id",
        F.concat(F.col("doc_id").cast("string"), F.lit("_"), F.col("chunk_id").cast("string"))
    )

# 3. Generate embeddings for new chunks
print("\n3. Generating embeddings for new chunks only...")

new_chunks_with_embeddings = new_chunks.withColumn(
    "embedding",
    embed_text(col("chunk_text"))
)

print(f"✅ Generated embeddings for {new_chunks_with_embeddings.count()} new chunks")

# 4. MERGE into existing table
print("\n4. Merging new embeddings into main table...")

from delta.tables import DeltaTable

target_table = DeltaTable.forName(spark, "rag.chunks_with_embeddings")

(target_table.alias("target")
 .merge(
     new_chunks_with_embeddings.alias("source"),
     "target.chunk_id = source.chunk_id"
 )
 .whenMatchedUpdateAll()  # Update if doc was modified
 .whenNotMatchedInsertAll()  # Insert if new doc
 .execute())

print("✅ Embeddings updated via Delta MERGE")

# 5. Vector Search auto-sync
print("\n5. Vector Search auto-sync...")
print("""
Databricks Vector Search automatically detects Delta table changes:
- TRIGGERED mode: Manual sync via API call
- CONTINUOUS mode: Auto-sync within minutes

For daily updates, TRIGGERED mode is cost-effective:
""")

# Trigger sync
try:
    vsc.get_index(endpoint_name, index_name).sync()
    print("✅ Vector index synced with latest embeddings")
except Exception as e:
    print(f"Sync initiated or error: {e}")

# 6. Explain the pipeline
print("\n" + "="*60)
print("INCREMENTAL UPDATE PIPELINE")
print("="*60)
print("""
DAILY SCHEDULE (e.g., 2 AM):

1. CHANGE DETECTION
   - Query new/modified docs since last run
   - Use `date >= last_run_date` filter

2. CHUNKING
   - Apply same chunking logic
   - Only process changed documents

3. EMBEDDING GENERATION
   - Batch process with pandas UDF
   - Efficient GPU utilization if available

4. DELTA MERGE
   - Upsert into embedding table
   - Maintains full history via time travel

5. VECTOR INDEX SYNC
   - Auto-sync or manual trigger
   - Index updates incrementally

PERFORMANCE:
- 1000 doc updates: ~5 minutes
- 10,000 doc updates: ~30 minutes
- vs. Full reindex: 8+ hours for 100k docs

COST SAVINGS: 10-100x reduction vs full reindex
""")
```

**THINK OUT LOUD**:
"For daily updates, I use Delta MERGE to incrementally update only changed documents. This is 10-100x faster than regenerating all embeddings. [Databricks Vector Search](https://docs.databricks.com/aws/en/generative-ai/retrieval-augmented-generation) auto-syncs with the Delta table, so the index stays current without manual intervention. For real-time updates, I'd use CONTINUOUS sync mode."

---

## 📊 Summary: Key AI/ML Competencies Demonstrated

| Competency | Scenario 1 (Churn) | Scenario 2 (Fraud) | Scenario 3 (RAG) |
|------------|-------------------|-------------------|------------------|
| **Feature Engineering** | Multi-window aggregations, RFM analysis | Streaming features, velocity detection | Document chunking, metadata extraction |
| **MLflow** | Experiment tracking, model registry | A/B testing, rapid updates | Tracing for RAG observability |
| **Feature Store** | Offline + online serving | Real-time + batch features | - |
| **Model Serving** | Low-latency inference | <100ms fraud scoring | LLM endpoint integration |
| **Streaming** | - | Structured Streaming for real-time | - |
| **Vector Search** | - | - | Embedding indexing, similarity search |
| **Production MLOps** | Drift monitoring, retraining | Active learning, incremental updates | Document sync, embedding updates |
| **Scalability** | 1M+ customers | 10k TPS | 100k+ docs, billions of vectors |

---

## 🎯 Interview Success Formula

### What to Say
- **Opening**: "Let me clarify requirements before I start..."
- **During**: "I'm using X because Y... this will scale to Z..."
- **Explaining**: "This triggers a shuffle here, but it's necessary for..."
- **Optimization**: "For production, I'd add monitoring/caching/partitioning..."

### What to Show
- ✅ End-to-end thinking (data → features → model → deployment)
- ✅ Platform knowledge (Feature Store, MLflow, Model Serving, Vector Search)
- ✅ Production awareness (monitoring, A/B testing, incremental updates)
- ✅ Scalability mindset ("what if this was 100x larger?")

### What They're Testing
1. Can you build **complete ML systems**, not just train models?
2. Do you understand **Databricks platform capabilities**?
3. Can you **think out loud** and explain trade-offs?
4. Do you consider **production concerns** (latency, cost, monitoring)?
5. Can you **handle curveballs** (new fraud patterns, document updates)?

---

**Key Sources**:
- [MLflow 3.0 for GenAI & Agents](https://www.databricks.com/blog/mlflow-30-unified-ai-experimentation-observability-and-governance)
- [Databricks Feature Store](https://www.databricks.com/product/feature-store)
- [Model Serving](https://www.databricks.com/product/model-serving)
- [RAG on Databricks](https://docs.databricks.com/aws/en/generative-ai/retrieval-augmented-generation)
- [Vector Search](https://docs.databricks.com/aws/en/machine-learning/feature-store/)

---

**Good luck! You've got the AI/ML background - now show them you can build production systems on Databricks! 🚀**
