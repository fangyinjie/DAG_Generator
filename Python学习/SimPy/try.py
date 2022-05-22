import traceback

try:
    value = 8/0
    print(value)

except:     # 出错打印
    info = traceback.format_exc()
    print(info)
    print(type(info))
    print('error')
else:   # 不出错打印
    print('no error')

finally: #出不出错都打印
    print('-'*100)

