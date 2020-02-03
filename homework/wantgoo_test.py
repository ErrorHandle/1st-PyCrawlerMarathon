import requests
from bs4 import BeautifulSoup

url = 'https://m.wantgoo.com/stock/twstock/stat?type=increase'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
#     'Upgrade-Insecure-Requests': '1',
#     'Cookie': 'HWWAFSESID=209c3afa07a24a0345; HWWAFSESTIME=1578300387392; Hm_lvt_3c606e4c5bc6e9ff490f59ae4106beb4=1578300394; Hm_lpvt_3c606e4c5bc6e9ff490f59ae4106beb4=1578300394; _pk_testcookie..undefined=1; _pk_testcookie.2.57ea=1; _pk_ref.2.57ea=%5B%22%22%2C%22%22%2C1578300394%2C%22http%3A%2F%2Flocalhost%3A8888%2Fnotebooks%2FDesktop%2FPython%2FpyM%2FD18%2FDay018_HW.ipynb%22%5D; _pk_id.2.57ea=16652dd3088e3078.1578300394.1.1578300394.1578300394.; _pk_ses.2.57ea=1; _ga=GA1.2.1524276836.1578300394; _gid=GA1.2.1793773395.1578300394; aicoin_session=eyJpdiI6IklUVlwvSDhHXC84RmU3OVJ6SVBGd3VKQT09IiwidmFsdWUiOiJXZDZ1MjdwUHVXbmNaQzFRMzA3XC81eEdUVkJrcEJCOE9SamI5Umw2TCt0a05qanU1S0pjdUtVYjZOa1wvZFBaQWpcLzZZMEFkOGlUMVlQTldcL0pOb3pBZlE9PSIsIm1hYyI6IjcwMGNmODM3MWM4ODFlYzRiNThkOWE3MDBhMTgzY2FiMTM4YTJhYWE1YzZhZGJkNjEwMzJjMzIwOWYxZDQwNmYifQ%3D%3D',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
# }
headers = {
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://www.wantgoo.com/global/stockindex?StockNo=ln',
    'cookie': 'cf_clearance=6547777ef06d855ccdfeb4ff10d93b922f3d8d7b-1580715817-0-150; __cfduid=d1d20d94fd8a21d3e8342c453965870b31580715817; BID=76B35637-1443-4CD5-B22F-6EB51F713271; _ga=GA1.2.1506491883.1580715818; _gid=GA1.2.1588132232.1580715818; _fbp=fb.1.1580715818350.300524177; _hjid=86ba1e95-9f36-4166-aeaa-3010b9e84f45; BrowserMode=Web; _gat_gtag_UA_6993262_2=1; wcsid=OZ7LnSLweLzUZzfu3h7B70HW6AbB6oH3; hblid=E3XznMlyHFbg52Bc3h7B70HHWaBU6kjr; _okdetect=%7B%22token%22%3A%2215807206229770%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22www.wantgoo.com%22%7D; olfsk=olfsk020950027088451284; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1580720623872%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; _ok=8391-691-10-7433; _oklv=1580720651525%2COZ7LnSLweLzUZzfu3h7B70HW6AbB6oH3',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'accept': '*/*'
}
resp = requests.get(url, headers = headers)

html = BeautifulSoup(resp.text, "html.parser")
tbody = html.find('body').find('div', attrs = {'id': 'wrap'}).find('article').find('div', class_ = 'mTbBox fixTbScroll-h').find('tbody').find_all('tr')
print(tbody)
