import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import geopandas as gpd
from datetime import datetime
import requests
import io
import os
import json
import base64
import logging
from pathlib import Path
import zipfile
import traceback
from urllib.error import URLError, HTTPError
from flask import send_file

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("medicare_dashboard.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("medicare_dashboard")

# Data Collection Functions
def download_ma_enrollment_data(year, month, retry_count=3):
    # ... (same as before)

def download_ma_penetration_data(year, month, retry_count=3):
    # ... (same as before)

def download_ratebook_data(year, retry_count=3):
    # ... (same as before)

def download_county_geo_data():
    # ... (same as before)

# Data Processing Functions
def process_enrollment_data(enrollment_dfs):
    # ... (same as before)

def process_penetration_data(penetration_dfs):
    # ... (same as before)

def enrich_with_ratebook(enrollment_data, ratebook_data):
    # ... (same as before)

# Visualization Functions
def create_enrollment_trend_chart(enrollment_data):
    # ... (same as before)

def create_penetration_rate_map(penetration_data, county_geo, year, month):
    # ... (same as before)

def create_payment_by_county_chart(enriched_data, state=None):
    # ... (same as before)

# Dash App
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Medicare Advantage Dashboard"),
    
    # Year and month selection
    html.Div([
        html.Label("Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in range(2020, 2024)],
            value=2023
        ),
        
        html.Label("Month:"),
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': str(month), 'value': month} for month in range(1, 13)],
            value=1
        ),
        
        html.Label("State (for Payment Chart):"),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': 'All', 'value': 'All'}],  # Initialize with 'All'
            value='All'
        )
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    # Enrollment Trend Chart
    dcc.Graph(id='enrollment-trend-chart'),
    
    # Penetration Rate Map
    dcc.Graph(id='penetration-rate-map'),
    
    # Payment by County Chart
    dcc.Graph(id='payment-by-county-chart')
])

# Callbacks
@app.callback(
    Output('enrollment-trend-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_enrollment_trend_chart(year, month):
    enrollment_df = download_ma_enrollment_data(year, month)
    enrollment_data = process_enrollment_data([enrollment_df])
    return create_enrollment_trend_chart(enrollment_data)

@app.callback(
    Output('penetration-rate-map', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_penetration_rate_map(year, month):
    penetration_df = download_ma_penetration_data(year, month)
    penetration_data = process_penetration_data([penetration_df])
    county_geo = download_county_geo_data()
    return create_penetration_rate_map(penetration_data, county_geo, year, month)

@app.callback(
    Output('payment-by-county-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('state-dropdown', 'value')]
)
def update_payment_by_county_chart(year, month, state):
    enrollment_df = download_ma_enrollment_data(year, month)
    ratebook_df = download_ratebook_data(year)
    enrollment_data = process_enrollment_data([enrollment_df])
    enriched_data = enrich_with_ratebook(enrollment_data, ratebook_df)
    
    if state == 'All':
        return create_payment_by_county_chart(enriched_data)
    else:
        return create_payment_by_county_chart(enriched_data, state)

@app.callback(
    Output('state-dropdown', 'options'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_state_dropdown(year, month):
    enrollment_df = download_ma_enrollment_data(year, month)
    enrollment_data = process_enrollment_data([enrollment_df])
    states = enrollment_data['state']['State'].unique()
    state_options = [{'label': 'All', 'value': 'All'}] + [{'label': state, 'value': state} for state in states]
    return state_options

if __name__ == '__main__':
    app.run_server(debug=True)