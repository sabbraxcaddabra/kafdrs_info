from dash import dcc, html, dash_table
from dash import Input, Output, State, callback
import json

import dash_bootstrap_components as dbc

import pandas as pd

with open('./data/kaf.json', encoding='utf8') as spec_codes:
    SPEC_CODES_DICT = json.load(spec_codes)

with open('./data/stat_years.json', encoding='utf8') as stats:
    STATS_DICT = json.load(stats)

with open('./data/to_rus.json', encoding='utf8') as localize_fp:
    LOCALIZE_DICT = json.load(localize_fp)

DEFAULT_DICT = {
    "code": "-",
    "name": "-",
    "count_human": 0,
    "count_apps": 0,
    "count_apps_obsh": 0,
    "sred_obsh": None,
    "count_apps_cel": 0,
    "sred_cel": None,
    "count_apps_kvot": 0,
    "sred_kvot": None,
    "count_apps_plat": 0,
    "sred_plat": None,
    "count_apps_obsh_post": 0,
    "sred_obsh_post": None,
    "min_obsh_post": 0,
    "count_apps_cel_post": 0,
    "sred_cel_post": None,
    "min_cel_post": 0,
    "count_apps_kvot_post": 0,
    "sred_kvot_post": None,
    "min_kvot_post": 0,
    "count_apps_plat_post": 0,
    "sred_plat_post": None,
    "min_plat_post": 0
}


def get_spec_codes(kaf_name):
    return SPEC_CODES_DICT[kaf_name]

def get_spec_code_stats(spec_code):
    all_year_dict = {key: val.get(spec_code, DEFAULT_DICT) for key, val in STATS_DICT.items()}
    return all_year_dict

def get_stats_df(stats_dict):
    for key in stats_dict:
        st_dict = stats_dict[key]
        if 'code' in st_dict.keys():
            del st_dict['code'], st_dict['name']

    df = {'Показатель': stats_dict['2022'].keys()}

    for key in stats_dict:
        df[key] = stats_dict[key].values()

    df = pd.DataFrame(df)

    return df


def generate_layout(kaf_name):
    spec_codes = get_spec_codes(kaf_name=kaf_name)
    options = {spec_code: f'{spec_code} - {STATS_DICT["2022"][spec_code]["name"]}' for spec_code in spec_codes}
    stats =  html.Div([
        html.H2(children=f'Статистика кафедры {kaf_name}', id='h1'),
        dcc.Dropdown(options=options, value=spec_codes[0], id='spec_codes', multi=False, clearable=False),
        html.Br(),
        dbc.Col(
            html.Div(children='', id='kaf_stats')
        ),
    ])

    return stats


@callback(
    Output('kaf_stats', 'children'),
    [Input('spec_codes', 'value')]
)
def get_stats(spec_code):

    df = get_stats_df(get_spec_code_stats(spec_code))

    df['Показатель'] = df['Показатель'].apply(lambda var_name: LOCALIZE_DICT.get(var_name))

    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_cell={'textAlign': 'left', 'minWidth': '100px'},
        export_format='xlsx'
        )
