"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Page Config
st.set_page_config(page_title="Learning Mode Survey", layout="wide")
st.title("📊 Online vs. Offline Learning Analysis")

# --- DATA STORAGE LOGIC ---
# We use a CSV file to store real user inputs permanently
DATA_FILE = "survey_responses.csv"


def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=['Age', 'Preferred_Mode', 'Avg_Daily_Study_Hours', 'Engagement_Level', 'Internet_Issue',
                                 'Understanding_Rating'])


def save_data(new_row):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


# --- SIDEBAR INPUT FORM ---
st.sidebar.header("Submit Your Response")
with st.sidebar.form("survey_form"):
    age = st.number_input("Age", 15, 50, 20)
    mode = st.selectbox("Preferred Mode", ["Online", "Offline", "Hybrid"])
    hours = st.slider("Daily Study Hours", 0.0, 12.0, 4.0)
    engagement = st.slider("Engagement Level (1-10)", 1, 10, 5)
    internet = st.radio("Internet Issues?", ["Yes", "No"])
    understanding = st.slider("Understanding Rating (1-10)", 1, 10, 5)

    submit = st.form_submit_button("Submit Data")

if submit:
    new_entry = {
        'Age': age, 'Preferred_Mode': mode, 'Avg_Daily_Study_Hours': hours,
        'Engagement_Level': engagement, 'Internet_Issue': internet, 'Understanding_Rating': understanding
    }
    save_data(new_entry)
    st.sidebar.success("Response recorded!")

# --- VISUALIZATION SECTION ---
df = load_data()

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribution of Preferences")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='Preferred_Mode', palette='viridis', ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("Engagement vs. Internet Issues")
        fig, ax = plt.subplots()
        sns.barplot(data=df, x='Preferred_Mode', y='Engagement_Level', hue='Internet_Issue', ax=ax)
        st.pyplot(fig)

    st.subheader("Raw Data Summary")
    st.write(df.describe())
else:
    st.info("No data yet. Be the first to submit a response in the sidebar!")

# Set visual style
sns.set_theme(style="whitegrid")

# Seed for reproducibility
np.random.seed(42)

# Create a dictionary of survey questions/responses
data = {
    'Student_ID': range(1, 101),
    'Age': np.random.randint(18, 25, 100),
    'Preferred_Mode': np.random.choice(['Online', 'Offline', 'Hybrid'], 100, p=[0.4, 0.45, 0.15]),
    'Avg_Daily_Study_Hours': np.random.uniform(2, 8, 100).round(1),
    'Engagement_Level': np.random.randint(1, 11, 100),  # Scale of 1 to 10
    'Internet_Issue': np.random.choice(['Yes', 'No'], 100, p=[0.3, 0.7]),
    'Understanding_Rating': np.random.randint(1, 11, 100) # How well they understand topics
}

# Create DataFrame
df = pd.DataFrame(data)

# Show first 5 rows
print(df.head())

# Check for missing values
print(df.isnull().sum())

# Basic statistical summary
print(df.describe())

# Group by Preferred Mode and see the average Engagement and Study Hours
analysis = df.groupby('Preferred_Mode')[['Engagement_Level', 'Avg_Daily_Study_Hours', 'Understanding_Rating']].mean()
print(analysis)

plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Preferred_Mode', palette='viridis')
plt.title('Distribution of Student Learning Preferences')
plt.xlabel('Learning Mode')
plt.ylabel('Number of Students')
plt.show()

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='Preferred_Mode', y='Understanding_Rating', palette='Set2')
plt.title('Understanding Rating Across Different Modes')
plt.show()

plt.figure(figsize=(7, 5))
sns.barplot(data=df, x='Preferred_Mode', y='Engagement_Level', hue='Internet_Issue')
plt.title('Impact of Internet Issues on Student Engagement')
plt.show()"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Learning Preference Survey",
    page_icon="🎓",
    layout="wide"
)

# Apply Seaborn theme for the plots
sns.set_theme(style="whitegrid")

# ==========================================
# 2. DATA PERSISTENCE LAYER
# ==========================================
# File path for the local database
DATA_FILE = "survey_results.csv"


def load_existing_data():
    """Loads data from CSV or creates a new DataFrame if file doesn't exist."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Define the schema for the data
        return pd.DataFrame(columns=[
            'Age', 'Preferred_Mode', 'Avg_Daily_Study_Hours',
            'Engagement_Level', 'Internet_Issue', 'Understanding_Rating'
        ])


def save_new_response(data_dict):
    """Appends a new user response to the CSV file."""
    df = load_existing_data()
    new_row = pd.DataFrame([data_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return df


# ==========================================
# 3. USER INTERFACE (SIDEBAR)
# ==========================================
st.sidebar.title("📝 Student Survey")
st.sidebar.markdown("Please provide your feedback on learning modes.")

with st.sidebar.form("survey_form", clear_on_submit=True):
    age = st.number_input("What is your age?", min_value=10, max_value=100, value=20)

    mode = st.selectbox(
        "Preferred Learning Mode",
        options=["Online", "Offline", "Hybrid"]
    )

    hours = st.slider("Average daily study hours", 0.0, 15.0, 4.0, step=0.5)

    engagement = st.select_slider(
        "Engagement Level (1 = Low, 10 = High)",
        options=list(range(1, 11)),
        value=5
    )

    internet = st.radio("Do you face frequent internet issues?", ["Yes", "No"])

    understanding = st.slider("Rate your understanding of topics (1-10)", 1, 10, 5)

    submit_button = st.form_submit_button("Submit Response")

# ==========================================
# 4. MAIN DASHBOARD LOGIC
# ==========================================
st.title("🎓 Online vs. Offline Learning Analysis")
st.markdown("""
This dashboard analyzes real-time student feedback to compare the effectiveness 
of different learning environments. Submit your data in the sidebar to update the charts!
""")

# Handle Submission
if submit_button:
    current_response = {
        'Age': age,
        'Preferred_Mode': mode,
        'Avg_Daily_Study_Hours': hours,
        'Engagement_Level': engagement,
        'Internet_Issue': internet,
        'Understanding_Rating': understanding
    }
    df = save_new_response(current_response)
    st.success("Thank you! Your response has been recorded.")
else:
    df = load_existing_data()

# ==========================================
# 5. DATA VISUALIZATION
# ==========================================
if not df.empty:
    # --- Metric Row ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Responses", len(df))
    col2.metric("Avg Engagement", f"{df['Engagement_Level'].mean():.1f}/10")
    col3.metric("Avg Study Hours", f"{df['Avg_Daily_Study_Hours'].mean():.1f} hrs")

    st.divider()

    # --- Charts Row 1 ---
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Distribution of Preferences")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df, x='Preferred_Mode', palette='viridis', ax=ax1)
        ax1.set_ylabel("Number of Students")
        st.pyplot(fig1)

    with chart_col2:
        st.subheader("Understanding Rating by Mode")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df, x='Preferred_Mode', y='Understanding_Rating', palette='Set2', ax=ax2)
        st.pyplot(fig2)

    # --- Charts Row 2 ---
    st.subheader("Impact of Internet Issues on Engagement")
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    sns.barplot(data=df, x='Preferred_Mode', y='Engagement_Level', hue='Internet_Issue', ax=ax3)
    st.pyplot(fig3)

    # --- Raw Data ---
    with st.expander("View Raw Data Table"):
        st.dataframe(df, use_container_width=True)

else:
    st.info("👋 Welcome! No data has been collected yet. Use the sidebar to submit the first response.")

# ==========================================
# 6. DOCUMENTATION & FOOTER
# ==========================================
st.sidebar.divider()
st.sidebar.info("""
**How to use:**
1. Fill out the form.
2. Click **Submit**.
3. Watch the dashboard update!

**Tech Stack:**
- Streamlit (Frontend)
- Pandas (Data Processing)
- Seaborn/Matplotlib (Analytics)
""")
