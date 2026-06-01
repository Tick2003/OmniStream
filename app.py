# -*- coding: utf-8 -*-
"""
OmniStream - GCP AI Solutions Proof of Concept (PoC)
Author: Lead AI Solutions Architect, Google Cloud
Description: A highly interactive, professional, single-file Streamlit application 
             serving as an enterprise-grade PoC for real-time e-commerce recommendations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics.pairwise import cosine_similarity

# ==============================================================================
# 1. STREAMLIT PAGE CONFIGURATION & THEME
# ==============================================================================
st.set_page_config(
    page_title="OmniStream // GCP AI Solutions PoC",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Corporate CSS for Google Cloud Design Aesthetics
st.markdown("""
<style>
    /* Import modern typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;600;800&display=swap');

    /* Global styling overrides */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1A73E8 0%, #4285F4 50%, #34A853 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #B0B3B8;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Professional Sidebar custom style */
    .sidebar-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #1A73E8;
        margin-bottom: 1rem;
    }
    
    /* Elegant Custom KPI Cards styling */
    .kpi-container {
        background: #1E222B;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .kpi-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(26, 115, 232, 0.2);
    }
    
    .kpi-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #9AA0A6;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
        margin-bottom: 0.2rem;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .delta-up {
        color: #34A853;
    }
    
    .delta-down {
        color: #EA4335;
    }

    /* Product card aesthetics */
    .product-card {
        background: #1E222B;
        border-radius: 16px;
        padding: 0px;
        margin-bottom: 1.5rem;
        overflow: hidden;
        border: 1px solid #2D3139;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(26, 115, 232, 0.25);
        border-color: #4285F4;
    }
    
    .product-header-electronics {
        background: linear-gradient(135deg, #1A73E8 0%, #4285F4 100%);
        height: 120px;
        padding: 1rem;
        display: flex;
        align-items: flex-end;
    }
    
    .product-header-smarthome {
        background: linear-gradient(135deg, #0F9D58 0%, #34A853 100%);
        height: 120px;
        padding: 1rem;
        display: flex;
        align-items: flex-end;
    }
    
    .product-header-audio {
        background: linear-gradient(135deg, #F4B400 0%, #FBBC05 100%);
        height: 120px;
        padding: 1rem;
        display: flex;
        align-items: flex-end;
    }
    
    .product-header-accessories {
        background: linear-gradient(135deg, #AB47BC 0%, #8E24AA 100%);
        height: 120px;
        padding: 1rem;
        display: flex;
        align-items: flex-end;
    }
    
    .product-title {
        font-family: 'Outfit', sans-serif;
        color: white;
        font-size: 1.25rem;
        font-weight: 700;
        line-height: 1.2;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    
    .product-body {
        padding: 1.25rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .product-desc {
        color: #B0B3B8;
        font-size: 0.85rem;
        line-height: 1.4;
        margin-bottom: 0.8rem;
        height: 55px;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .product-price {
        font-size: 1.4rem;
        font-weight: 700;
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
        margin-bottom: 0.4rem;
    }
    
    .product-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
    }
    
    .product-rating {
        color: #FBBC05;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .category-badge {
        background: rgba(255, 255, 255, 0.1);
        color: #E8EAED;
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Technical narrative aesthetic container */
    .narrative-box {
        background: #15181F;
        border-left: 4px solid #1A73E8;
        border-radius: 4px 12px 12px 4px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Adjust Streamlit button styles inside product cards to be discrete */
    div.stButton > button {
        width: 100%;
        background-color: #1E222B;
        color: #4285F4;
        border: 1px solid #4285F4;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #4285F4 !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(66, 133, 244, 0.3);
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. STATIC INVENTORY & SYNTHETIC DATA ENGINE
# ==============================================================================

# Premium Google Cloud themed Retail Inventory (Static Mock Catalog)
PRODUCTS = [
    {"id": 101, "name": "Google Pixel 8 Pro", "category": "Electronics", "price": 999.00, "rating": 4.8, "desc": "Next-gen flagship smartphone featuring built-in Google Gemini Nano AI for advanced on-device reasoning."},
    {"id": 102, "name": "Pixel Watch 2", "category": "Electronics", "price": 349.00, "rating": 4.5, "desc": "Sleek biometric smartwatch with continuous heart-rate tracking and safety checks powered by advanced Fitbit algorithms."},
    {"id": 103, "name": "Nest Hub Max", "category": "Smart Home", "price": 229.00, "rating": 4.7, "desc": "Smart dashboard with a vibrant 10-inch HD display, stereo speakers, Nest Cam, and seamless Google Assistant control."},
    {"id": 104, "name": "Nest Wifi Pro", "category": "Smart Home", "price": 299.00, "rating": 4.6, "desc": "Tri-band Wi-Fi 6E mesh router system delivering blazing-fast, secure coverage for high-bandwidth enterprise streaming."},
    {"id": 105, "name": "Pixel Buds Pro", "category": "Premium Audio", "price": 199.00, "rating": 4.5, "desc": "Premium noise-canceling wireless earbuds featuring Silent Seal technology and spatial audio with head tracking."},
    {"id": 106, "name": "Chromecast 4K with Google TV", "category": "Electronics", "price": 49.00, "rating": 4.4, "desc": "Crystal-clear 4K HDR media streamer featuring tailored personalized recommendations and smart home device controls."},
    {"id": 107, "name": "Nest Learning Thermostat", "category": "Smart Home", "price": 249.00, "rating": 4.8, "desc": "Self-programming, energy-efficient smart thermostat that adapts to your home schedule and local weather patterns."},
    {"id": 108, "name": "Nest Doorbell (Wired)", "category": "Smart Home", "price": 179.00, "rating": 4.3, "desc": "Intelligent video doorbell featuring 24/7 continuous recording, high HDR definition, and advanced object detection."},
    {"id": 109, "name": "Google Pixel Tablet", "category": "Electronics", "price": 499.00, "rating": 4.6, "desc": "Premium 11-inch Android tablet featuring an innovative, magnetic charging speaker dock for hub integration."},
    {"id": 110, "name": "Fitbit Charge 6", "category": "Accessories", "price": 159.00, "rating": 4.4, "desc": "Advanced fitness tracker with built-in GPS, active heart-rate zones, and direct controls for YouTube Music and Google Maps."},
    {"id": 111, "name": "Pixel Fold", "category": "Electronics", "price": 1799.00, "rating": 4.2, "desc": "Ultra-thin, dual-screen folding smartphone offering exceptional split-screen multi-tasking and professional multitasking features."},
    {"id": 112, "name": "Nest Cam (Outdoor)", "category": "Smart Home", "price": 189.00, "rating": 4.5, "desc": "Weatherproof intelligent security camera with high resolution, infrared night vision, and immediate threat alerts."},
    {"id": 113, "name": "Google Coral Dev Board", "category": "Electronics", "price": 119.00, "rating": 4.9, "desc": "Single-board hardware kit featuring an integrated Edge TPU coprocessor for high-speed local machine learning inference."},
    {"id": 114, "name": "Fitbit Sense 2", "category": "Accessories", "price": 249.00, "rating": 4.3, "desc": "Advanced health smartwatch with a continuous electrodermal activity (cEDA) sensor for active stress tracking."},
    {"id": 115, "name": "Pixel Stand (2nd Gen)", "category": "Accessories", "price": 79.00, "rating": 4.5, "desc": "Rapid 23W wireless charger designed for Pixel devices, featuring an integrated cooling fan and smart charging modes."}
]

@st.cache_data
def load_initial_clickstream_dataset():
    """
    Generates a high-quality, synthetic historical dataset of e-commerce clickstream events.
    Includes 50 baseline users and 4 primary enterprise personas skewed heavily 
    toward specific category preferences to show real-world Collaborative Filtering.
    """
    user_ids = [f"USR_{i}" for i in range(1001, 1051)]
    
    events = []
    actions = ["View", "Cart", "Purchase"]
    action_probs = [0.70, 0.20, 0.10] # Realistic conversions: 70% views, 20% carts, 10% purchases
    
    np.random.seed(42)
    start_time = datetime.datetime.now() - datetime.timedelta(hours=6)
    
    # 1. Baseline random clickstream traffic
    for _ in range(400):
        uid = np.random.choice(user_ids)
        prod = np.random.choice(PRODUCTS)
        act = np.random.choice(actions, p=action_probs)
        # Random spacing over the past 6 hours
        time_offset = np.random.randint(1, 21600)
        timestamp = start_time + datetime.timedelta(seconds=time_offset)
        events.append({
            "User_ID": uid,
            "Item_ID": prod["id"],
            "Item_Name": prod["name"],
            "Category": prod["category"],
            "Action": act,
            "Timestamp": timestamp,
            "Price": prod["price"]
        })
        
    # 2. Skewed behavioral history for target personas
    
    # Persona: Sarah (Cloud Architect) -> Heavily buys enterprise electronics & developer kits
    sarah_prods = [p for p in PRODUCTS if p["id"] in [101, 109, 111, 113, 105]]
    for _ in range(25):
        prod = np.random.choice(sarah_prods)
        act = np.random.choice(actions, p=[0.55, 0.30, 0.15])
        time_offset = np.random.randint(1, 21600)
        timestamp = start_time + datetime.timedelta(seconds=time_offset)
        events.append({
            "User_ID": "USR_SARAH",
            "Item_ID": prod["id"],
            "Item_Name": prod["name"],
            "Category": prod["category"],
            "Action": act,
            "Timestamp": timestamp,
            "Price": prod["price"]
        })
        
    # Persona: Mark (Smart Home Builder) -> Heavily buys Nest/Smart Home automation devices
    mark_prods = [p for p in PRODUCTS if p["category"] == "Smart Home"]
    for _ in range(25):
        prod = np.random.choice(mark_prods)
        act = np.random.choice(actions, p=[0.55, 0.30, 0.15])
        time_offset = np.random.randint(1, 21600)
        timestamp = start_time + datetime.timedelta(seconds=time_offset)
        events.append({
            "User_ID": "USR_MARK",
            "Item_ID": prod["id"],
            "Item_Name": prod["name"],
            "Category": prod["category"],
            "Action": act,
            "Timestamp": timestamp,
            "Price": prod["price"]
        })
        
    # Persona: Elena (Fitness Enthusiast) -> Focused heavily on wearable accessories & audio
    elena_prods = [p for p in PRODUCTS if p["id"] in [110, 114, 102, 105, 115]]
    for _ in range(25):
        prod = np.random.choice(elena_prods)
        act = np.random.choice(actions, p=[0.55, 0.30, 0.15])
        time_offset = np.random.randint(1, 21600)
        timestamp = start_time + datetime.timedelta(seconds=time_offset)
        events.append({
            "User_ID": "USR_ELENA",
            "Item_ID": prod["id"],
            "Item_Name": prod["name"],
            "Category": prod["category"],
            "Action": act,
            "Timestamp": timestamp,
            "Price": prod["price"]
        })
        
    # Persona: Alex (Developer & Maker) -> Tech gadgets, Google TV, Wifi Pro
    alex_prods = [p for p in PRODUCTS if p["id"] in [113, 104, 106, 101, 109]]
    for _ in range(25):
        prod = np.random.choice(alex_prods)
        act = np.random.choice(actions, p=[0.60, 0.25, 0.15])
        time_offset = np.random.randint(1, 21600)
        timestamp = start_time + datetime.timedelta(seconds=time_offset)
        events.append({
            "User_ID": "USR_ALEX",
            "Item_ID": prod["id"],
            "Item_Name": prod["name"],
            "Category": prod["category"],
            "Action": act,
            "Timestamp": timestamp,
            "Price": prod["price"]
        })

    df = pd.DataFrame(events)
    # Sort chronologically
    df = df.sort_values(by="Timestamp").reset_index(drop=True)
    return df

# Initialize Session State Data Store to simulate real-time ingestion mutability
if "clickstream_df" not in st.session_state:
    st.session_state.clickstream_df = load_initial_clickstream_dataset()

# Cache control for simulated background streaming loop
if "is_streaming" not in st.session_state:
    st.session_state.is_streaming = False

# ==============================================================================
# 3. COLLABORATIVE FILTERING ENGINE (SCIKIT-LEARN)
# ==============================================================================

def train_collaborative_filtering_model(df_events, target_user, inventory_products, top_n=5):
    """
    Computes a localized, scientific Collaborative Filtering Recommendation Engine
    based on a User-Item Interaction Matrix. Uses interaction weights:
    View = 1.0, Cart = 3.0, Purchase = 5.0. Computes Cosine Similarity across
    users to make predictive recommendations.
    """
    # 1. Map interactions to weights
    weight_map = {"View": 1.0, "Cart": 3.0, "Purchase": 5.0}
    df_weighted = df_events.copy()
    df_weighted["Weight"] = df_weighted["Action"].map(weight_map)
    
    # 2. Build Pivoted User-Item Interaction Matrix (User_ID is index, Item_ID is column)
    # Aggregate by sum of interaction weights (indicating high interest for repeated clicks)
    user_item_matrix = df_weighted.groupby(["User_ID", "Item_ID"])["Weight"].sum().unstack(fill_value=0.0)
    
    # 3. Ensure all products in the catalog are represented as columns
    for prod in inventory_products:
        if prod["id"] not in user_item_matrix.columns:
            user_item_matrix[prod["id"]] = 0.0
            
    # Normalize order of columns
    user_item_matrix = user_item_matrix.reindex(sorted(user_item_matrix.columns), axis=1)
    
    # 4. Fallback if the selected user does not exist in our history yet
    if target_user not in user_item_matrix.index:
        popularity_scores = df_weighted.groupby("Item_ID")["Weight"].sum().sort_values(ascending=False)
        top_ids = list(popularity_scores.index[:top_n])
        return [p for p in inventory_products if p["id"] in top_ids]
        
    # Convert matrix to numpy array for Cosine Similarity
    matrix_values = user_item_matrix.values
    
    # 5. Compute user-to-user cosine similarities
    user_similarities = cosine_similarity(matrix_values)
    user_sim_df = pd.DataFrame(
        user_similarities, 
        index=user_item_matrix.index, 
        columns=user_item_matrix.index
    )
    
    # Get target user's interaction profile
    target_profile = user_item_matrix.loc[target_user]
    
    # Extract similar users (excluding the target user themselves)
    similar_users = user_sim_df[target_user].drop(target_user).sort_values(ascending=False)
    
    # Extract top 5 nearest neighbor users
    top_neighbors = similar_users.head(5)
    
    # Recommend products the target user has NOT purchased yet (Purchase weight >= 5.0)
    # We want to identify items where the user's current interaction state is either 0 or has no purchase
    # Find items already purchased by the user
    purchased_items = df_weighted[(df_weighted["User_ID"] == target_user) & (df_weighted["Action"] == "Purchase")]["Item_ID"].unique()
    
    predicted_rankings = {}
    
    # Predict weighted scores for all other products
    for item_id in user_item_matrix.columns:
        if item_id in purchased_items:
            continue # Do not recommend already purchased products
            
        weighted_score_sum = 0.0
        similarity_weight_sum = 0.0
        
        for neighbor, sim_score in top_neighbors.items():
            neighbor_rating = user_item_matrix.loc[neighbor, item_id]
            if neighbor_rating > 0:
                weighted_score_sum += sim_score * neighbor_rating
                similarity_weight_sum += sim_score
                
        if similarity_weight_sum > 0:
            predicted_rankings[item_id] = weighted_score_sum / similarity_weight_sum
        else:
            # Subtle popularity fallback factor to fill recommendations
            pop_score = df_weighted[df_weighted["Item_ID"] == item_id]["Weight"].sum()
            predicted_rankings[item_id] = pop_score * 0.001
            
    # Sort items based on predicted matrix scores
    recommended_ids = sorted(predicted_rankings, key=predicted_rankings.get, reverse=True)[:top_n]
    
    # Make sure we have exactly top_n elements
    if len(recommended_ids) < top_n:
        # Fill remaining with general popular items
        popularity_list = df_weighted.groupby("Item_ID")["Weight"].sum().sort_values(ascending=False).index
        for item_id in popularity_list:
            if item_id not in recommended_ids and item_id not in purchased_items:
                recommended_ids.append(item_id)
                if len(recommended_ids) == top_n:
                    break
                    
    # Map back to full product details from catalog
    recommended_products = [p for p in inventory_products if p["id"] in recommended_ids]
    # Maintain the sorted prediction order
    recommended_products.sort(key=lambda x: recommended_ids.index(x["id"]))
    
    return recommended_products


# ==============================================================================
# 4. SIDEBAR - SIMULATION & CONTROL PANEL
# ==============================================================================

with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ PoC Control Center</div>', unsafe_allow_html=True)
    st.markdown("Use this console to control the simulated real-time telemetry streaming into the GCP architecture.")
    
    st.write("---")
    
    # Active Pipeline Telemetry Ingestion Controls
    st.subheader("Live Pipeline Controls")
    
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        if st.button("🚀 Ingest Spike", help="Simulate a sudden burst of 20 high-velocity user actions."):
            # Generate 20 new events
            new_events = []
            actions = ["View", "Cart", "Purchase"]
            user_ids = [f"USR_{i}" for i in range(1001, 1051)] + ["USR_SARAH", "USR_MARK", "USR_ELENA", "USR_ALEX"]
            for _ in range(20):
                prod = np.random.choice(PRODUCTS)
                act = np.random.choice(actions, p=[0.6, 0.3, 0.1])
                timestamp = datetime.datetime.now()
                new_events.append({
                    "User_ID": np.random.choice(user_ids),
                    "Item_ID": prod["id"],
                    "Item_Name": prod["name"],
                    "Category": prod["category"],
                    "Action": act,
                    "Timestamp": timestamp,
                    "Price": prod["price"]
                })
            st.session_state.clickstream_df = pd.concat([
                st.session_state.clickstream_df, 
                pd.DataFrame(new_events)
            ]).reset_index(drop=True)
            st.toast("⚡ High-velocity ingestion spike processed!", icon="⚡")
            
    with col_sim2:
        if st.button("🧹 Reset Data", help="Reset telemetry back to original seed data."):
            st.session_state.clickstream_df = load_initial_clickstream_dataset()
            st.toast("Telemetry data reset to initial baseline.", icon="🧹")
            st.rerun()

    # Streaming Loop Trigger Toggle
    st.session_state.is_streaming = st.checkbox(
        "🔄 Enable Active Background Stream", 
        value=st.session_state.is_streaming,
        help="Runs an automated telemetry stream adding 3 clickstream events every second."
    )
    
    st.write("---")
    
    # GCP Architecture Tags
    st.markdown("### Powered by Google Cloud")
    st.info("""
    **Production Tech Stack:**
    *   **Ingestion:** GCP Pub/Sub (Global Queue)
    *   **Data Processing:** Google Cloud Dataflow
    *   **Data Warehouse:** BigQuery (Streaming Buffer)
    *   **ML Platform:** Vertex AI Distributed Pipelines
    *   **Serving Engine:** Vertex AI Vector Search
    """)
    
    st.caption("Google Cloud Solutions Architecture PoC • Version 1.2.0")


# ==============================================================================
# MAIN PAGE LAYOUT & APP HEADER
# ==============================================================================
st.markdown('<div class="main-title">OmniStream ☁️</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Google Cloud AI Solutions Architect • Real-Time E-Commerce Recommendation PoC</div>', unsafe_allow_html=True)

# Main Application Tabs
tab1, tab2, tab3 = st.tabs([
    "📈 Real-Time Event Ingestion (Simulated)", 
    "🔮 Vertex AI Recommendation Engine", 
    "🏗️ Enterprise GCP Cloud Architecture"
])


# ==============================================================================
# TAB 1: REAL-TIME EVENT INGESTION (SIMULATED DATAFLOW)
# ==============================================================================
with tab1:
    st.header("Streamlit-Simulated Clickstream Pipeline")
    st.write(
        "This tab simulates high-velocity user actions streaming globally into Google Cloud. "
        "Toggle the active background stream in the sidebar to witness real-time metric updates and interactive chart repaints."
    )
    
    # Continuous Streaming Execution Frame
    if st.session_state.is_streaming:
        # Ingest 3 random events
        actions = ["View", "Cart", "Purchase"]
        user_ids = [f"USR_{i}" for i in range(1001, 1051)] + ["USR_SARAH", "USR_MARK", "USR_ELENA", "USR_ALEX"]
        new_events = []
        for _ in range(3):
            prod = np.random.choice(PRODUCTS)
            act = np.random.choice(actions, p=[0.70, 0.22, 0.08])
            timestamp = datetime.datetime.now()
            new_events.append({
                "User_ID": np.random.choice(user_ids),
                "Item_ID": prod["id"],
                "Item_Name": prod["name"],
                "Category": prod["category"],
                "Action": act,
                "Timestamp": timestamp,
                "Price": prod["price"]
            })
        st.session_state.clickstream_df = pd.concat([
            st.session_state.clickstream_df, 
            pd.DataFrame(new_events)
        ]).reset_index(drop=True)
        # Sleep and Rerun to create simulated loop
        time.sleep(0.7)
        st.rerun()

    df_current = st.session_state.clickstream_df.copy()
    
    # ----------------- LIVE METRICS PANEL -----------------
    # Compute calculations dynamically based on state
    total_events = len(df_current)
    active_users = df_current["User_ID"].nunique()
    total_revenue = df_current[df_current["Action"] == "Purchase"]["Price"].sum()
    
    # Compute active Events per Second (EPS) based on recent timestamp logs (last 30 seconds)
    recent_cutoff = datetime.datetime.now() - datetime.timedelta(seconds=60)
    # Check if we have standard string or timestamps in the dataframe
    df_current["Timestamp"] = pd.to_datetime(df_current["Timestamp"])
    recent_events = df_current[df_current["Timestamp"] >= recent_cutoff]
    simulated_eps = len(recent_events) / 60.0 if len(recent_events) > 0 else np.random.uniform(1.2, 3.8)
    if simulated_eps < 1.0:
        simulated_eps = np.random.uniform(1.2, 4.5)
        
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.markdown(f"""
        <div class="kpi-container" style="border-left: 5px solid #1A73E8;">
            <div class="kpi-label">Ingestion Velocity</div>
            <div class="kpi-value">{simulated_eps:.2f} EPS</div>
            <div class="kpi-delta"><span class="delta-up">▲ Live Streaming</span> (Pub/Sub Queue)</div>
        </div>
        """, unsafe_allow_html=True)
        
    with metric_col2:
        st.markdown(f"""
        <div class="kpi-container" style="border-left: 5px solid #FBBC05;">
            <div class="kpi-label">Active Users Tracked</div>
            <div class="kpi-value">{active_users:,} Users</div>
            <div class="kpi-delta"><span class="delta-up">▲ +{np.random.randint(1,4)} online</span> dynamically scaling</div>
        </div>
        """, unsafe_allow_html=True)
        
    with metric_col3:
        st.markdown(f"""
        <div class="kpi-container" style="border-left: 5px solid #34A853;">
            <div class="kpi-label">Simulated Live Revenue</div>
            <div class="kpi-value">${total_revenue:,.2f}</div>
            <div class="kpi-delta"><span class="delta-up">▲ 100% conversion tracking</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # ----------------- VISUALIZATIONS -----------------
    chart_col1, chart_col2 = st.columns([2, 1])
    
    with chart_col1:
        st.subheader("Clickstream Velocity & Event Time-Series")
        # Bin timestamps to 30-second windows for smooth plotting
        df_current["Time_Bin"] = df_current["Timestamp"].dt.round("30s")
        time_series_data = df_current.groupby(["Time_Bin", "Action"]).size().reset_index(name="Event_Count")
        
        # Take only the last 30 intervals to show a clean moving dashboard
        time_series_data = time_series_data.tail(90)
        
        fig_time = px.area(
            time_series_data,
            x="Time_Bin",
            y="Event_Count",
            color="Action",
            color_discrete_map={"View": "#4285F4", "Cart": "#FBBC05", "Purchase": "#34A853"},
            labels={"Time_Bin": "Time Log", "Event_Count": "Events per Window"},
            template="plotly_dark"
        )
        fig_time.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=10, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_time, use_container_width=True)

    with chart_col2:
        st.subheader("Event Share Breakdown")
        action_counts = df_current["Action"].value_counts().reset_index()
        action_counts.columns = ["Action", "Count"]
        
        fig_pie = px.pie(
            action_counts,
            values="Count",
            names="Action",
            hole=0.4,
            color="Action",
            color_discrete_map={"View": "#4285F4", "Cart": "#FBBC05", "Purchase": "#34A853"},
            template="plotly_dark"
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=10, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ----------------- RECENT INGESTED LOGGER -----------------
    with st.expander("🔎 View Raw Clickstream Ingestion Logs (Last 10 Events)"):
        st.dataframe(
            df_current.sort_values(by="Timestamp", ascending=False).head(10)[
                ["Timestamp", "User_ID", "Item_Name", "Category", "Action", "Price"]
            ],
            use_container_width=True
        )

    # ----------------- ARCHITECT NARRATIVE -----------------
    st.markdown("""
    <div class="narrative-box">
        <h3>🧑‍💻 GCP Enterprise Stream Ingestion Narrative</h3>
        <p>In a production-ready enterprise deployment on Google Cloud Platform, this high-velocity clickstream ingest flows seamlessly over a managed Serverless infrastructure:</p>
        <ol>
            <li><b>Google Cloud Pub/Sub:</b> Actively ingests clickstream event payloads globally via standard HTTPS edge points. Handles millions of requests per second with horizontal, out-of-the-box scaling.</li>
            <li><b>Google Cloud Dataflow (Apache Beam):</b> Subscribes to the Pub/Sub topic to process events. Performs stateful deduplication, windowed metrics aggregations (e.g., 30-second sliding time windows), and enriches records with catalog product data.</li>
            <li><b>BigQuery Streaming API:</b> Ingests refined stream logs from Dataflow directly into the raw analytical tables at sub-second latency, bypassing the need for batch loads (ELT pattern).</li>
        </ol>
        <p><i>Architecture Diagram:</i></p>
        <pre style="background: #11141A; border: 1px solid #2D3139; color: #FFFFFF; padding: 10px; border-radius: 6px; font-family: monospace;">
[User Client Click] ➔ [Pub/Sub Topic] ➔ [Dataflow Stream Job (Beam)] ➔ [BigQuery Ingestion Storage]
                                                               ➔ [Vertex AI Feature Store]
        </pre>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2: VERTEX AI RECOMMENDATION ENGINE (SIMULATED CF PLATFORM)
# ==============================================================================
with tab2:
    st.header("Localized ML Recommendation Engine")
    st.write(
        "Select a User Persona to load their real-time telemetry clickstream profile. "
        "We dynamically fit a **User-User Collaborative Filtering model** (Cosine Similarity) via Scikit-Learn to predict and render the top 5 product recommendations."
    )
    
    # 1. USER PROFILE SELECTION
    personas_options = {
        "Sarah (Cloud Architect Persona)": "USR_SARAH",
        "Mark (Smart Home Enthusiast Persona)": "USR_MARK",
        "Elena (Active Fitness Athlete Persona)": "USR_ELENA",
        "Alex (Hardware Dev & Maker Persona)": "USR_ALEX"
    }
    
    selected_name = st.selectbox(
        "Select User Profile Profile:", 
        options=list(personas_options.keys())
    )
    target_user_id = personas_options[selected_name]

    # Display persona's history
    df_persona_history = df_current[df_current["User_ID"] == target_user_id]
    
    hist_col1, hist_col2 = st.columns([1, 2])
    with hist_col1:
        st.markdown(f"### Persona: `{target_user_id}`")
        st.markdown(f"**Total Registered Interactions:** `{len(df_persona_history)}` events")
        
        # Breakdown by action
        act_summary = df_persona_history["Action"].value_counts()
        for act in ["View", "Cart", "Purchase"]:
            cnt = act_summary.get(act, 0)
            st.caption(f"• **{act}s:** {cnt}")
            
    with hist_col2:
        st.subheader("Recent Customer Telemetry Logs")
        if not df_persona_history.empty:
            st.dataframe(
                df_persona_history.sort_values(by="Timestamp", ascending=False).head(5)[
                    ["Timestamp", "Item_Name", "Category", "Action", "Price"]
                ],
                use_container_width=True
            )
        else:
            st.warning("No interactions registered yet. Add interactions to train model.")

    st.write("---")

    # 2. RUN SCIKIT-LEARN COLLABORATIVE FILTERING MODEL
    with st.spinner("Re-training Collaborative Filtering model on streaming matrix..."):
        recs = train_collaborative_filtering_model(
            df_current, 
            target_user=target_user_id, 
            inventory_products=PRODUCTS, 
            top_n=5
        )
    
    st.subheader("🔮 Recommended Products for You (Top 5 Personalized Recommendations)")
    
    # Render recommended items dynamically with custom aesthetic cards
    cols = st.columns(5)
    
    for idx, item in enumerate(recs):
        # Determine CSS styling based on product category
        category = item["category"]
        if category == "Electronics":
            header_class = "product-header-electronics"
        elif category == "Smart Home":
            header_class = "product-header-smarthome"
        elif category == "Premium Audio":
            header_class = "product-header-audio"
        else:
            header_class = "product-header-accessories"
            
        with cols[idx]:
            st.markdown(f"""
            <div class="product-card">
                <div class="{header_class}">
                    <div class="product-title">{item["name"]}</div>
                </div>
                <div class="product-body">
                    <div class="product-meta">
                        <span class="category-badge">{category}</span>
                        <span class="product-rating">⭐ {item["rating"]}</span>
                    </div>
                    <div class="product-desc">{item["desc"]}</div>
                    <div class="product-price">${item["price"]:.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive Button to simulate conversions dynamically!
            if st.button(f"Simulate Purchase", key=f"rec_{item['id']}_{idx}"):
                # Add a purchase event to the session state to simulate immediate pipeline feedback loop
                purchase_event = {
                    "User_ID": target_user_id,
                    "Item_ID": item["id"],
                    "Item_Name": item["name"],
                    "Category": item["category"],
                    "Action": "Purchase",
                    "Timestamp": datetime.datetime.now(),
                    "Price": item["price"]
                }
                st.session_state.clickstream_df = pd.concat([
                    st.session_state.clickstream_df, 
                    pd.DataFrame([purchase_event])
                ]).reset_index(drop=True)
                st.toast(f"🎉 Simulated Purchase of '{item['name']}' logged immediately to pipeline!", icon="🛒")
                time.sleep(0.5)
                st.rerun()

    st.write("---")

    # ----------------- ARCHITECT RECOMMENDATION NARRATIVE -----------------
    st.markdown("""
    <div class="narrative-box">
        <h3>🧬 Scaling to Production: Vertex AI Recommendation Architecture</h3>
        <p>While this local PoC executes Cosine Similarity on user matrices inside memory using <b>Scikit-Learn</b>, a high-impact global enterprise deployment scales utilizing <b>Google Cloud Vertex AI</b>:</p>
        <ul>
            <li><b>Two-Tower Model Architecture:</b> Models are trained using <b>TensorFlow Recommenders (TFRS)</b>, dividing recommendations into two deep neural networks:
                <ul>
                    <li><i>Query (User) Tower:</i> Maps real-time customer behavior, session contexts, and user profiles to a joint vector space.</li>
                    <li><i>Candidate (Product) Tower:</i> Embeds the catalog inventory into the same vector space.</li>
                </ul>
            </li>
            <li><b>Vertex AI Pipelines (Kubeflow Orchestrator):</b> Schedules automated retraining pipelines in response to BigQuery events or daily batch updates. The pipeline extracts clickstream metrics, trains the TFRS model, runs validation audits, and exports updated embeddings to Cloud Storage.</li>
            <li><b>Vertex AI Vector Search (Matching Engine):</b> Serves predictions at millisecond scale. Rather than computing expensive similarity loops in application web layers, candidate item embeddings are deployed onto Vertex AI Vector Search endpoints, allowing high-throughput, low-latency approximate nearest neighbor (ANN) retrieval at under 10ms.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# TAB 3: GCP SECURITY, MULTI-TENANCY & IACO
# ==============================================================================
with tab3:
    st.header("Enterprise Cloud Architecture & Foundations")
    st.write(
        "This architectural guide details the enterprise layout for deploying "
        "scalable, secure, and multi-tenant e-commerce recommendation pipelines on Google Cloud Platform."
    )
    
    # ----------------- SUB-TAB LAYOUT -----------------
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "🤖 Infrastructure as Code (Terraform)",
        "🗄️ BigQuery Data Warehouse Schema",
        "🔐 Identity, Security & IAM Practices"
    ])
    
    with sub_tab1:
        st.subheader("1. Multi-Tenant Infrastructure Provisioning")
        st.markdown(
            "Enterprise systems must isolate developer environments and provision components consistently. "
            "Below is a standard declarative **Terraform HCL** block illustrating how to declare the core pipeline assets "
            "including a Pub/Sub ingestion queue, Dataflow job, and highly optimized BigQuery tables."
        )
        
        # Terraform HCL Code Snippet
        st.code("""
# ==============================================================================
# OMNISTREAM INFRASTRUCTURE PROVISIONING - PRODUCTION ARCHITECTURE
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.10.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# 1. Decoupled Clickstream Event Queue (Pub/Sub)
resource "google_pubsub_topic" "clickstream_topic" {
  name = "omnistream-clickstream-ingest-prod"
  labels = {
    environment = "production"
    data_tier   = "ingestion"
  }
  
  message_storage_policy {
    allowed_persistence_regions = [var.gcp_region]
  }
}

# 2. BigQuery Analytics Storage Dataset
resource "google_bigquery_dataset" "omnistream_dataset" {
  dataset_id                  = "omnistream_analytics_prod"
  friendly_name               = "OmniStream Analytics Data Warehouse"
  description                 = "Contains historical and streaming e-commerce clickstream records."
  location                    = "US"
  default_table_expiration_ms = 31536000000 # 365 Days Retention Policy
  
  labels = {
    environment = "production"
    compliance  = "gdpr-hipaa"
  }
}

# 3. Partitioned & Clustered Clickstream Table
resource "google_bigquery_table" "clickstream_events" {
  dataset_id = google_bigquery_dataset.omnistream_dataset.dataset_id
  table_id   = "clickstream_events_raw"
  
  # Partition by Event Time for cost-effective analytical scanning
  time_partitioning {
    type  = "DAY"
    field = "timestamp"
  }
  
  # Cluster by User ID and Action Type for high-performance recommendation filtering
  clustering = ["user_id", "action"]
  
  schema = <<EOF
[
  {"name": "user_id", "type": "STRING", "mode": "REQUIRED", "description": "Unique e-commerce customer identifier"},
  {"name": "item_id", "type": "INTEGER", "mode": "REQUIRED", "description": "Unique retail item ID"},
  {"name": "item_name", "type": "STRING", "mode": "NULLABLE", "description": "Canonical product name"},
  {"name": "category", "type": "STRING", "mode": "NULLABLE", "description": "Product department tag"},
  {"name": "action", "type": "STRING", "mode": "REQUIRED", "description": "View, Cart, or Purchase action"},
  {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED", "description": "UTC timestamp of the customer action"},
  {"name": "price", "type": "FLOAT", "mode": "NULLABLE", "description": "Unit list price of the product"}
]
EOF
}

# 4. Stream Processing Engine (Dataflow Template Deployment)
resource "google_dataflow_flex_template_job" "dataflow_streaming_pipeline" {
  name            = "omnistream-pubsub-to-bigquery"
  container_spec_gcs_path = "gs://dataflow-templates-${var.gcp_region}/latest/PubSub_to_BigQuery_Flex"
  
  parameters = {
    inputTopic      = google_pubsub_topic.clickstream_topic.id
    outputTableSpec = "${var.gcp_project_id}:${google_bigquery_table.clickstream_events.dataset_id}.${google_bigquery_table.clickstream_events.table_id}"
  }
}
        """, language="hcl")
        
    with sub_tab2:
        st.subheader("2. BigQuery Data Warehouse Schema Optimizations")
        st.markdown(
            "To support high-velocity real-time recommendation updates, "
            "BigQuery datasets must be optimized for both stream ingestion and fast queries."
        )
        
        # Partitioning & Clustering Explanation Table
        st.markdown("""
        ### Optimized Warehouse Strategies
        
        | Strategy | Architectural Implementation | Practical PoC Impact |
        | :--- | :--- | :--- |
        | **Day-level Partitioning** | Partitioned on `timestamp` (Day) | Restricts analytical queries from scanning entire historical tables, slashing GCP BigQuery computing costs by up to 90%. |
        | **Multi-Column Clustering** | Clustered on `[user_id, action]` | Colocates customer profile interactions in disk blocks. Speeds up Scikit-Learn matrix extraction or model retraining queries by orders of magnitude. |
        | **Streaming Ingestion Buffer** | Utilizing BigQuery Write API | Standardizes millisecond-latency streaming ingest directly into analytical partitions, eliminating batch ETL overhead. |
        | **BigQuery ML (BQML)** | Collaborative Filtering Matrix Factorization | Enables rapid ML recommendations directly inside BigQuery via a SQL statement (e.g., `CREATE MODEL ... OPTIONS(model_type='matrix_factorization')`). |
        """)
        
        # BQML Code Snippet
        st.write("#### Rapid Prototyping: Train recommendation matrix directly in BigQuery with SQL:")
        st.code("""
CREATE OR REPLACE MODEL `omnistream_analytics_prod.recommendation_model`
OPTIONS(
  model_type='matrix_factorization',
  user_col='user_id',
  item_col='item_id',
  rating_col='interaction_weight',
  feedback_type='implicit'
) AS
SELECT 
  user_id, 
  item_id, 
  CASE 
    WHEN action = 'Purchase' THEN 5.0
    WHEN action = 'Cart' THEN 3.0
    ELSE 1.0 
  END AS interaction_weight
FROM 
  `omnistream_analytics_prod.clickstream_events_raw`
WHERE 
  timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
        """, language="sql")
        
    with sub_tab3:
        st.subheader("3. IAM Identity, VPC Service Controls & CMEK")
        st.markdown(
            "Securing production customer telemetry requires hardening standard service authorization pipelines. "
            "Google Cloud Solutions recommends the following three-pillar security architecture:"
        )
        
        st.markdown("""
        ### 🛡️ Three-Pillar Production Security Matrix
        
        #### Pillar A: Least Privilege Service Accounts (IAM)
        Never reuse default Compute Engine or App Engine service accounts for live streaming data. In production:
        1. **Dataflow Pipeline Worker:** Granted `roles/pubsub.subscriber` on the ingestion topic and `roles/bigquery.dataEditor` on the target warehouse.
        2. **Vertex AI Training Pipeline:** Granted read access (`roles/bigquery.dataViewer`) to BigQuery inputs and read/write access to Cloud Storage training models (`roles/storage.objectAdmin`).
        3. **Application API Client:** Granted `roles/aiplatform.user` to invoke Vertex AI Vector Search endpoint vectors, with zero access to underlying BigQuery datasets.
        
        #### Pillar B: Network Hardening via VPC Service Controls (VPC-SC)
        *   Establish a secure virtual network boundary around BigQuery, Vertex AI, and Cloud Storage using **VPC Service Controls**.
        *   Mitigates data exfiltration risks by blocking unauthorized API requests originating outside the trusted perimeter, even if valid credentials or active IAM keys are intercepted.
        
        #### Pillar C: Customer-Managed Encryption Keys (CMEK)
        *   Configure Cloud Key Management Service (KMS) to encrypt clickstream files at rest in BigQuery and Cloud Storage buckets.
        *   Allows operations teams to dynamically revoke access keys, rendering analytical data unreadable in compliance with high-level corporate data sovereignty regulations.
        """)
        
        # IAM Shell Command Snippet
        st.write("#### Enterprise CLI Automation Example (Assigning Dataflow least privilege role):")
        st.code("""
# Create dedicated, isolated Service Account
gcloud iam service-accounts create omnistream-dataflow-worker \
    --description="Service account to run Dataflow clickstream processing" \
    --display-name="OmniStream Dataflow Worker"

# Bind Pub/Sub Subscriber access
gcloud projects add-iam-policy-binding enterprise-gcp-project-prod \
    --member="serviceAccount:omnistream-dataflow-worker@enterprise-gcp-project-prod.iam.gserviceaccount.com" \
    --role="roles/pubsub.subscriber"

# Bind BigQuery Data Editor access
gcloud projects add-iam-policy-binding enterprise-gcp-project-prod \
    --member="serviceAccount:omnistream-dataflow-worker@enterprise-gcp-project-prod.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"
        """, language="bash")

# ==============================================================================
# FOOTER
# ==============================================================================
st.write("---")
col_foot1, col_foot2 = st.columns([2, 1])
with col_foot1:
    st.caption("Disclaimer: This Proof of Concept application uses localized simulation for telemetry and matrix calculations. No actual GCP billable services or API keys are required for local testing.")
with col_foot2:
    st.markdown("<p style='text-align: right; color:#9AA0A6; font-size:0.8rem;'>Google Cloud Professional Services • Architecture PoC</p>", unsafe_allow_html=True)
