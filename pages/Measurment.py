

import dash
from dash_labs.plugins.pages import register_page
from dash import dcc, html, Input, Output, callback

from datetime import datetime as dt

from src.RandDataGen import rand_msurs
from src.Graphs import create_lines

register_page(__name__)
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)


server = app.server
app.config.suppress_callback_exceptions = True


msurs_df=rand_msurs(200)
msurs_list=['temperature','pulse', 'respration', 'sugar', 'oxegen','Pressure']
conditions=msurs_df.condition.unique()
#exclude null
conditions= [i for i in msurs_df.condition.unique() if i ]


def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Vitals Analytics"),
            html.H3("Welcome to the Vitals Analytics Dashboard"),
            html.Div(
                id="intro",
                children="Explore your vitals data by date range, conditon. Annotate your charts by weather showing your conditon upon recording your measurement or show gudieliness of each measurement, you can select both but charts would be litile unclear .",
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

        html.P("Add Annotation"),

        dcc.Checklist(
            
            options=['Show Conditon', 'Show guidelines'],
            value=[],
            inline=True,id="styling-select",
),html.Br(),
            html.P("Select Condition"),
            #html.Br(),
            dcc.Dropdown(
                id="cond-select",
                options=[{"label": i, "value": i} for i in conditions],
                value=conditions[:],
                multi=True,
            ),
            html.Br(),
            html.P("Select Date Range"),
            dcc.DatePickerRange(
                id="date-picker-select",
                start_date=dt(2018, 5, 6),
                end_date=dt(2018, 6, 2),
                min_date_allowed=dt(2018, 4, 24),
                max_date_allowed=dt(2018, 6, 27),
                initial_visible_month=dt(2018, 6, 27),
            ),
            html.Br(),
            html.Br(),
            html.P("Select Measurements To Show"),
            dcc.Dropdown(
                id="msurs-select",
                options=[{"label": i, "value": i} for i in msurs_list],
                value=msurs_list[:],
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
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],style={"display":"none"}
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
                        html.B("Your Measurments"),
                        html.Hr(),
                        dcc.Graph(id="patient_volume_h",style={"height":"1500px",'width': '1140px',}) ,

                    ],#style={'width':'1200', 'height':'800px'},
                ),
                # Patient Wait time by Department

            ],
        ),
    ],
)


@callback(
    Output("patient_volume_h", "figure"),
    [
        Input("msurs-select", "value"),
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("styling-select","value"),
        Input("cond-select", "value"),

        #Input("reset-btn", "n_clicks"),
    ],
)

def update_lines(vitals,start,end,style,cond):

    start = start + " 00:00:00"
    end = end + " 00:00:00"


    # Return to original hm(no colored annotation) by resetting
    return create_lines(
        msurs_df,vitals,start, end,style,cond)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
