#测试经纬度转地理信息

"""
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='myuseragent')
data = "{}, {}".format(str(80),str(120))
location = geolocator.reverse(data,zoom=18)
print(location)
"""

"""


import requests

# 执行一次高德地图地理逆编码的查询
# 输入值：coordList -> 经纬度的序列,currentKey -> 当前使用的Key
# 返回值：resultList -> 查询成功，返回结果地址的序列
#        -1 -> 执行当前查询时Key的配额用完了
#        -2 -> 执行当前查询出错
def ExcuteSingleQuery(coordList ,currentkey):
    # 1-将coordList中的经纬度坐标连接成高德地图API能够识别的样子
    coordString = ""     # 当前coordList组成的string
    for currentCoord in coordList:
        coordString += str(currentCoord[0]) + "," + str(currentCoord[1]) + '|'
    # 2-地理编码查询需要的Url
    output = 'json'    # 查询返回的形式
    batch = 'true'     # 是否支持多个查询
    base = 'https://restapi.amap.com/v3/geocode/regeo?'    # 逆地理编码查询Url的头
    currentUrl = base + "output=" + output + "&batch=" + batch + "&location=" + coordString+ "&key=" + currentkey
    # 3-提交请求
    response = requests.get(currentUrl)    # 提交请求
    answer = response.json()   # 接收返回
    # 4-解析Json的内容
    resultList = []    # 用来存放逆地理编码结果的空序列
    if answer['status'] == '1' and answer['info'] == 'OK':
        # 4.1-请求和返回都成功，则进行解析
        tmpList = answer['regeocodes']    # 获取所有结果坐标点
        for i in range(0,len(tmpList)):
            try:
                # 解析','分隔的经纬度
                addressString = tmpList[i]['formatted_address']
                # 放入结果序列
                resultList.append(addressString)
            except:
                # 如果发生错误则存入None
                resultList.append(None)
        return resultList
    elif answer['info'] == 'DAILY_QUERY_OVER_LIMIT':
        # 4.2-当前账号的余额用完了,返回-1
        return -1
    else:
        # 4.3-如果发生其他错误则返回-2
        return -2
    
if __name__ == '__main__':

    # 创建测试地址经纬度坐标集
    coordList = [
        "121.475538,31.228207",
        "121.479475,31.235831",
        "121.459444,31.233372",
        "121.50825,31.2296841",
        "121.518464,31.231464"
    ]

    # 进行地理编码
    print(ExcuteSingleQuery(coordList = coordList, currentkey="365ac412d6e22f49ce3d345270ecc643"))

"""


from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='8616535151561234')
location = geolocator.reverse("38.9122, 121.602")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)