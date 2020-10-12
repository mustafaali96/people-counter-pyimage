import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

X = deque(maxlen=40)
X.append(1)
Y = deque(maxlen=40)
Y.append(1)
people_count = 0

    
app = dash.Dash()
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals = 0
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')])

    
def update_graph_scatter(n):
    f = open("total_peoples.txt", "r")
    f = f.readlines()
    #print(f[0], type(f))
    people_count = int(f[0])
    X.append(X[-1]+1)
    Y.append(people_count)
    #Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}





app.run_server(debug=True)