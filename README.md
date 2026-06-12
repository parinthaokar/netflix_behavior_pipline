# 🎬 End-to-End Netflix Data Pipeline (ELT)
### Automated Orchestration with Astro Airflow, Snowflake, and dbt Core (Cosmos)

---

## 📌 Project Overview
Streaming platforms live and die by content decisions — what to greenlight, what to promote, what to kill. But when those decisions are made on 24-hour-old data manually pulled by analysts, the business is always reacting, never anticipating. This pipeline eliminates that lag.

The core problem it solves: Content and growth teams shouldn't be waiting on data engineers to run manual exports before making programming decisions. This pipeline makes behavioral analytics — genre engagement, subscription revenue, device profiles — automatically available and always current.

This project implements a modern, automated ELT (Extract, Load, Transform) data pipeline designed to process simulated Netflix user behavior data. 

The pipeline orchestrates the ingestion of raw data from an **AWS S3 Bucket**, loads it securely into a **Snowflake Cloud Data Warehouse**, and dynamically triggers modular **dbt Core** models using **Astronomer Cosmos** to build clean staging views and production-ready analytics marts.

---

## 🏗️ Technical Architecture & Data Flow

```text
       [ AWS S3 Bucket ]
               │
               ▼ (Raw Data Ingestion via COPY INTO)
     [ Snowflake (RAW_DATA Schema) ]
               │
               ▼ 🚀 Managed by Airflow SQLExecuteQueryOperator
     [ dbt Core / Cosmos Task Group ] 🧠 Models executed natively as Airflow tasks
               │
               ├──► Staging Layer (stg_user_subscription_info)
               └──► Analytics Marts (mart_subscription_revenue, mart_genre_engagement)



### Key Components:

* **Orchestration:** [Astronomer Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) (Apache Airflow) running inside isolated Docker containers.
* **Storage & Compute:** Snowflake Cloud Data Warehouse.
* **Transformations:** dbt Core dynamically parsed into an Airflow Directed Acyclic Graph (DAG) via **Astronomer Cosmos**, eliminating the need to compile manifest files manually.

---text
## 📂 Repository Structure


.
├── my-airflow-project/              # Main Airflow Environment
│   ├── dags/
│   │   └── load_netflix_data.py    # Main Orchestration DAG file
│   ├── include/
│   │   └── netflix_behavior_pipline/# Modular dbt Project Folder
│   │       ├── models/
│   │       │   ├── staging/         # Materialized views cleansing raw data
│   │       │   └── marts/           # Final reporting and KPI tables
│   │       └── dbt_project.yml      # dbt Configuration File
│   ├── Dockerfile                   # Custom Airflow build container
│   └── requirements.txt             # Project dependencies (cosmos, dbt-snowflake)
└── README.md

```

---

## ⚡ DAG Pipeline Execution Flow

When triggered, Apache Airflow sequences the pipeline natively across your infrastructure:

1. **`copy_s3_to_snowflake`**: Optimally streams data from the cloud storage stage into raw staging tables using Snowflake’s bulk `COPY INTO` command.
2. **`dbt_transformations` (Cosmos Task Group)**: Cosmos dynamically builds out individual dbt runs as isolated, native Airflow nodes:
* **Staging:** Cleanses string metrics and fixes schema anomalies in the `stg_` models.
* **Marts:** Generates downstream business metrics (Revenue streams, platform engagement logs, content popularity arrays) in the `mart_` models.



---

## 🛠️ Local Environment Setup & Deployment

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) installed (`brew install astronomer/tap/astro`).
* Active **Snowflake Account**.

### 1. Initialize Docker Containers

Navigate to your project directory and spin up the Airflow framework locally:

```bash
cd my-airflow-project
astro dev start

```

> 💡 **Note:** This initializes the Airflow Web Server, Scheduler, and Metadata Database inside Docker. Access the UI at `http://localhost:8080` using the default credentials (`admin` / `admin`).

### 2. Configure Airflow Connections

To safely process pipelines without hardcoding secrets, create a connection inside the Airflow UI (**Admin -> Connections**):

| Connection Field | Value |
| --- | --- |
| **Connection ID** | `snowflake_conn` |
| **Connection Type** | `Snowflake` |
| **Account** | `<your_snowflake_account_locator>` |
| **Warehouse** | `COMPUTE_WH` |
| **Database** | `NETFLIX_BEHAVIOR` |
| **Schema** | `RAW_DATA` |
| **Login / Password** | *Your Snowflake credentials* |

### 3. Run Pipeline Execution

Unpause the `s3_to_snowflake_pipeline` DAG in the Airflow UI and click **Trigger DAG**. Monitor the live end-to-end telemetry graph until all tasks resolve in green success states.

---

## 📈 Core Data Mart Analytics Delivered

* **💰 Subscription Revenue Tracking:** Financial reporting summarizing aggregate platform yields based on user demographic tiers.
* **📊 Genre Engagement Analytics:** Aggregated viewing metrics determining peak performance periods across target genres.
* **📱 Device Behavior Profiles:** Performance benchmarking cross-referencing watch durations against hardware distributions.

