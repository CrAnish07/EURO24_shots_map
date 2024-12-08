import json
import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


st.title("Euros 2024 shots map")
st.subheader("Filter to any team/player to see all of their shots taken!")

df = pd.read_csv('euros_2024_shot_map.csv')
df = df[df['type']=='Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

team = st.selectbox('Select a team', df['team'].sort_values().unique(), index=None)
player = st.selectbox('Select a player', df[df['team']==team]['player'].sort_values().unique(), index=True)

def filter_data(df, team, player):
    if team:
        df = df[df['team']==team]
    if player:
        df = df[df['player']==player]
        
    return df

filtered_df = filter_data(df, team, player)        

pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10,10))
fig.set_facecolor('#f3edd3')
ax.patch.set_facecolor('#f3edd3')

fig.text(
    0.34, 0.915, "Goal        No Goal", size=20, color="black"
    )


fig.patches.extend([
    Circle(
         (0.31, 0.925), 0.015, color="green",
         transform=fig.transFigure, alpha = 1, zorder = 2
),
    Circle(
         (0.445, 0.925), 0.015, fill=True, color="white",
         transform=fig.transFigure, alpha = 0.5, zorder = 1 
 )
])

# green_circle = Circle(
#         (0.31, 0.925), 0.015, color="green",
#         transform=fig.transFigure, edgecolor = 'black', alpha = 1, zorder = 2
# ),
# white_circle = Circle(
#         (0.445, 0.925), 0.015, fill=True, color="white",
#         transform=fig.transFigure, edgecolor = 'black', alpha = 0.5, zorder = 1 
# )

# fig.add_artist(green_circle)
# fig.add_artist(white_circle)


def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x = float(x['location'][0]),
            y = float(x['location'][1]),
            ax = ax,
            s = 1000 * x['shot_statsbomb_xg'],
            color = 'green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors = 'black',
            alpha = 1 if x['type'] == 'goal' else 0.5,
            zorder = 2 if x['type'] == 'goal' else 1
        )
        
plot_shots(filtered_df, ax, pitch)        

st.pyplot(fig)