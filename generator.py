import json
from lxml import etree
import os

with open('ans.txt','rb') as f:
    ans = json.load(f)

def checkNotChoice(s,c):
    return not s.capitalize().startswith(c)

def extractor(page):
    with open(page,'rb') as f:
        html = etree.HTML(f.read())
        html_question = html.xpath("//div[@class='questionArea']/span[1]/table/tbody/tr/td[2]/div")

        for q in html_question:
            question = filter(lambda x: checkNotChoice(x,'A') and checkNotChoice(x,'B') and checkNotChoice(x,'C') and checkNotChoice(x,'D')
                          and len(x)>5, [i.xpath('string(.)').strip() for i in q.xpath(".//p")])
            yield ''.join(question)

def generator(page='paper.html'):
    global ans
    n=0
    for i in extractor(page):
        if n%5 == 0:
            print 
            print '%d-%d'%(n+1,n+5),
        n+=1
        if ans.has_key(i):
            print ans[i][1],
        else:
            print '?',

def render(s, c):
    pos = [s.find(p) for p in list('ABCD')]
    pos.append(len(s))
    pp = []
    for i in range(len(pos)-1):
        pp.append((pos[i],pos[pos.index(pos[i])+1]))
    choice = [s.find(p) for p in list(c)]
    cc = []
    for i in choice:
        cc.append((i,pos[pos.index(i)+1]))

    kk=''
    for x,y in pp:
        #s=s[0:x]+'<font color="red">'+s[x:y]+'</font>'+s[y:]
        #s=s[0:x]+'@@@'+s[x+1:y]+'@@@'+s[y:]
        if (x,y) in cc:
            kk+='<font color="red">'
            kk+=s[x:y]
            kk+='</font>'
        else:
            kk+=s[x:y]
    #print s
    return kk
        

def generate_html(page='paper.html'):
    global ans
    with open('aaaaaaa.html','wb') as f:
        f.write('<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body><table border="1"><tr><th>No.</th><th>Question</th></tr>')
        #f.write('<tr><td><font color="red">%s</font></td><td>%s</td></tr>'%(row[0].encode('utf-8'),row[1].encode('utf-8')))
        n=1
        for i in extractor(page):
            if ans.has_key(i):
                f.write('<tr><td>%d<br><strong>%s</strong></td><td>%s<br>%s</td></tr>'%(n,ans[i][1].encode('utf-8'),i.encode('utf-8'),render(ans[i][0],ans[i][1]).encode('utf-8')))
            else:
                pass
            n+=1
        f.write('</table></body></html>')
   
if __name__ == '__main__':
    generate_html("paper.html")
    generator('paper.html')
    os.system("pause")
