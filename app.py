import tkinter as tk
from tkinter import filedialog, simpledialog
import folium
import os
import geopandas as gpd
from shapely.geometry import Point

class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Analysis")
        
        # Campo para inserir o número da matrícula
        self.matricula_entry = tk.Entry(root)
        self.matricula_entry.pack()

        # Botão para carregar arquivo GeoJSON/TopoJSON
        load_button = tk.Button(root, text="Carregar Arquivo", command=self.load_file)
        load_button.pack()

        # Inicializar o Mapa Folium
        self.initialize_map()

    def initialize_map(self):
        self.map = folium.Map(location=[-15.788497, -47.879873], zoom_start=4)
        self.map_html = 'map.html'
        if os.path.exists(self.map_html):
            self.map = folium.Map(location=[-15.788497, -47.879873], zoom_start=4)
            folium.map.LayerControl().add_to(self.map)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("GeoJSON/TopoJSON/JSON files", "*.geojson *.topojson *.json")])
        if file_path:
            self.display_map(file_path)

    def display_map(self, file_path):
        gdf = gpd.read_file(file_path)
        for _, row in gdf.iterrows():
            folium.GeoJson(row['geometry']).add_to(self.map)
            # Se um número de matrícula foi inserido, exibir no meio do polígono
            if self.matricula_entry.get():
                center = row['geometry'].centroid
                folium.Marker([center.y, center.x], popup=self.matricula_entry.get()).add_to(self.map)

        self.map.save(self.map_html)
        os.system(f'start {self.map_html}')

if __name__ == "__main__":
    root = tk.Tk()
    app = MapApp(root)
    root.mainloop()
