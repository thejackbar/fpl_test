import pandas as pd
import streamlit as st
import io

# Creating a dataframe template for your fantasy football team
columns = ['Player Name', 'Position', 'Price (M)']
positions = ['GK', 'DEF', 'MID', 'ATT']

# Initializing the template
fantasy_team = pd.DataFrame(columns=columns)

# Adding empty rows for each player position
fantasy_team = pd.concat([fantasy_team, pd.DataFrame([{'Player Name': '', 'Position': 'GK', 'Price (M)': 0} for _ in range(2)])], ignore_index=True)
fantasy_team = pd.concat([fantasy_team, pd.DataFrame([{'Player Name': '', 'Position': 'DEF', 'Price (M)': 0} for _ in range(5)])], ignore_index=True)
fantasy_team = pd.concat([fantasy_team, pd.DataFrame([{'Player Name': '', 'Position': 'MID', 'Price (M)': 0} for _ in range(5)])], ignore_index=True)
fantasy_team = pd.concat([fantasy_team, pd.DataFrame([{'Player Name': '', 'Position': 'ATT', 'Price (M)': 0} for _ in range(3)])], ignore_index=True)

# Streamlit web app setup
st.title("Fantasy Football Team Tracker")

# Editable data table using form and columns for compatibility
with st.form("team_form"):
    edited_team = fantasy_team.copy()
    for idx, row in edited_team.iterrows():
        cols = st.columns(3)
        edited_team.at[idx, 'Player Name'] = cols[0].text_input(f"Player Name {idx+1}", row['Player Name'])
        edited_team.at[idx, 'Position'] = cols[1].selectbox(f"Position {idx+1}", options=positions, index=positions.index(row['Position']) if row['Position'] in positions else 0)
        edited_team.at[idx, 'Price (M)'] = cols[2].number_input(f"Price (M) {idx+1}", min_value=0.0, max_value=20.0, value=row['Price (M)'])
    submitted = st.form_submit_button("Update Team")

# Function to calculate the total price of the team
def calculate_total_price(team_df):
    return team_df['Price (M)'].sum()

# Placeholder for checking budget
budget = 100  # The total budget available

# Calculating total price and displaying results
if submitted:
    total_price = calculate_total_price(edited_team)
    if total_price > budget:
        st.warning(f"Warning: Your total team price of {total_price}M exceeds the budget of {budget}M.")
    else:
        st.success(f"Your total team price is {total_price}M, within the budget of {budget}M.")

# Export to Excel
excel_buffer = io.BytesIO()
edited_team.to_excel(excel_buffer, index=False, engine='openpyxl')
excel_buffer.seek(0)

st.download_button(
    label="Download Team as Excel",
    data=excel_buffer,
    file_name="fantasy_team_tracker.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
