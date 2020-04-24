import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import unidecode

url='https://www.sashares.co.za/jse-top-40/'

doc = lh.fromstring(requests.get(url).content)
tr = doc.xpath('//tr')

frame=[]
i=0
for t in tr[0]:
    i+=1
    col=t.text_content()
    frame.append((col,[]))

len(tr)

for j in range(1,len(tr)):
    T=tr[j]

    if len(T)!=4:
        break
    i=0

    for t in T.iterchildren():
        data=t.text_content()

        frame[i][1].append(data)
        i+=1

Dict={title:column for (title,column) in frame}
df=pd.DataFrame(Dict)
df = df.replace(r'View','https://www.profiledata.co.za/brokersites/SAShares/Summary.aspx?c=', regex=True)

df['URL'] = df['View']+df['JSE Code']
df=df.drop(['View'], axis=1)


FF = pd.DataFrame([])#empty table

for row in df['URL']:
    url=row
    page = requests.get(url)
    soup = BeautifulSoup(page.content,"html.parser")

    contentTable  = soup.find('table', { "class" : "TableData nolight"})
    df2 = pd.read_html(str(contentTable))[2]  #taking the 3rd "table"
    frame = df2.transpose()
    frame.columns = frame.iloc[0]
    frame=frame.iloc[pd.RangeIndex(len(frame)).drop(0)]
    frame['URL']=url
    FF= FF.append(frame)



#print(FF)
result = df.merge(FF,on='URL',how='left')
result= result[result['JSE Code'] != 'JSE Code']

result["Yesterday's Close"] = result["Yesterday's Close"].apply(unidecode.unidecode)
result["Today's Open"] = result["Today's Open"].apply(unidecode.unidecode)
result["Market Cap_x"] = result["Market Cap_x"].apply(unidecode.unidecode)
result["Volume"] = result["Volume"].apply(unidecode.unidecode)
result["P/E Ratio"] = result["P/E Ratio"].apply(unidecode.unidecode)
result["EPS"] = result["EPS"].apply(unidecode.unidecode)
#print(result)
#result.to_csv('result.csv', encoding="cp1252")
