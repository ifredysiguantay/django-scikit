from django.shortcuts import render
import numpy as np 
from sklearn.linear_model import LinearRegression


def pie_chart(request):
    labels = []
    data = []

    cursor.execute("select table_one.precio_unitario from table_one where nombre_producto ='{0}'".format(data))
    id_search = cursor.fetchall()
    id_search = id_search[0][0]

    cursor.execute("select unidades_vendidas,numero_semana from table_three where product_name = '{0}'".format(id_search))

    data = cursor.fetchall()

    x_arr y_arr = [],[]

    for a,b in data:
        x_arr.append(a[0])
        y_arr.append(b[0])

    x = np.array(x_arr).reshape((-1,1))
    y = np.array(y_arr).

    model = LinearRegression()

    model.fit(x,y)


    y_pred = model.predict(x)

    return render(request, 'pie_chart.html', {
        'labels': y_arr,
        'data': y_pred,
    })
