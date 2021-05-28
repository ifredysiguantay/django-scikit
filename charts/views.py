from django.shortcuts import render
import numpy as np 
from sklearn.linear_model import LinearRegression
from django.db import connections
from sklearn.preprocessing import PolynomialFeatures
cursor = connections['default'].cursor()
def pie_chart(request):
    if request.method == 'POST':
        labels = []
        data = []
        data_request = request.POST.get('data')
        cursor.execute("select table_one.id from table_one where nombre_producto ='{0}'".format(data_request))
        id_search = cursor.fetchall()
        
        id_search = id_search[0][0]
        cursor.execute("select unidades_vendidas,numero_semana from table_three where product_name = '{0}'".format(id_search))

        data = cursor.fetchall()

        x_arr,y_arr = [],[]

        for a,b in data:
            tmp = b.split('-')
            x_arr.append(a)
            y_arr.append(tmp[1])

        x = np.array(x_arr).reshape((-1,1))
        y = np.array(y_arr)

        model = LinearRegression()

     

        x_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(x)
        model = LinearRegression().fit(x_, y)


        y_pred = model.predict(x_)
        return render(request, 'pie_chart.html', {
            'labels': y_arr,
            'data': list(y_pred),
        })
    else:
        return render(request,'form_action.html')

