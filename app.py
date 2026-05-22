import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
df = pd.read_csv(URL)
df.columns = df.columns.str.lower()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", 
            style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    
    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'},
                {'label': 'Yearly Report', 'value': 'Yearly Report'}
            ],
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlign': 'center'}
        )
    ]),
    
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': int(i), 'value': int(i)} for i in sorted(df['year'].unique())],
            placeholder='Select Year',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlign': 'center'}
        )
    ]),
    
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flexWrap': 'wrap'}),
    ])
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Report':
        return False
    else:
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(report_type, input_year):
    if report_type == 'Recession Period Statistics':
        recession_data = df[df['recession'] == 1]
        
        yearly_rec = recession_data.groupby('year')['automobile_sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='year', y='automobile_sales', title="Average Automobile Sales over Recession Period"))
        
        average_sales = recession_data.groupby('vehicle_type')['automobile_sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='vehicle_type', y='automobile_sales', title="Average Sales by Vehicle Type"))
        
        exp_rec = recession_data.groupby('vehicle_type')['advertising_expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values='advertising_expenditure', names='vehicle_type', title="Ad Expenditure by Vehicle Type"))
        
        R_chart4 = dcc.Graph(figure=px.scatter(recession_data, x='unemployment_rate', y='automobile_sales', color='vehicle_type', title="Effect of Unemployment Rate on Sales"))
        
        return [
            html.Div(children=[R_chart1, R_chart2], style={'display': 'flex', 'width': '100%'}),
            html.Div(children=[R_chart3, R_chart4], style={'display': 'flex', 'width': '100%'})
        ]

    elif report_type == 'Yearly Report' and input_year:
        yearly_data = df[df['year'] == input_year]
        
        monthly_sales = yearly_data.groupby('month')['automobile_sales'].sum().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(monthly_sales, x='month', y='automobile_sales', title=f"Total Monthly Sales in {input_year}"))
        
        Y_chart2 = dcc.Graph(figure=px.bar(yearly_data, x='vehicle_type', y='automobile_sales', title=f"Average Sales by Vehicle Type in {input_year}"))
        
        exp_yearly = yearly_data.groupby('vehicle_type')['advertising_expenditure'].sum().reset_index()
        Y_chart3 = dcc.Graph(figure=px.pie(exp_yearly, values='advertising_expenditure', names='vehicle_type', title=f"Ad Expenditure in {input_year}"))
        
        return [
            html.Div(children=[Y_chart1, Y_chart2], style={'display': 'flex', 'width': '100%'}),
            html.Div(children=[Y_chart3], style={'display': 'flex', 'width': '100%'})
        ]
    else:
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
    