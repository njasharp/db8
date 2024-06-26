import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Gaming Trends Dashboard", layout="wide")
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    body {background-color: #212121;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Load the data from CSV
data = pd.read_csv('new_data.csv')
new_data = pd.read_csv('new_data2.csv')

# Remove columns with "Unnamed" in their names and drop rows with all None values
new_data = new_data.loc[:, ~new_data.columns.str.contains('^Unnamed')]
new_data = new_data.dropna(how='all')

# Function to display top 5 items as a list
def display_top_5(data_list, title):
    st.subheader(title)
    for item in data_list:
        st.write(f"{item}")

# Function to plot top 5 items as a bar chart
def plot_top_5(data_list, title):
    items = data_list[0].split(', ') if data_list else []
    labels = []
    sizes = []
    for item in items:
        parts = item.split(': ')
        if len(parts) == 2:
            labels.append(parts[0])
            sizes.append(int(parts[1].replace('%', '')))
    
    if labels and sizes:
        fig, ax = plt.subplots()
        ax.barh(labels, sizes, color='skyblue')
        ax.set_title(title)
        ax.invert_yaxis()
        st.pyplot(fig)

# Sidebar options
st.sidebar.title("Gaming Trends - Options")
selected_country = st.sidebar.selectbox("Select Country", data['Country'].unique())
selected_chart = st.sidebar.radio("Select Chart Type", ["Top Platforms","Mobile vs PC vs Console"])

# Filter data by selected country
country_data = data[data['Country'] == selected_country]
new_country_data = new_data[new_data['Country'] == selected_country]

# Main page
st.title(f"Gaming Trends in {selected_country}")

# Display main charts based on selection
if selected_chart == "Mobile vs PC vs Console":
    st.subheader("Mobile vs PC vs Console")
    mobile_pc_console = country_data['Mobile vs PC vs Console'].values[0]
    labels = ['Mobile', 'PC', 'Console']
    sizes = [int(s.split(': ')[1].replace('%', '')) for s in mobile_pc_console.split(', ')]
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

elif selected_chart == "Top Platforms":
    st.subheader("Top Platforms (Android vs iOS)")
    platforms = country_data['Top Platforms (Android vs iOS)'].values[0]
    labels = ['Android', 'iOS']
    sizes = [int(s.split(': ')[1].replace('%', '')) for s in platforms.split(', ')]
    
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig2)

# Display top 5 charts
engagement_data = new_country_data['Top Games (Engagement)'].tolist()
monetization_data = new_country_data['Top Games (Monetization)'].tolist()
genres_data = new_country_data['Top Genres'].tolist()
publishers_data = new_country_data['Top Publishers'].tolist()
trends_data = new_country_data['Emerging Trends'].tolist()

col1, col2 = st.columns(2)

with col1:
    display_top_5(engagement_data, f"Top Games (Engagement) - {selected_country}")
    plot_top_5(engagement_data, f"Top Games (Engagement) - {selected_country}")
    
    display_top_5(genres_data, f"Top Genres - {selected_country}")
    plot_top_5(genres_data, f"Top Genres - {selected_country}")

    display_top_5(trends_data, f"Emerging Trends - {selected_country}")
    plot_top_5(trends_data, f"Emerging Trends - {selected_country}")

with col2:
    display_top_5(monetization_data, f"Top Games (Monetization) - {selected_country}")
    plot_top_5(monetization_data, f"Top Games (Monetization) - {selected_country}")

    display_top_5(publishers_data, f"Top Publishers - {selected_country}")
    plot_top_5(publishers_data, f"Top Publishers - {selected_country}")

# Display footer
st.write(data)
st.write(new_data)
st.image("nod1.png")
st.info("dw-v1.2")