


from datetime import datetime as dt

from src.RandDataGen import rand_cmmit,rand_tkn
from src.Graphs import create_pie,Create_HeatScatt

import dash
from dash import dcc, html, Input, Output, callback
from dash_labs.plugins.pages import register_page

register_page(__name__,path="/")
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)


server = app.server
app.config.suppress_callback_exceptions = True


cmmit_df=rand_cmmit(5,60)
currtkn_df=rand_tkn(5)


drug_list=cmmit_df["drug"].explode().dropna().unique().tolist()


def create_pies():
    """

    func to create drug progress chart.
    """
    n=len(currtkn_df)#number of bar charts
    w=1150/n #radius of each bar chart 
    graph_list=[]#a list to put every single pie in it 
    #iteritaing over rows to draw charts one per iteriation
    for idx,row in currtkn_df.iterrows():
        #append the chart to charts list
        graph_list.append(html.Div(
            dcc.Graph(figure=create_pie(n,row),    
            config={'displayModeBar': False
    },),
            # Ensure graphs are correct size, side-by-side with required margin
            style={'width':f'{w}px',"heigt":f"{w}px", 'display':"inline-block",'margin':'0px ' }),)
    return graph_list

def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Medication Analytics"),
            html.H3("Welcome to the Medication Analytics Dashboard"),
            html.Div(
                id="intro",
                children="Explore Your commitment to medication by date, choose which medication you want to show insights about, you also can see information about your current medication.",
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Date Range"),
            dcc.DatePickerRange(
                id="date-picker-select",
                start_date=dt(2018, 5, 6),
                end_date=dt(2018, 6, 2),
                min_date_allowed=dt(2018, 4, 24),
                max_date_allowed=dt(2018, 6, 2),
                initial_visible_month=dt(2018, 6, 1),
            ),
            html.Br(),
            html.Br(),
            html.P("Select Drugs To Show"),
            dcc.Dropdown(
                id="admit-select",
                options=[{"label": i, "value": i} for i in drug_list],
                value=drug_list[:],
                multi=True,
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )



layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("Logo.png"))],style={"display":"none"}
        ),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                html.Div(
                    id="patient_volume_card",
                    children=[
                    html.Hr(),
                    html.B("Currently Taken Drugs Progress"),
                    html.Br(),
                    html.Br(),
                    *create_pies(),

                        html.Br(),
                        html.Br(),
                        html.B("Last 28 Days Comitment"),
                        html.Hr(),
                        # Ensure graphs are correct size, side-by-side with required margin
                        dcc.Graph(id="patient_volume_hm",style={'width': '1150px', 'height': '800px'}) ,

                    ],
                ),

            ],
        ),
    ],
)


@callback(
    Output("patient_volume_hm", "figure"),
    [
        Input("admit-select", "value"),
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        #Input("reset-btn", "n_clicks"),
    ],
)

def update_heatmap(drugs,start,end):



    # Return to original hm(no colored annotation) by resetting
    return Create_HeatScatt(
        cmmit_df,drugs,start, end)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
