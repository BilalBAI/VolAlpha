import os
import pandas as pd
from pandas import DataFrame
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Group, Scheme, Sign
import plotly.graph_objs as go

from cftl_common.config import get_config
from cftl_common.clients.stash import StashClient


def money(decimals, sign=Sign.default):
    return Format(group=Group.yes, precision=decimals, scheme=Scheme.fixed, sign=sign)


EQOPT_COLUMNS = [
    {
        "id": "product",
        "name": "Product",
        "type": "text"
    }, {
        "id": "BidAsk",
        "name": "BidAsk",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "Concentration",
        "name": "Concentration",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "TermStructure",
        "name": "TermStructure",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "Skew",
        "name": "Skew",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "Sum",
        "name": "Sum",
        "type": "numeric",
        "format": money(0)
    }
]

IROPT_COLUMNS = [
    {
        "id": "product",
        "name": "Product",
        "type": "text"
    }, {
        "id": "Ccy",
        "name": "Currency",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "Hccy",
        "name": "Hccy",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "Hcontract",
        "name": "Hcontract",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "HedgeCharge",
        "name": "HedgeCharge",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "ExitChargeA",
        "name": "ExitChargeA",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "ExitChargeB",
        "name": "ExitChargeB",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "ExitCharge",
        "name": "ExitCharge",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "Fees",
        "name": "Fees",
        "type": "numeric",
        "format": money(0)
    }, {
        "id": "Sum",
        "name": "Sum",
        "type": "numeric",
        "format": money(0)
    }
]


class DashApp:

    def __init__(self):
        self.config = config = get_config()
        auth = (os.getenv('USERNAME'), os.getenv('PASSWORD'))
        self.stash = StashClient(**config['stash-config'], auth=auth)
        self.engine_hist = self.config['DB_HIST']
        self.app = app = dash.Dash(__name__)
        # Dash app setup
        self.app.layout = html.Div(
            html.Div(
                [
                    html.H2('Risk Monitor',
                            style={'color': 'white'}),
                    dcc.Interval(
                        id='interval-component',
                        interval=1 * 1000,   # in milliseconds
                        n_intervals=0
                    ),
                    html.H4(id='total_risk'),
                    html.H4(id='update_time', style={'color': 'white'}),
                    html.H4('Currency: USD', style={'color': 'white'}),
                    html.H3('Hist Liquidity Risk', style={'color': 'white'}),
                    dcc.Dropdown(
                        id='hist-dropdown',
                        options=[{
                            'label': book,
                            'value': book
                        } for book in self.config['all-books']],
                        value='Total',
                    ),
                    dcc.Graph(id='hist', style={'backgroundColor': 'black'}),
                    html.H3('Equity Options: Book Level',
                            style={'color': 'white'}),
                    dash_table.DataTable(
                        id='eq_options_b',
                        columns=EQOPT_COLUMNS,
                        sort_action="native",
                        sort_mode='multi',
                        style_header={
                            'backgroundColor': 'rgb(0, 0, 0)',
                            'fontSize': 15
                        },
                        style_cell={
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white',
                            'fontSize': 13
                        }
                    ),
                    html.H3('Equity Options: Product Level',
                            style={'color': 'white'}),
                    dash_table.DataTable(
                        id='eq_options_p',
                        columns=EQOPT_COLUMNS,
                        sort_action="native",
                        sort_mode='multi',
                        style_header={
                            'backgroundColor': 'rgb(0, 0, 0)',
                            'fontSize': 15
                        },
                        style_cell={
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white',
                            'fontSize': 13
                        }
                    ),
                    html.H3('Interest Rate Options: Book Level',
                            style={'color': 'white'}),
                    dash_table.DataTable(
                        id='ir_options_b',
                        columns=IROPT_COLUMNS,
                        sort_action="native",
                        sort_mode='multi',
                        style_header={
                            'backgroundColor': 'rgb(0, 0, 0)',
                            'fontSize': 15
                        },
                        style_cell={
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white',
                            'fontSize': 13
                        }
                    ),
                    html.H3('Interest Rate Options: Product Level',
                            style={'color': 'white'}),
                    dash_table.DataTable(
                        id='ir_options_p',
                        columns=IROPT_COLUMNS,
                        sort_action="native",
                        sort_mode='multi',
                        style_header={
                            'backgroundColor': 'rgb(0, 0, 0)',
                            'fontSize': 15
                        },
                        style_cell={
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white',
                            'fontSize': 13
                        }
                    )
                ]
            )
        )

        @app.callback(
            [
                Output('eq_options_b', 'data'),
                Output('eq_options_p', 'data'),
                Output('ir_options_b', 'data'),
                Output('ir_options_p', 'data'),
                Output('total_risk', 'children'),
                Output('update_time', 'children')
            ], [Input('interval-component', 'n_intervals')]
        )
        def update_output(n_):
            results = self.stash.get_item(
                self.config['stash-config']['stash_subdir']).json()
            data = DataFrame(results['data'])
            data = data[data['scenario'] == 'Liquidity']
            total_risk = data[(data['group'] == 'Total') & (data['product'] == 'Sum') &
                              (data['measure'] == 'Sum')]['value'].sum()
            if results['missing'] != []:
                total = html.H3(
                    children=f"Total Risk: {total_risk:,.0f}   Missing Books: {
                        results['missing']}",
                    style={
                        'color': 'white',
                        'backgroundColor': 'red'
                    }
                )
            else:
                total = html.H3(
                    children=f"Total Risk: {total_risk:,.0f}",
                    style={
                        'color': 'white',
                        "border": "2px yellow solid",
                        "width": "200px"
                    }
                )
            ixb, ixp = self.grouping(data, 'ix')
            irb, irp = self.grouping(data, 'ir')
            return ixb.to_dict('records'), ixp.to_dict('records'), irb.to_dict('records'), irp.to_dict(
                'records'
            ), total, f"Time Updated: {results['timestamp']}"

        @app.callback(dash.dependencies.Output('hist', 'figure'), [dash.dependencies.Input('hist-dropdown', 'value')])
        def update_figure(value):
            if value == 'Select Book':
                fig = go.Figure(data=[go.Scatter(x=[], y=[])])
            else:
                book_hist = self.hist_data(value)
                fig = go.Figure(data=[go.Scatter(
                    x=book_hist['date'].to_list(), y=book_hist['value'].to_list())])
            fig.layout.template = 'plotly_dark'
            return fig

    def hist_data(self, group):
        df = pd.read_sql(
            f"""select * from crest_option where "group"='{
                group}' AND product='Sum' AND measure='Sum' AND scenario='Liquidity'""",
            con=self.engine_hist
        )
        df = df[['date', 'value']].groupby(by='date', as_index=False).sum()
        return df

    def grouping(self, data, type_):
        df = data[(data['type'] == type_) & (data['scenario'] == 'Liquidity')]
        dfb = df[df['product'] == 'Sum']
        dfb = dfb.pivot_table(
            index='group', columns='measure', values='value').reset_index()
        dfb = dfb.rename(columns={'group': 'product'})
        dfb.columns.name = None
        dfp = df[df['group'] == 'Total']
        dfp = dfp.pivot_table(
            index='product', columns='measure', values='value').reset_index()
        dfp.columns.name = None
        return dfb.sort_values(by='Sum', ascending=False), dfp.sort_values(by='Sum', ascending=False)

    def run_server(self):
        self.app.run_server(**self.config['server_config'])
