#import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import pandas as pd
import matplotlib as mpl

import matplotlib.gridspec as gridspec
from PIL import Image
import requests
from io import BytesIO
import streamlit as st

classification_df = pd.read_csv('formula1.csv')

# remove the first column in classification_df
classification_df.drop(classification_df.columns[0], axis=1, inplace=True)

# create a new column with the lap time difference to first row
classification_df['diff_to_fastest'] = classification_df['Lap Time'] - classification_df['Lap Time'].min()

#round off the new column to 3 decimal points
classification_df['diff_to_fastest'] = classification_df['diff_to_fastest'].round(3)

title_font = "Alegreya Sans"
body_font = "Open Sans"
text_color = "white"
background = "#010001"
filler = "grey"
primary = "lime"

mpl.rcParams["xtick.color"] = text_color
mpl.rcParams["ytick.color"] = text_color
mpl.rcParams["xtick.labelsize"] = 20
mpl.rcParams["ytick.labelsize"] = 24

fig, ax = plt.subplots(figsize=(32, 18))
fig.set_facecolor(background)
ax.patch.set_alpha(0)

ax.grid(color=filler, linestyle="-", linewidth=1, alpha=0.5, zorder=0)

x = classification_df["Lap Time"].tolist()
y = classification_df["Driver"].tolist()

hbars = ax.barh(
    y,
    x,
    color="lime",
    edgecolor=background,
    lw=0.5,
    zorder=1,
    xerr=1,
    error_kw=dict(
        lw=2,
        capsize=2,
        capthick=0,
        ecolor="red",
    ),
)
ax.invert_yaxis()

fig.text(
    0.15,
    0.90,
    "Bahrain Testing Day 3 Classification",
    fontweight="bold",
    fontsize=40,
    fontfamily=title_font,
    color=text_color,
)

# ax.bar_label(hbars, classification_df['Lap Time'], color='black', fontsize=24, fontweight='bold',  fmt='%.2f',  label_type='center')
ax.bar_label(
    hbars,
    classification_df["diff_to_fastest"],
    color="red",
    fontsize=24,
    fontweight="regular",
    fmt="%.2f",
    padding=12,
)

ax.set_xlabel("Lap Time", fontsize=32, color=text_color)

ax.tick_params(axis="y", length=20)

spines = ["top", "bottom", "left", "right"]
for s in spines:
    if s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    else:
        ax.spines[s].set_color(text_color)

ax2 = fig.add_axes([0.12, 0.90, 0.025, 0.025])  # badge
ax2.axis("off")
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Flag_of_Bahrain.svg/1280px-Flag_of_Bahrain.svg.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
ax2.imshow(img)

fig.text(
    0.05,
    0.05,
    "Created for r/Formula1 with ❤️ by @harish5p",
    fontsize=20,
    color="red",
    fontfamily=body_font,
)

plt.tight_layout
st.pyplot(fig)
