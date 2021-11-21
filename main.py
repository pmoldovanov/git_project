import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
from datetime import datetime


zipfile = "zip://D:/Документы/My/test/test_polygons.zip!test_polygons/test.shp"
test=gpd.read_file(zipfile) #,ignore_fields=["iso_a3", "gdp_md_est"],

test=test.to_crs({'proj':'cea'}) # пришлось делать преобразованиен, иначе выходил Warning

verbose=False


def timeit2(func):
    def wrapper():
        start = datetime.now()
        func()
        end =datetime.now()
        duration=end-start
        d= duration.total_seconds() 
        print ( f'[{func.__name__}]  Start:{start}  End:{end} Duration: {d} s')
    return wrapper

def timeit3(func):
    def wrapper():
        start = datetime.now()
        func()
        end =datetime.now()
        duration=end-start
        d= duration.total_seconds() 
        print ( f'[{func.__name__}]  Duration: {d} s')
    return wrapper

class timeit(object):
    def __init__(self,  condition):
        self.condition = condition
   
    def __call__(self, func):
        if not self.condition:
            return timeit3(func)
        return timeit2(func)

@timeit(verbose)
def zadanie1():

    # # начальная фигура 
    # fig, (ax1) = plt.subplots(1, 1, figsize=(10,10))
    # test.plot(ax=ax1, color='green', edgecolor='red')
    # plt.show()

    df = pd.DataFrame(test.drop(columns=['geometry','VALUE','ID']))

    df['CNT']=1
    df_group=df.groupby(['CATEGORY']).count()
    df_group['percent'] = 100*df_group['CNT'] / len(df.index)

    # показываем сводную таблицу
    print(df_group)


    # рисуем круговую диаграмму
    plt.pie(df_group['percent']) 
    plt.legend(df_group.index, loc="upper right")
    plt.show()




@timeit(verbose)
def zadanie2():
    Result = pd.DataFrame(columns=[ 'geometry','VALUE'])
 
    test_list=test.index.to_list()
    for index in test_list:
        for index2  in test_list:
            if index2<=index:continue # пропускаем уже пройденные полигоны

            POLY_1=test[test.index == index].drop(['ID','CATEGORY'],axis=1) 
            POLY_2=test[test.index == index2].drop(['ID','CATEGORY'],axis=1) 

            NEW_POLY_1 = gpd.overlay(POLY_1,POLY_2,how='intersection') # полигон пересечений

            # раскоментировать, если нужно посмотреть фигуры пересечений
            # fig, (ax1) = plt.subplots(1, 1, figsize=(5,5))
            # POLY_1.plot(ax=ax1, color='green', edgecolor='black')
            # POLY_2.plot(ax=ax1, color='blue', edgecolor='black')
            # NEW_POLY_1.plot(ax=ax1, color='red', edgecolor='black')
            # plt.show()

            if NEW_POLY_1.shape[0] > 0:  # нашли пересеченияё
                
                poly_1_value=POLY_1['VALUE'].values[0]
                poly_2_value=POLY_2['VALUE'].values[0]
                poly_1_area=POLY_1['geometry'].area.values[0] /10**6
                poly_2_area=POLY_2['geometry'].area.values[0] /10**6
                new_poly_1_area=NEW_POLY_1['geometry'].area.values[0] /10**6
                
                value=(new_poly_1_area * poly_1_value )/poly_1_area + (new_poly_1_area * poly_2_value )/poly_2_area
                geometry=NEW_POLY_1['geometry'].values[0]
                NEW_POLY_1['AREA'] =new_poly_1_area
                NEW_POLY_1['VALUE'] = value


                Result=Result.append({'geometry': geometry, 'VALUE': value}, ignore_index=True)
  
    gdf = gpd.GeoDataFrame(Result, geometry='geometry')
    gdf.to_file("D:/Документы/My/test/result.shp", driver="ESRI Shapefile")



zadanie1()
zadanie2()