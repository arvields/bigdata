from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import io
import base64
from dash import dash_table
from dash.exceptions import PreventUpdate
from dbfread import DBF

# Initialize the Dash app
app = Dash(__name__)

# Load initial data
df = pd.read_csv('suicide-rate.csv')

# Create country list for dropdown
country_list = [{'label': c, 'value': c} for c in df['country'].unique()]

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Suicide Rate of Countries Based on Age and Sex (1986-2015)",
                style={'textAlign': 'center'})
    ]),

    # File upload section
    html.Div([
        html.Hr(),
        html.H3("Upload CSV File"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            multiple=False,
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        ),
        html.Div(id='output-data-upload'),
    ]),

    html.Div([
        html.Label([
            "Selected Year: ",
            dcc.Dropdown(
                id='csv-year',
                options=[{'label': year, 'value': year} for year in range(1986, 2016)],
                value=2000,
                searchable=False,
                clearable=False,
                style={'width': '50%'}
            ),
        ]),

        html.Label([
            "Selected Age: ",
            dcc.Dropdown(
                id='csv-age',
                options=[
                    {'label': '5-14 years', 'value': '5-14 years'},
                    {'label': '15-24 years', 'value': '15-24 years'},
                    {'label': '25-34 years', 'value': '25-34 years'},
                    {'label': '35-54 years', 'value': '35-54 years'},
                    {'label': '55-74 years', 'value': '55-74 years'},
                    {'label': '75+ years', 'value': '75+ years'},
                ],
                value='5-14 years',
                searchable=False,
                clearable=False,
                style={'width': '50%'}
            ),
        ]),

        html.Label([
            "Selected Sex: ",
            dcc.Dropdown(
                id='csv-sex',
                options=[
                    {'label': 'Male', 'value': 'male'},
                    {'label': 'Female', 'value': 'female'}
                ],
                value='male',
                searchable=False,
                clearable=False,
                style={'width': '50%'}
            ),
        ]),

    ]),

    html.Div([
        dcc.Graph(id='csv-map'),
    ]),

    html.Div([
        html.Label([
            "Selected Country: ",
            dcc.Dropdown(
                id='csv-country',
                options=country_list,
                value=['Philippines', 'South Africa', 'Brazil', 'United States', 'France', 'Australia'],
                multi=True,
                clearable=False,
                style={'width': '50%'}
            ),
        ]),

    ]),

    html.Div([
        dcc.Graph(id='csv-graph-suicides')
    ]),

    html.Div([
        dcc.Graph(id='csv-graph-population')
    ]),

    html.Div([
        dcc.Graph(id='csv-graph-gdp-year')
    ]),

    html.Div([
        dcc.Graph(id='csv-graph-gdp-capita')
    ]),
])

# Callback to update the displayed data after file upload
@app.callback(
    [Output('output-data-upload', 'children'),
     Output('csv-map', 'figure'),
     Output('csv-graph-suicides', 'figure'),
     Output('csv-graph-population', 'figure'),
     Output('csv-graph-gdp-year', 'figure'),
     Output('csv-graph-gdp-capita', 'figure')],
    [Input('upload-data', 'contents'),
     Input('csv-year', 'value'),
     Input('csv-age', 'value'),
     Input('csv-sex', 'value'),
     Input('csv-country', 'value')]
)
def update_data(contents, selected_year, selected_age, selected_sex, selected_country):
    if contents is None:
        raise PreventUpdate

    # Initialize the variable
    uploaded_df = pd.DataFrame()

    # Parse the content of the uploaded file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Check if the file is a CSV or DBF
        if 'csv' in content_type:
            uploaded_df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'dbf' in content_type:
            # Read DBF file using dbfread
            table = DBF(io.BytesIO(decoded))
            uploaded_df = pd.DataFrame(iter(table))

    except Exception as e:
        return html.Div(['Error reading uploaded file. Please make sure it is a valid CSV or DBF file.']), {}, {}, {}, {}, {}

    # Update the data and visualizations
    country_list = [{'label': c, 'value': c} for c in uploaded_df['country'].unique()]

    # Visualizations
    map_fig = update_map(selected_year, selected_age, selected_sex, uploaded_df)
    suicides_fig = update_graph_suicide(selected_country, selected_age, selected_sex, uploaded_df)
    population_fig = update_graph_population(selected_country, selected_age, selected_sex, uploaded_df)
    gdp_year_fig = update_graph_gdp_year(selected_country, selected_age, selected_sex, uploaded_df)
    gdp_capita_fig = update_graph_gdp_capita(selected_country, selected_age, selected_sex, uploaded_df)

    return html.Div(['File uploaded successfully!']), map_fig, suicides_fig, population_fig, gdp_year_fig, gdp_capita_fig

# Callback functions for visualizations
def update_map(selected_year, selected_age, selected_sex, df):
    selected_df = df[(df.year == selected_year) &
                     (df.age == selected_age) &
                     (df.sex == selected_sex)]

    # Check if 'country_iso' column exists in selected_df
    if 'country_iso' not in selected_df.columns:
        # If not, you need to create it based on the country names or ISO codes
        # For example, assuming 'iso_mapping' is a mapping of country names to ISO codes
        iso_mapping = {'Philippines': 'PHL', 'South Africa': 'ZAF', 'Brazil': 'BRA', 'United States': 'USA', 'France': 'FRA', 'Australia': 'AUS'}
        selected_df['country_iso'] = selected_df['country'].map(iso_mapping)

    fig = px.choropleth(selected_df,
                        locationmode='ISO-3',
                        locations='country_iso',
                        color='suicides/100k pop',
                        hover_name='country',
                        hover_data=['country_iso', 'suicides/100k pop'],
                        labels={'country_iso': 'Country Code (ISO-3)',
                                'suicides/100k pop': 'Suicide Rate (per 100k people)'},
                        color_continuous_scale=px.colors.sequential.Plasma,
                        range_color=(0, 225),
                        width=1500,
                        height=550)
    return fig

def update_graph_suicide(selected_country, selected_age, selected_sex, df):
    selected_df = df[(df['country'].isin(selected_country)) &
                     (df.age == selected_age) &
                     (df.sex == selected_sex)]

    fig = px.line(selected_df,
                  x='year',
                  y='suicides_no',
                  color='country',
                  labels={
                      'year': 'Year',
                      'suicides_no': 'No. of Suicides',
                      'country': 'Selected Country'
                  },
                  title='No. of Suicides in a Country Based on Age and Sex',
                  markers=True)
    return fig

def update_graph_population(selected_country, selected_age, selected_sex, df):
    selected_df = df[(df['country'].isin(selected_country)) &
                     (df.age == selected_age) &
                     (df.sex == selected_sex)]

    fig = px.line(selected_df,
                  x='year',
                  y='population',
                  color='country',
                  labels={
                      'year': 'Year',
                      'population': 'Population',
                      'country': 'Selected Country'
                  },
                  title='Population of a Country Based on Age and Sex',
                  markers=True)
    return fig

def update_graph_gdp_year(selected_country, selected_age, selected_sex, df):
    selected_df = df.loc[(df['country'].isin(selected_country)) &
                         (df.age == selected_age) &
                         (df.sex == selected_sex)]

    # Check if 'gdp_for_year($)' column exists in selected_df
    if 'gdp_for_year($)' not in selected_df.columns:
        # If not, adjust the column name based on your actual column names
        raise ValueError("Column 'gdp_for_year($)' not found in the DataFrame.")

    fig = px.line(selected_df,
                  x='year',
                  y='gdp_for_year($)',
                  color='country',
                  labels={
                      'year': 'Year',
                      'gdp_for_year($)': 'GDP per Year ($)',
                      'country': 'Selected Country'
                  },
                  title='Yearly Gross Domestic Product (GDP) of a Country Based on Age and Sex',
                  markers=True)
    return fig

def update_graph_gdp_capita(selected_country, selected_age, selected_sex, df):
    selected_df = df.loc[(df['country'].isin(selected_country)) &
                         (df.age == selected_age) &
                         (df.sex == selected_sex)]

    # Print the column names for debugging purposes
    print(f"Column names in selected_df: {selected_df.columns}")

    # Check if 'gdp_per_capita($)' column exists in selected_df
    if 'gdp_per_capita($)' not in selected_df.columns:
        # Print the actual column names in the DataFrame
        print(f"Actual column names in the DataFrame: {df.columns}")
        raise ValueError("Column 'gdp_per_capita($)' not found in the DataFrame.")

    fig = px.line(selected_df,
                  x='year',
                  y='gdp_per_capita($)',
                  color='country',
                  labels={
                      'year': 'Year',
                      'gdp_per_capita($)': 'GDP per Capita ($)',
                      'country': 'Selected Country'
                  },
                  title='Yearly Gross Domestic Product (GDP) per Capita of a Country Based on Age and Sex',
                  markers=True)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
