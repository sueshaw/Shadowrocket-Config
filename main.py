import base64
import datetime
import urllib.request

def Base64toPure():
    base64file=open("gfwbase64.txt")
    pure=base64.b64decode(base64file.read()).decode('utf-8')
    base64file.close()
    pureFile=open("gfwpure.txt",'w')
    pureFile.write(pure)
    pureFile.close()

exitList=[]
def GetProxyRule(rule):
    #rule=""
    if rule.startswith('!') or rule.startswith('[') or rule.startswith('@') or rule.startswith('/'):
        return ""
    elif rule.startswith('.'):
        rule= rule[1:]
    elif rule.startswith('||'):
        rule= rule[2:]
    elif rule.startswith('|https'):
        rule= rule[9:]
    elif rule.startswith('|http://'):
        rule=rule[8:]
    if rule.endswith('\n'):
        rule=rule[:-1]
    if "/" in rule:
        rule=rule[:rule.index("/")]
    if "*" in rule:
        rule=rule[rule.index("*")+1:]
    if  rule=="":
        return ""
    if rule not in exitList:
        exitList.append(rule)
        return "DOMAIN-SUFFIX,"+rule+",Proxy"
    else:
        return ""


def GetProxyRules():
    Base64toPure()
    f=open("gfwpure.txt")
    ssRule=""
    for line in f:
        newline=GetProxyRule(line)
        if  newline!="":
            ssRule+=newline+"\n"
    f.close()
    return ssRule


def WriteRules():
    f=open("baserule.txt")
    w=open("rule.txt","w")
    toWrite=""
    w.write("# Shadowrocket: "+str(datetime.datetime.now())+"\n")
    for line in f:
        w.write(line)
        if line=="[Rule]\n":
            w.write(GetProxyRules())
    f.close()
    w.close()

def Downloadlist():
    baseUrl="https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"

    fileName="gfwbase64.txt"

    response = urllib.request.urlopen(baseUrl)
    data = response.read()
    text = data.decode('utf-8')
    w=open(fileName,'w')
    w.write(text)
    w.close()


Downloadlist()
WriteRules()
