import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import folium
from folium.plugins import HeatMap
import io


class Explorer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        # self.data = pd.read_html('https://en.wikipedia.org/wiki/Economy_of_the_United_States', match='Inflation rate')[0]

        buffer = io.StringIO()
        self.data.info(buf=buffer)
        self.info = buffer.getvalue()

    def type_distribution(self):
        grouped = self.data.groupby('Primary Type').size()
        less_than_one_columns = grouped[grouped / grouped.sum() < 0.01].index.tolist()
        self.data['Primary Type'] = self.data['Primary Type'].replace(less_than_one_columns, 'Other')

        grouped = self.data.groupby('Primary Type').size()
        fig = plt.figure()
        plt.pie(grouped, labels=grouped.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  
        plt.title('Distribution of Crimes by Primary Type')
        return fig
    
    def show_month_cnt(self):
        self.data['Date'] = pd.to_datetime(self.data['Date'], format='%m/%d/%Y %I:%M:%S %p')
        self.data['Month'] = self.data['Date'].dt.month
        grouped = self.data.groupby('Month').size()

        fig = plt.figure()
        plt.plot(grouped.index, grouped.values, marker='o', linestyle='-')
        plt.xlabel('Month')
        plt.ylabel('Count')
        plt.title('Crime Count by Month in 2022')
        plt.grid(True)
        return fig

    def map_chi(self):
        chicago_map = folium.Map(location=[41.8781, -87.6298], zoom_start=10)
        filtered_data = self.data[self.data['Latitude'].notnull()]
        locations = filtered_data[['Latitude', 'Longitude']].sample(2000)
        location_list = locations.values.tolist()

        heat_map = HeatMap(location_list, radius=15, blur=25)
        chicago_map.add_child(heat_map)

        return chicago_map

    