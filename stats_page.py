from dash import dcc, html, dash_table
from dash import Input, Output, State, callback
import json

import pandas as pd

with open('./data/kaf.json', encoding='utf8') as spec_codes:
    SPEC_CODES_DICT = json.load(spec_codes)

with open('./data/stat2022.json', encoding='utf8') as stats:
    STATS_DICT = json.load(stats)

with open('./data/to_rus.json', encoding='utf8') as localize_fp:
    LOCALIZE_DICT = json.load(localize_fp)


def get_spec_codes(kaf_name):
    return SPEC_CODES_DICT[kaf_name]

def get_spec_code_stats(spec_code):
    return STATS_DICT[spec_code]

def generate_layout(kaf_name):
    spec_codes = get_spec_codes(kaf_name=kaf_name)
    options = {spec_code: f'{spec_code} - {STATS_DICT[spec_code]["name"]}' for spec_code in spec_codes}
    stats =  html.Div([
        html.H2(children=f'Статистика кафедры {kaf_name}', id='h1'),
        dcc.Dropdown(options=options, value=spec_codes[0],id='spec_codes', multi=False, clearable=False),
        html.Br(),
        html.Div(children='', id='kaf_stats')
    ])

    return stats


@callback(
    Output('kaf_stats', 'children'),
    [Input('spec_codes', 'value')]
)
def get_stats(spec_code):
    stats_dict = get_spec_code_stats(spec_code)

    if 'code' in stats_dict.keys():
        del stats_dict['code'], stats_dict['name']

    df = pd.DataFrame(data=dict(
        var=list(stats_dict.keys()),
        val=list(stats_dict.values())
    ))

    df['var'] = df['var'].apply(lambda var_name: LOCALIZE_DICT.get(var_name))

    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_cell={'textAlign': 'left'},
        )
