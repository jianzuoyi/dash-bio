import dash_bio
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_table as dt
from dash_bio.utils import circosParser as cp
import base64
import io
import pandas as pd
import json

with open('./tests/dash/sample_data/circos_graph_data.json', 'r') as circos_graph_data:
    circos_graph_data = json.load(circos_graph_data)

parsed_layout = cp.txt_to_layout(
    file_one_name="./tests/dash/sample_data/circos_GRCh37.txt",
    file_two_name="./tests/dash/sample_data/circos_GRCh38.txt",
    append_one="-GRCh37",
    append_two="-GRCh38",
    relPath=True,
    create_local=False,
)

parsed_track_one = cp.txt_to_track(
    file_name="./tests/dash/sample_data/circos_GRCh37.txt",
    append_block_id="-GRCh37",
    relPath=True,
    create_local=False,
)

parsed_track_two = cp.txt_to_track(
    file_name="./tests/dash/sample_data/circos_GRCh38.txt",
    append_block_id="-GRCh38",
    relPath=True,
    create_local=False,
)


def description():
    return 'Dash Circos is a library used to analyze and interpret data using a circular layout, \
    based on the popular Circos graph. Showcase relationships between data/datasets in a \
    beautiful way.'


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string).decode("UTF-8")
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded))
            df = df.to_dict(orient="records")
            return df
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])
    return


empty = dash_bio.DashCircos(
    id="main-circos", selectEvent={}, layout=[], size=800, config={}, tracks=[]
)

upload_instructions = (
    "1. Set Circos Graph to Custom. \n" +
    "2. Select Dataset (Press Data for Sample Data). \n" +
    "3. Drag and Drop .CSV for each Dataset \n" +
    "4. Press Render! \n" +
    "5. Reselect Dataset to view data in table." 
)


def layout():
    return html.Div(
        [
            html.Div(
                id="header-circos",
                style={"background-color": "#119DFF"},
                children=[
                    html.H2("Dash Bio: Circos Graph Selector"),
                    html.A(
                        html.Img(
                            src='data:image/png;base64,{}'.format(
                                base64.b64encode(
                                    open(
                                        './assets/dashbio_logo_words.png',
                                        'rb'
                                    ).read()
                                ).decode()
                            )
                        ),
                        href="http://www.dash.bio",
                    ),
                ],
                className="circos-banner",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    dt.DataTable(
                                        id="data-table",
                                        row_selectable=True,
                                        sorting=True,
                                        filtering=True,
                                        css=[{
                                            'selector': '.dash-cell div.dash-cell-value',
                                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;',
                                        }],
                                        style_cell={
                                            'whiteSpace': 'no-wrap',
                                            'overflow': 'hidden',
                                            'textOverflow': 'ellipsis',
                                                            'maxWidth': 0,
                                        },
                                        style_table={
                                            'maxHeight': '30vh',
                                        },
                                        n_fixed_rows=1,
                                    ),
                                    html.Div(
                                        id="expected-index"),
                                ], className="circos-datatable"
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H5(
                                                "Select Circos Graph"),
                                            dcc.Dropdown(
                                                id="circos-selector",
                                                options=[
                                                    {
                                                        "label": "Custom",
                                                        "value": "custom",
                                                    },
                                                    {
                                                        "label": "Heatmap",
                                                        "value": "heatmap",
                                                    },
                                                    {
                                                        "label": "Chords",
                                                        "value": "chords",
                                                    },
                                                    {
                                                        "label": "Highlight",
                                                        "value": "highlight",
                                                    },
                                                    {
                                                        "label": "Histogram",
                                                        "value": "histogram",
                                                    },
                                                    {
                                                        "label": "Line",
                                                        "value": "line",
                                                    },
                                                    {
                                                        "label": "Scatter",
                                                        "value": "scatter",
                                                    },
                                                    {
                                                        "label": "Stack",
                                                        "value": "stack",
                                                    },
                                                    {
                                                        "label": "Text",
                                                        "value": "text",
                                                    },
                                                    {
                                                        "label": "Sample Parser Dataset",
                                                        "value": "parser_data",
                                                    },
                                                ],
                                                value="chords",
                                            ),
                                        ],
                                        className="six columns",
                                    ),
                                    html.Div(
                                        [
                                            html.H5(
                                                "Size Slider"),
                                            html.Div(
                                                [
                                                    dcc.Slider(
                                                        id="size-slider",
                                                        marks={
                                                            500: "Min",
                                                            800: "Max",
                                                        },
                                                        min=500,
                                                        max=800,
                                                        step=10,
                                                        value=600,
                                                    )
                                                ], className="circos-size-slider"
                                            ),
                                        ],
                                        className="six columns",
                                    ),
                                ],
                                className="circos-row-one row",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H5(
                                                "Select Data Set"
                                            ),
                                            dcc.Dropdown(
                                                id="data-selector",
                                                options=[
                                                    {
                                                        "label": "Layout",
                                                        "value": "layout",
                                                    }
                                                ],
                                                value="layout",
                                            ),
                                        ], className="six columns",
                                    ),
                                    html.Div(
                                        [
                                            html.H5(
                                                "Hover/Click Data"
                                            ),
                                            dcc.Textarea(
                                                id="event-data",
                                                placeholder="Hover or click on data to see it here.",
                                                value="Hover or click on data to see it here.",
                                                className="circos-event-data"
                                            ),
                                        ],
                                        className="six columns",
                                    ),
                                ],
                                className="circos-row-two row",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H5(
                                                "Upload Data",
                                                className="circos-select-data-set five columns",
                                            ),
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.A(
                                                                html.Button(
                                                                    "Download",
                                                                    className="circos-button-data five columns",
                                                                ),
                                                                href="/assets/sample_data/circos_sample_data.rar",
                                                                download="circos_sample_data.rar"
                                                            ),
                                                            html.Button(
                                                                "Render",
                                                                id="render-button",
                                                                className="circos-button-render five columns",
                                                            ),
                                                        ], className="row",
                                                    )
                                                ], className="six columns"
                                            )
                                        ],
                                        className="circos-row-three row",
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Textarea(
                                                        value=upload_instructions,
                                                        className="circos-text-area"
                                                    )
                                                ], className="six columns"
                                            ),
                                            html.Div(
                                                [
                                                    dcc.Upload(
                                                        id="upload-data",
                                                        children=html.Div(
                                                            [
                                                                "Drag and Drop .CSV file here!"
                                                            ],
                                                        ),
                                                        className="circos-upload-data",
                                                        multiple=True,
                                                    )
                                                ], className="six columns"
                                            )
                                        ],
                                        className="circos-row-four row",
                                    ),
                                ],
                                className="row",
                            ),
                        ],
                        className="circos-column-one five columns",
                    ),
                    html.Div(
                        id="circos-hold",
                        children=[
                            empty
                        ],
                        className="circos-column-two seven columns",
                    ),
                ], className="row",
            ),
            html.Div(
                [
                    html.Div(id="output-data-upload"),
                    dcc.Interval(
                        id="init", n_intervals=0, interval=100000000),
                ], className="circos-display-none"
            ),
        ]
    )


def callbacks(app):
    @app.callback(
        Output("init", "interval"),
        [Input("init", "n_intervals")]
    )
    def init_callbacks_on_start(init):
        if init >= 1:
            return 10000000000000
        return 1000

    @app.callback(
        Output("data-selector", "options"),
        [Input("circos-hold", "children"),
         Input("circos-selector", "value")],
        [State("main-circos", "tracks")],
    )
    def event_dropdown(dropdown, circos_select, tracks):
        if tracks is not None and circos_select != "custom":
            array = []
            dropdown = []

            for k, v in [(k, v) for x in tracks for (k, v) in x.items()]:
                if k == "type":
                    array.append(v)

            for i in range(len(tracks)):
                if array[i] != "CHORDS":
                    dropdown.append(
                        {"label": "{}".format(array[i]), "value": i})

            dropdown.append({"label": "LAYOUT", "value": "layout"}.copy())
            return dropdown

        elif circos_select == "custom":
            dropdown = [
                {"label": "Layout", "value": 0},
                {"label": "Track One", "value": 1},
                {"label": "Track Two", "value": 2},
            ]
            return dropdown
        else:
            return ["blank"]

    @app.callback(
        Output("output-data-upload", "children"),
        [Input("upload-data", "contents")],
        [State("upload-data", "filename"),
         State("upload-data", "last_modified"),
         State("output-data-upload", "children"),
         State("data-selector", "value"),
         State("circos-selector", "value")]
    )
    def update_output(
        list_of_contents, list_of_names, list_of_dates, data, upload_select, circos_select
    ):
        if data == None:
            array = [None, None, None]
        else:
            array = json.loads(data)

        if list_of_contents is not None:
            children = list(
                (
                    parse_contents(c, n, d)
                    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
                )
            )
            children = children[0]
            array[upload_select] = children
            return json.dumps(array)
        return

    @app.callback(
        Output("circos-hold", "children"),
        [Input("circos-selector", "value"),
         Input("size-slider", "value"),
         Input("init", "n_intervals"),
         Input("render-button", "n_clicks")],
        [State("output-data-upload", "children")],
    )
    def init(circos_select, size, init_onstart, render_button, uploadData):
        if circos_select == "custom" and uploadData != None:
            array = json.loads(uploadData)
            return dash_bio.DashCircos(
                id="main-circos",
                selectEvent={"0": "hover", "1": "click"},
                layout=array[0],
                config={
                    "innerRadius": size / 2 - 80,
                    "outerRadius": size / 2 - 40,
                    "ticks": {"display": False, "labelDenominator": 1000000},
                    "labels": {
                        "position": "center",
                        "display": False,
                        "size": 12,
                        "color": "#000",
                        "radialOffset": 70,
                    },
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": array[1],
                        "config": {
                            "innerRadius": size / 2 - 80,
                            "outerRadius": size / 2 - 40,
                            "opacity": 0.3,
                            "tooltipContent": {"name": "all"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "HIGHLIGHT",
                        "data": array[2],
                        "config": {
                            "innerRadius": size / 2 - 80,
                            "outerRadius": size / 2 - 40,
                            "opacity": 0.3,
                            "tooltipContent": {"name": "all"},
                            "color": {"name": "color"},
                        },
                    },
                ],
                size=800,
                style={"display": "flex", "justify-content": "center"},
            )
        elif circos_select == "parser_data":
            return dash_bio.DashCircos(
                id="main-circos",
                selectEvent={"0": "hover", "1": "click"},
                layout=parsed_layout,
                config={
                    "innerRadius": size / 2 - 80,
                    "outerRadius": size / 2 - 40,
                    "ticks": {"display": False, "labelDenominator": 1000000},
                    "labels": {
                        "position": "center",
                        "display": False,
                        "size": 8,
                        "color": "#000",
                        "radialOffset": 90,
                    },
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": parsed_track_one,
                        "config": {
                                "innerRadius": size / 2 - 80,
                                "outerRadius": size / 2 - 40,
                                "opacity": 0.3,
                                "tooltipContent": {"name": "block_id"},
                                "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "HIGHLIGHT",
                        "data": parsed_track_two,
                        "config": {
                                "innerRadius": size / 2 - 80,
                                "outerRadius": size / 2 - 40,
                                "opacity": 0.3,
                                "tooltipContent": {"name": "block_id"},
                                "color": {"name": "color"},
                        },
                    },
                ],
                size=800,
                style={"display": "flex", "justify-content": "center"}
            )
        elif circos_select == "heatmap":
            return dash_bio.DashCircos(
                id="main-circos",
                selectEvent={"0": "hover", "1": "hover"},
                layout=circos_graph_data["month_layout"],
                config={
                    "innerRadius": (size / 2 - 80),
                    "outerRadius": (size / 2 - 30),
                    "ticks": {"display": False},
                    "labels": {
                        "position": "center",
                        "display": True,
                        "size": 14,
                        "color": "#000",
                        "radialOffset": 15,
                    },
                },
                tracks=[
                    {
                        "type": "HEATMAP",
                        "data": circos_graph_data["heatmap"],
                        "config": {
                            "innerRadius": 0.8,
                            "outerRadius": 0.98,
                            "logScale": False,
                            "color": "YlOrRd",
                            "tooltipContent": {"name": "value"},
                        },
                    },
                    {
                        "type": "HEATMAP",
                        "data": circos_graph_data["heatmap"],
                        "config": {
                            "innerRadius": 0.7,
                            "outerRadius": 0.79,
                            "logScale": False,
                            "color": "Blues",
                            "tooltipContent": {"name": "value"},
                        },
                    },
                ],
                size=800,
                style={"display": "flex", "justify-content": "center"},
            )
        elif circos_select == "chords":
            return dash_bio.DashCircos(
                id="main-circos",
                selectEvent={"0": "both", "1": "both"},
                layout=circos_graph_data["GRCh37"],
                config={
                    "innerRadius": size / 2 - 80,
                    "outerRadius": size / 2 - 40,
                    "ticks": {"display": False, "labelDenominator": 1000000},
                    "labels": {
                        "position": "center",
                        "display": True,
                        "size": 11,
                        "color": "#000",
                        "radialOffset": 75,
                    },
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": circos_graph_data["cytobands"],
                        "config": {
                            "innerRadius": size / 2 - 80,
                            "outerRadius": size / 2 - 40,
                            "opacity": 0.3,
                            "tooltipContent": {"name": "all"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "CHORDS",
                        "data": circos_graph_data["chords"],
                        "config": {
                            "logScale": False,
                            "opacity": 0.7,
                            "color": "#ff5722",
                            "tooltipContent": {
                                "source": "source",
                                "sourceID": "id",
                                "target": "target",
                                "targetID": "id",
                                "targetEnd": "end",
                            },
                        },
                    },
                ],
                size=800,
                style={"display": "flex", "justify-content": "center"},
            )
        elif circos_select == "highlight":
            return dash_bio.DashCircos(
                id="main-circos",
                selectEvent={"0": "hover"},
                layout=circos_graph_data["GRCh37"],
                config={
                    "innerRadius": size / 2 - 100,
                    "outerRadius": size / 2 - 50,
                    "ticks": {"display": False},
                    "labels": {"display": False},
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": circos_graph_data["cytobands"],
                        "config": {
                            "innerRadius": size / 2 - 100,
                            "outerRadius": size / 2 - 50,
                            "opacity": 0.5,
                            "tooltipContent": {"name": "name"},
                            "color": {"name": "color"},
                        },
                    }
                ],
                size=800,
                style={"display": "flex", "justify-content": "center"},
            )

        elif circos_select == "histogram":
            return dash_bio.DashCircos(
                id="main-circos",
                layout=circos_graph_data["GRCh37"],
                selectEvent={"0": "hover", "1": "hover"},
                config={
                    "innerRadius": size / 2 - 150,
                    "outerRadius": size / 2 - 120,
                    "ticks": {"display": False, "labelDenominator": 1000000},
                    "labels": {"display": False},
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": circos_graph_data["cytobands"],
                        "config": {
                            "innerRadius": size / 2 - 150,
                            "outerRadius": size / 2 - 120,
                            "opacity": 0.6,
                            "tooltipContent": {"name": "name"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "HISTOGRAM",
                        "data": circos_graph_data["histogram"],
                        "config": {
                            "innerRadius": 1.01,
                            "outerRadius": 1.4,
                            "color": "OrRd",
                            "tooltipContent": {"name": "value"},
                        },
                    },
                ],
                size=800,
                style={"display": "flex", "justify-content": "center"},
            )
        elif circos_select == "line":
            return dash_bio.DashCircos(
                id="main-circos",
                selectEvent={"0": "both", "1": "both", "2": "both", "3": "both", "4": "both" ,"5": "both", "6": "both", "7":"both"},
                layout=list(
                    filter(lambda d: d["id"] in [
                        "chr1", "chr2", "chr3"], circos_graph_data["GRCh37"])
                ),
                config={
                    "innerRadius": size / 2 - 150,
                    "outerRadius": size / 2 - 130,
                    "ticks": {
                        "display": False,
                        "spacing": 1000000,
                        "labelSuffix": "",
                    },
                    "labels": {
                        "position": "center",
                        "display": False,
                        "size": 14,
                        "color": "#000",
                        "radialOffset": 30,
                    },
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": list(
                            filter(
                                lambda d: d["block_id"] in [
                                    "chr1", "chr2", "chr3"],
                                circos_graph_data["cytobands"],
                            )
                        ),
                        "config": {
                            "innerRadius": size / 2 - 150,
                            "outerRadius": size / 2 - 130,
                            "opacity": 0.3,
                            "tooltipContent": {"name": "name"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "LINE",
                        "data": circos_graph_data["snp250"],
                        "config": {
                            "innerRadius": 0.5,
                            "outerRadius": 0.8,
                            "color": "#222222",
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                            "axes": [
                                {"spacing": 0.001, "thickness": 1,
                                    "color": "#666666"}
                            ],
                            "backgrounds": [
                                {
                                    "start": 0,
                                    "end": 0.002,
                                    "color": "#f44336",
                                    "opacity": 0.5,
                                },
                                {
                                    "start": 0.006,
                                    "end": 0.015,
                                    "color": "#4caf50",
                                    "opacity": 0.5,
                                },
                            ],
                            "maxGap": 1000000,
                            "min": 0,
                            "max": 0.015,
                        },
                    },
                    {
                        "type": "SCATTER",
                        "data": circos_graph_data["snp250"],
                        "config": {
                            "innerRadius": 0.5,
                            "outerRadius": 0.8,
                            "min": 0,
                            "max": 0.015,
                            "fill": False,
                            "strokeWidth": 0,
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                        },
                    },
                    {
                        "type": "LINE",
                        "data": circos_graph_data["snp"],
                        "config": {
                            "innerRadius": 1.01,
                            "outerRadius": 1.15,
                            "maxGap": 1000000,
                            "min": 0,
                            "max": 0.015,
                            "color": "#222222",
                            "tooltipContent": {"name": "value"},
                            "axes": [
                                {"position": 0.002, "color": "#f44336"},
                                {"position": 0.006, "color": "#4caf50"},
                            ],
                        },
                    },
                    {
                        "type": "LINE",
                        "data": circos_graph_data["snp1m"],
                        "config": {
                            "innerRadius": 1.01,
                            "outerRadius": 1.15,
                            "maxGap": 1000000,
                            "min": 0,
                            "max": 0.015,
                            "color": "#f44336",
                            "tooltipContent": {"name": "value"},
                        },
                    },
                    {
                        "type": "LINE",
                        "data": circos_graph_data["snp"],
                        "config": {
                            "innerRadius": 0.85,
                            "outerRadius": 0.95,
                            "maxGap": 1000000,
                            "direction": "in",
                            "min": 0,
                            "max": 0.015,
                            "color": "#222222",
                            "axes": [
                                {"position": 0.01, "color": "#4caf50"},
                                {"position": 0.008, "color": "#4caf50"},
                                {"position": 0.006, "color": "#4caf50"},
                                {"position": 0.002, "color": "#f44336"},
                            ],
                        },
                    },
                    {
                        "type": "LINE",
                        "data": circos_graph_data["snp1m"],
                        "config": {
                            "innerRadius": 0.85,
                            "outerRadius": 0.95,
                            "maxGap": 1000000,
                            "direction": "in",
                            "min": 0,
                            "max": 0.015,
                            "color": "#f44336",
                            "tooltipContent": {"name": "value"},
                        },
                    },
                ],
                size=800,
                style={"display": "flex", "justify-content": "center"},
            )
        elif circos_select == "scatter":
            return dash_bio.DashCircos(
                id="main-circos",
                selectEvent={"0": "hover", "1": "both", "3": "both", "4": "both", "5": "both"},
                layout=list(
                    filter(lambda d: d["id"] in [
                        "chr1", "chr2", "chr3"], circos_graph_data["GRCh37"])
                ),
                config={
                    "innerRadius": size / 2 - 150,
                    "outerRadius": size / 2 - 130,
                    "ticks": {
                        "display": False,
                        "spacing": 1000000,
                        "labelSuffix": "",
                    },
                    "labels": {"display": False},
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": list(
                            filter(
                                lambda d: d["block_id"] in [
                                    "chr1", "chr2", "chr3"],
                                circos_graph_data["cytobands"],
                            )
                        ),
                        "config": {
                            "innerRadius": size / 2 - 150,
                            "outerRadius": size / 2 - 130,
                            "opacity": 0.8,
                            "tooltipContent": {"name": "name"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "SCATTER",
                        "data": list(
                            filter(lambda d: float(
                                d["value"]) > 0.007, circos_graph_data["snp250"])
                        ),
                        "config": {
                            "innerRadius": 0.65,
                            "outerRadius": 0.95,
                            "color": {"colorData": "name"},
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                            "strokeColor": "grey",
                            "strokeWidth": 1,
                            "shape": "circle",
                            "size": 14,
                            "min": 0,
                            "max": 0.013,
                            "axes": [
                                {
                                    "spacing": 0.001,
                                    "start": 0.006,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.3,
                                },
                                {
                                    "spacing": 0.002,
                                    "start": 0.006,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.5,
                                },
                                {
                                    "spacing": 0.002,
                                    "start": 0.002,
                                    "end": 0.006,
                                    "thickness": 1,
                                    "color": "#666",
                                    "opacity": 0.5,
                                },
                                {
                                    "spacing": 0.001,
                                    "end": 0.002,
                                    "thickness": 1,
                                    "color": "#f44336",
                                    "opacity": 0.5,
                                },
                            ],
                            "backgrounds": [
                                {"start": 0.006, "color": "#4caf50", "opacity": 0.1},
                                {
                                    "start": 0.002,
                                    "end": 0.006,
                                    "color": "#d3d3d3",
                                    "opacity": 0.1,
                                },
                                {"end": 0.002, "color": "#f44336", "opacity": 0.1},
                            ],
                        },
                    },
                    {
                        "type": "SCATTER",
                        "data": circos_graph_data["snp250"],
                        "config": {
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                            "color": "#4caf50",
                            "strokeColor": "green",
                            "strokeWidth": 1,
                            "shape": "rectangle",
                            "size": 10,
                            "min": 0.007,
                            "max": 0.013,
                            "innerRadius": 1.075,
                            "outerRadius": 1.175,
                            "axes": [
                                {
                                    "spacing": 0.001,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.3,
                                },
                                {
                                    "spacing": 0.002,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.5,
                                },
                            ],
                            "backgrounds": [
                                {"start": 0.007, "color": "#4caf50", "opacity": 0.1},
                                {"start": 0.009, "color": "#4caf50", "opacity": 0.1},
                                {"start": 0.011, "color": "#4caf50", "opacity": 0.1},
                                {"start": 0.013, "color": "#4caf50", "opacity": 0.1},
                            ],
                        },
                    },
                    {
                        "type": "SCATTER",
                        "data": list(
                            filter(lambda d: float(
                                d["value"]) < 0.002, circos_graph_data["snp250"])
                        ),
                        "config": {
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                            "color": "#f44336",
                            "strokeColor": "red",
                            "strokeWidth": 1,
                            "shape": "triangle",
                            "size": 10,
                            "min": 0,
                            "max": 0.002,
                            "innerRadius": 0.35,
                            "outerRadius": 0.60,
                            "axes": [
                                {
                                    "spacing": 0.0001,
                                    "thickness": 1,
                                    "color": "#f44336",
                                    "opacity": 0.3,
                                },
                                {
                                    "spacing": 0.0005,
                                    "thickness": 1,
                                    "color": "#f44336",
                                    "opacity": 0.5,
                                },
                            ],
                            "backgrounds": [
                                {"end": 0.0004, "color": "#f44336", "opacity": 0.1},
                                {"end": 0.0008, "color": "#f44336", "opacity": 0.1},
                                {"end": 0.0012, "color": "#f44336", "opacity": 0.1},
                                {"end": 0.0016, "color": "#f44336", "opacity": 0.1},
                                {"end": 0.002, "color": "#f44336", "opacity": 0.1},
                            ],
                        },
                    },
                    {
                        "type": "SCATTER",
                        "data": circos_graph_data["snp250"],
                        "config": {
                            "tooltipContent": {
                                "source": "block_id",
                                "target": "position",
                                "targetEnd": "value",
                            },
                            "innerRadius": 0.65,
                            "outerRadius": 0.95,
                            "strokeColor": "grey",
                            "strokeWidth": 1,
                            "shape": "circle",
                            "size": 14,
                            "min": 0,
                            "max": 0.013,
                            "axes": [
                                {
                                    "spacing": 0.001,
                                    "start": 0.006,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.3,
                                },
                                {
                                    "spacing": 0.002,
                                    "start": 0.006,
                                    "thickness": 1,
                                    "color": "#4caf50",
                                    "opacity": 0.5,
                                },
                                {
                                    "spacing": 0.002,
                                    "start": 0.002,
                                    "end": 0.006,
                                    "thickness": 1,
                                    "color": "#666",
                                    "opacity": 0.5,
                                },
                                {
                                    "spacing": 0.001,
                                    "end": "0.002",
                                    "thickness": 1,
                                    "color": "#f44336",
                                    "opacity": 0.5,
                                },
                            ],
                            "backgrounds": [
                                {"start": 0.006, "color": "#4caf50", "opacity": 0.1},
                                {
                                    "start": 0.002,
                                    "end": 0.006,
                                    "color": "#d3d3d3",
                                    "opacity": 0.1,
                                },
                                {"end": 0.002, "color": "#f44336", "opacity": 0.1},
                            ],
                        },
                    },
                ],
                size=800,
                style={"display": "flex", "justify-content": "center"},
            )
        elif circos_select == "stack":
            return dash_bio.DashCircos(
                id="main-circos",
                selectEvent={"0": "hover"},
                layout=[
                    {"id": "chr9", "len": 8000000,
                        "label": "chr9", "color": "#FFCC00"}
                ],
                config={
                    "innerRadius": size / 2 - 50,
                    "outerRadius": size / 2 - 30,
                    "ticks": {
                        "display": False,
                        "labels": False,
                        "spacing": 10000,
                    },
                    "labels": {
                        "display": False,
                        "labels": False,
                        "spacing": 10000,
                    },
                },
                tracks=[
                    {
                        "type": "STACK",
                        "data": circos_graph_data["stack"],
                        "config": {
                            "innerRadius": 0.7,
                            "outerRadius": 1,
                            "thickness": 4,
                            "margin": 0.01 * 8000000,
                            "direction": "out",
                            "strokeWidth": 0,
                            "opacity": 0.5,
                            "color": "#d3d3d3",
                            "tooltipContent": {"name": "chr"},
                            "color": {
                                "conditional": {
                                    "end": "end",
                                    "start": "start",
                                    "value": [150000, 120000, 90000, 60000, 30000],
                                    "color": [
                                        "red",
                                        "black",
                                        "#000000",
                                        "#999",
                                        "#BBB",
                                    ],
                                }
                            }
                        },
                    }
                ],
                size=800,
                style={"display": "flex", "justify-content": "center"},
            )
        elif circos_select == "text":
            return dash_bio.DashCircos(
                id="main-circos",
                selectEvent={"0": "hover", "1": "both"},
                layout=[circos_graph_data["GRCh37"][0]],
                config={
                    "innerRadius": size / 2 - 100,
                    "outerRadius": size / 2 - 80,
                    "labels": {"display": False},
                    "ticks": {"display": False},
                },
                tracks=[
                    {
                        "type": "HIGHLIGHT",
                        "data": list(
                            filter(
                                lambda d: d["block_id"] == circos_graph_data["GRCh37"][0]["id"],
                                circos_graph_data["cytobands"],
                            )
                        ),
                        "config": {
                            "innerRadius": size / 2 - 100,
                            "outerRadius": size / 2 - 80,
                            "opacity": 0.7,
                            "tooltipContent": {"name": "name"},
                            "color": {"name": "color"},
                        },
                    },
                    {
                        "type": "TEXT",
                        "data": list(
                            map(
                                lambda d: {
                                    "position": (d["start"] + d["end"]) / 2,
                                    "value": d["name"],
                                    "block_id": d["block_id"],
                                },
                                filter(
                                    lambda d: d["block_id"] == circos_graph_data["GRCh37"][0]["id"],
                                    circos_graph_data["cytobands"],
                                ),
                            )
                        ),
                        "config": {
                            "innerRadius": 1.02,
                            "outerRadius": 1.3,
                            "style": {"font-size": 12},
                        },
                    },
                ],
                size=800,
                style={"display": "flex", "justify-content": "center"},
            )
        return empty

    @app.callback(
        Output("data-table", "data"),
        [Input("data-selector", "value"),
         Input("render-button", "n_clicks"),
         Input("data-selector", "options"),
         Input("data-table", "selected_cells")],
        [State("main-circos", "layout"),
         State("main-circos", "tracks")],
    )
    def update_table_rows(data_selector, render_button, circos_trigger, selected, layout, tracks):
        try:
            if data_selector == "layout":
                df = pd.DataFrame(layout)
            else:
                df = pd.DataFrame(tracks[data_selector]["data"])
            return df.to_dict("records")
        except:
            df = pd.DataFrame() 
            return df

    @app.callback(
        Output("data-table", "columns"),
        [Input("data-selector", "value"),
         Input("render-button", "n_clicks"),
         Input("data-selector", "options"),
         Input("data-table", "selected_cells")],
        [State("main-circos", "layout"),
         State("main-circos", "tracks")],
    )
    def update_table_columns(data_selector, render_button, circos_trigger, selected, layout, tracks):
        try:
            if data_selector == "layout":
                df = pd.DataFrame(layout)
            else:
                df = pd.DataFrame(tracks[data_selector]["data"])
            return [{'id': i, 'name': i} for i in df.columns]
        except:
            df = pd.DataFrame() 
            return df
    @app.callback(
        Output("event-data", "value"),
        [Input("main-circos", "eventDatum")]
    )
    def event_data(eventDatum):
        return str(eventDatum)

