# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding="ISO-8859-1",
    dtype={
        'Div1Airport': str,
        'Div1TailNum': str,
        'Div2Airport': str,
        'Div2TailNum': str
    }
)

# Create Dash app
app = dash.Dash(__name__)

# Reusable styles
card_style = {
    'backgroundColor': 'white',
    'padding': '15px',
    'margin': '10px',
    'borderRadius': '15px',
    'boxShadow': '0 4px 12px rgba(0,0,0,0.08)',
    'width': '50%'
}

row_style = {
    'display': 'flex',
    'justifyContent': 'center',
    'gap': '20px',
    'marginBottom': '20px'
}

# App layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    'Flight Delay Time Statistics',
                    style={
                        'textAlign': 'center',
                        'color': '#2C3E50',
                        'fontSize': '36px',
                        'marginBottom': '10px'
                    }
                ),

                html.P(
                    'Explore average airline delay causes by year and airline.',
                    style={
                        'textAlign': 'center',
                        'color': '#7F8C8D',
                        'fontSize': '18px',
                        'marginBottom': '30px'
                    }
                ),

                html.Div(
                    children=[
                        html.Label(
                            "Input Year:",
                            style={
                                'fontSize': '18px',
                                'fontWeight': 'bold',
                                'marginRight': '10px'
                            }
                        ),
                        dcc.Input(
                            id='input-year',
                            value='2010',
                            type='number',
                            style={
                                'height': '35px',
                                'fontSize': '18px',
                                'borderRadius': '8px',
                                'border': '1px solid #BDC3C7',
                                'padding': '5px 10px'
                            }
                        )
                    ],
                    style={
                        'textAlign': 'center',
                        'marginBottom': '30px'
                    }
                ),

                html.Div([
                    html.Div(dcc.Graph(id='carrier-plot'), style=card_style),
                    html.Div(dcc.Graph(id='weather-plot'), style=card_style)
                ], style=row_style),

                html.Div([
                    html.Div(dcc.Graph(id='nas-plot'), style=card_style),
                    html.Div(dcc.Graph(id='security-plot'), style=card_style)
                ], style=row_style),

                html.Div(
                    dcc.Graph(id='late-plot'),
                    style={
                        **card_style,
                        'width': '95%',
                        'margin': '20px auto'
                    }
                )
            ],
            style={
                'maxWidth': '1300px',
                'margin': '0 auto',
                'padding': '30px'
            }
        )
    ],
    style={
        'backgroundColor': '#F4F6F7',
        'minHeight': '100vh',
        'fontFamily': 'Arial, sans-serif'
    }
)


# Compute data for selected year
def compute_info(airline_data, entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]

    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


# Callback
@app.callback(
    [
        Output('carrier-plot', 'figure'),
        Output('weather-plot', 'figure'),
        Output('nas-plot', 'figure'),
        Output('security-plot', 'figure'),
        Output('late-plot', 'figure')
    ],
    Input('input-year', 'value')
)
def get_graph(entered_year):
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(
        airline_data,
        entered_year
    )

    carrier_fig = px.line(
        avg_car,
        x='Month',
        y='CarrierDelay',
        color='Reporting_Airline',
        title='Average Carrier Delay Time by Airline'
    )

    weather_fig = px.line(
        avg_weather,
        x='Month',
        y='WeatherDelay',
        color='Reporting_Airline',
        title='Average Weather Delay Time by Airline'
    )

    nas_fig = px.line(
        avg_NAS,
        x='Month',
        y='NASDelay',
        color='Reporting_Airline',
        title='Average NAS Delay Time by Airline'
    )

    sec_fig = px.line(
        avg_sec,
        x='Month',
        y='SecurityDelay',
        color='Reporting_Airline',
        title='Average Security Delay Time by Airline'
    )

    late_fig = px.line(
        avg_late,
        x='Month',
        y='LateAircraftDelay',
        color='Reporting_Airline',
        title='Average Late Aircraft Delay Time by Airline'
    )

    figures = [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]

    for fig in figures:
        fig.update_layout(
            template='plotly_white',
            title_x=0.5,
            font=dict(size=12),
            margin=dict(l=40, r=40, t=60, b=40),
            legend_title_text='Airline'
        )

    return figures


# Run app
if __name__ == '__main__':
    app.run()
