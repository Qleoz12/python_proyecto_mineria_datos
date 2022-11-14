from dash import dash_table


def generate_table(dataframe, id, page_size=10, ):
    # return html.Table([
    #     html.Thead(
    #         html.Tr([html.Th(col) for col in dataframe.columns])
    #     ),
    #     html.Tbody([
    #         html.Tr([
    #             html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
    #         ]) for i in range(min(len(dataframe), max_rows))
    #     ])
    # ])
    return dash_table.DataTable(
        id=id,
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size,
        style_table={'overflowX': 'auto'},
    )


def data_imports(df):
    imports_departmens = {"91": "AMAZONAS", "05": "ANTIOQUIA", "81": "ARAUCA", "08": "ATLANTICO", "13": "BOLIVAR",
                          "15": "BOYACA", "17": "CALDAS", "18": "CAQUETA", "85": "CASANARE", "19": "CAUCA",
                          "20": "CESAR", "27": "CHOCO", "23": "CORDOBA", "25": "CUNDINAMARCA", "94": "GUANIA",
                          "44": "GUAJIRA", "95": "GUAVIARE", "41": "HUILA", "47": "MAGDALENA", "50": "META",
                          "52": "NARIÑO", "54": "NORTE DE SANTANDER", "86": "PUTUMAYO", "63": "QUINDIO",
                          "66": "RISARALDA", "88": "SAN ANDRES", "11": "SANTAFE DE BOGOTA", "68": "SANTANDER",
                          "70": "SUCRE", "73": "TOLIMA", "76": "VALLE DEL CAUCA", "97": "VAUPES", "99": "VICHADA"}

    df['Name'] = df['DEPIM'].apply(lambda x: imports_departmens.get(x))
    cols = df.columns.tolist()
    id = cols[0]
    cols = cols[-1:] + cols[1:-1]
    cols.insert(0, id)
    df = df[cols]

    return df
