import urllib.request as ur

url='http://delivery.acm.org/10.1145/3100000/3098829/p85-Narayana.pdf?ip=125.220.159.2&id=3098829&acc=PUBLIC&key=BF85BBA5741FDC6E%2E4977B3C8BBB4AEC7%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35&__acm__=1527593519_2daa7ced3fff47900a0622d05a294e21'
# url2='http://kns.cnki.net/kns/download.aspx?filename=VYORHTaljMnRHV2J0N3RWcpBVZJ9kMrd1K6tSUxF0aqlkY1lDbLNzKxwWUkFENQRGTj9kMFNGOMdURrdkaLd3b=0TP3pnMSpUN2okWhlEVjRzT1EXORtyK34Wax90YktSTEp0Kr1GR5YFUlpHRvYEZUR2aqdjZFJFUXhFSmllVuZ&tablename=IPFDLAST2017&dflag=pdfdown'
file_name = "1234.pdf"
u = ur.urlopen(url)
f = open(file_name, 'wb')
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    f.write(buffer)
f.close()
print("Sucessful to download sig" + " " + file_name)
