from django.shortcuts import render
import numpy as np
from django.db import connections
np.set_printoptions(threshold=np.inf)
import pandas as pd
from sklearn.linear_model import LinearRegression
import warnings
from django.http import HttpResponse, HttpResponseNotFound
warnings.filterwarnings(action="ignore", module="sklearn", message="^internal gelsd")
cursor = connections['default'].cursor()

def linearizer(lowerLimit, upperLimit):
    upperLimit += 1
    out = []
    while (lowerLimit < upperLimit):
        out.append(lowerLimit)
        lowerLimit += 1
    return out 


def pie_chart(request):
    if request.method == 'POST':
        labels_chart = []
        data_chart = []
        sales_quantity = []

        data_request = request.POST.get('data')
        cursor.execute("select table_one.id,table_one.precio_unitario from table_one where nombre_producto ='{0}'".format(data_request))
        id_search = cursor.fetchall()
        
        
        if(not len(id_search)):
            return HttpResponseNotFound('<h1>Producto no encontrado</h1>')

        price_product = id_search[0][1]
        id_search = id_search[0][0]
        
        
        cursor.execute("select unidades_vendidas from table_three where product_name = '{0}'".format(id_search))

        data = cursor.fetchall()
        input_data = pd.DataFrame(list(data))

        y = input_data.iloc[:,0]
        length_y = len(y.index)

        x = []

        x = linearizer(0,(length_y -1))

        x = pd.DataFrame(x)

        model = LinearRegression()
        model.fit(x,y)

        positionToPredict =  request.POST.get('weeks')

        positionToPredict = int(positionToPredict)

        new_data = linearizer(length_y,(positionToPredict + length_y))

        new_data = pd.DataFrame(new_data)
        prediction = model.predict(new_data)
    
        
        for a in range(1,len(prediction)):
            labels_chart.append(a)
        for b in list(prediction):
            data_chart.append(price_product*round(b))
            sales_quantity.append(round(b))
        sales_quantity.pop()
        return render(request, 'pie_chart.html', {
            'labels':labels_chart,
            'data': data_chart,
            'sales_quantity':sales_quantity,
            'price_product':price_product
        })
    else:
        return render(request,'form_action.html')

