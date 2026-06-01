# OmniStream: GCP AI Solutions Proof of Concept (PoC)

OmniStream is an enterprise-grade, single-file Streamlit application serving as a highly interactive, professional Proof of Concept (PoC) for a real-time e-commerce recommendation platform on Google Cloud Platform (GCP). 

Built by Google Cloud Solutions Architects, this app demonstrates the intersection of real-time telemetry streaming, localized machine learning collaborative filtering, and enterprise security foundations.

---

## 🏗️ Production System Architecture

In a production environment, this pipeline scales on fully managed Google Cloud infrastructure. Below is the data flow topology:

```text
                                  +-----------------------+
                                  |   Web Client / App    |
                                  +-----------+-----------+
                                              | (JSON Payload)
                                              v
                                  +-----------+-----------+
                                  |  Google Cloud Pub/Sub | (Global Ingestion Queue)
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------+-----------+
                                  | Google Cloud Dataflow | (Stateful Beam Processing)
                                  +-----+-----------+-----+
                                        |           |
                     (Streaming Ingest) |           | (Model Embeddings)
                                        v           v
                    +-------------------+---+   +---+-------------------+
                    |   GCP BigQuery Raw    |   | Vertex AI Vector Search| (10ms Latency ANN)
                    |   (Clustered/Part.)   |   |   (Matching Engine)   |
                    +-----------------------+   +-----------------------+
```

---

## 🛠️ Application Modules & Features

The self-contained application (`app.py`) is structured across three interactive workspaces:

### 📈 Tab 1: Real-Time Event Ingestion (Simulated)
*   **Dynamic Telemetry Ingestion Loop:** An active background stream updating metric counts and event charts dynamically.
*   **Live Metrics Panel:** Sleek glassmorphic metrics measuring Ingestion Velocity (Events/Sec), Active Users Tracked, and Live Simulated Revenue.
*   **Moving Time-Series Visuals:** Area charts and event share donut indicators using Plotly Dark theme.
*   **Architect Narrative:** Deep-dive analysis of real-time stream aggregation utilizing **Pub/Sub**, **Dataflow**, and **BigQuery Ingestion Storage**.

### 🔮 Tab 2: Vertex AI Recommendation Engine (Simulated)
*   **Localized Collaborative Filtering Model:** Dynamic User-User Collaborative Filtering powered by **Scikit-Learn** cosine similarity.
*   **Customer Persona Telemetry Profiles:** Interactive selection of 4 target customer personas (Sarah, Mark, Elena, Alex) with heavily skewed historical preferences.
*   **Personalized Recommendation Grid:** Displays top 5 recommended items from a 15-product premium catalog, complete with category-specific colored cards, ratings, and pricing.
*   **Interactive Simulation Button:** Click "Simulate Purchase" on any recommended product card to record the action directly back into the streaming telemetry database, prompting immediate localized model retraining.
*   **Production Scaling Guide:** In-depth blueprints explaining **TensorFlow Recommenders (TFRS)** Two-Tower architectures and **Vertex AI Vectors (Matching Engine)** approximate nearest neighbor (ANN) retrieval.

### 🏗️ Tab 3: Cloud Architecture & Best Practices
*   **Infrastructure as Code (IaC):** Production-grade declarative **Terraform HCL** block declaring Pub/Sub topics, BigQuery datasets, clustered analytical tables, and Dataflow pipelines.
*   **BigQuery Data Warehouse Design:** Analysis of day-partitioning, multi-column clustering strategies, and a ready-to-run **BigQuery ML (BQML)** Implicit Matrix Factorization training script.
*   **Three-Pillar Security Matrix:** Hardening instructions covering Least Privilege Service Accounts (`gcloud` CLI examples), VPC Service Controls (VPC-SC) boundaries, and Cloud KMS Customer-Managed Encryption Keys (CMEK).

---

## 🚀 Getting Started

### Local Setup
1. **Clone this repository:**
   ```bash
   git clone https://github.com/Tick2003/OmniStream.git
   cd OmniStream
   ```
2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Launch the local Streamlit application:**
   ```bash
   streamlit run app.py
   ```

### Deploying to Streamlit Community Cloud
1. Link your GitHub account at **[share.streamlit.io](https://share.streamlit.io/)**.
2. Select this repository (`Tick2003/OmniStream`) and branch (`main`).
3. Set the entrypoint path to `app.py`.
4. Click **Deploy** to go live!

---

## 📋 Requirements
*   `streamlit>=1.30.0`
*   `pandas>=2.0.0`
*   `numpy>=1.24.0`
*   `scikit-learn>=1.2.0`
*   `plotly>=5.15.0`

---

*Disclaimer: This is a Proof of Concept application utilizing localized dataset simulations. No active GCP billable services or API credentials are required for local testing.*
