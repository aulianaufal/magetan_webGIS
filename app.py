from flask import Flask
from flask import render_template, request
import folium
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("static/data_populasi.csv")
names = df['nama lokasi'].dropna().unique().tolist()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    nm = ""
    description = ""
    name = ""

    if request.method == 'POST':
        nm = request.form.get('nm')
        description = request.form.get('description')
        name = request.form.get('name')

    filtered = df[
        (df["nama lokasi"].str.contains(nm, case=False, na=False)) &
        (df["deskripsi"].str.contains(description, case=False, na=False)) &
        (df["nama lokasi"].str.contains(name, case=False, na=False))
    ]

    m = folium.Map(location=[-7.6920988, 111.3213975], zoom_start=13)
    for _, row in filtered.iterrows():
        popup_html = f"""
        <div style="max-width: 250px; font-family: Arial;">
            <h4 style="color: #2c3e50; margin-bottom: 1px;">{row['nama lokasi']}</h4>
            <p style="color: #7f8c8d; margin-top: 1px; line-height: 1.4;">
                {row['deskripsi']}
            </p>
        </div>
        """
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row["nama lokasi"]
        ).add_to(m)

    # Save map to HTML string
    map_html = m._repr_html_()
    return render_template('home.html', map_html=map_html, names=names)

if __name__ == '__main__':
    app.run(debug=True)
