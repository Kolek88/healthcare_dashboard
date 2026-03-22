import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Healthcare Analytics Dashboard", layout="wide")
st.title(" Healthcare Analytics Dashboard")
st.markdown("An interactive overview of patient wait times and hospital metrics.")

# Load Data from CSV 
@st.cache_data
def load_data():
    df = pd.read_csv('hospital_data.csv')
    return df

try:
    df = load_data()
    
    # Data Processing
    def categorize_wait(wait_time):
        if wait_time > 60:
            return 'Critical'
        elif wait_time > 30:
            return 'Moderate'
        else:
            return 'On Time'
            
    df['status'] = df['wait_time_minutes'].apply(categorize_wait)
    
    # Get the top 10 longest wait times
    top_10_waits = df.sort_values(by='wait_time_minutes', ascending=False).drop_duplicates(subset=['name']).head(10)

    # 4. Dashboard Layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Patient Wait Times (Top 10 Longest)")
        
        # Recreate the Matplotlib Chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(top_10_waits['name'], top_10_waits['wait_time_minutes'], color='skyblue')
        
        ax.set_title('Top 10 Patient Wait Times')
        ax.set_xlabel('Patient Name')
        ax.set_ylabel('Minutes Waited')
        plt.xticks(rotation=45) 
        ax.axhline(y=60, color='r', linestyle='--', label='Critical Threshold (60m)')
        ax.legend()
        
        st.pyplot(fig)

    with col2:
        st.subheader("Wait Time Status Report")
        st.dataframe(
            top_10_waits[['name', 'wait_time_minutes', 'status']],
            column_config={
                "name": "Patient Name",
                "wait_time_minutes": "Wait (Mins)",
                "status": "Status"
            },
            hide_index=True,
            use_container_width=True
        )

except FileNotFoundError:
    st.error("Error: Could not find 'hospital_data.csv'. Please ensure the data file is in the same directory.")