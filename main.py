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

#Proxy Rules
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

#BlockRules

blockRule=[]
def GetBlockRule(rule):
    #rule=""
    if rule.startswith('!') or rule.startswith('-'):
        return ""
    if "/" in rule:
        return ""
    if rule.startswith('||'):
        rule=rule[2:]
    if rule.endswith("\n"):
        rule=rule[:-1]
    if rule.endswith("^"):
        rule = rule[:rule.index("^")]
    if "^" in rule:
        if "third-party" in rule:
            rule = rule[:rule.index("^")]
        else:
            return ""
    if "$" in rule:
        rule=rule[:rule.index("$")]
    if "/" in rule:
        return ""
    if rule in blockRule:
        return ""
    else:
        blockRule.append(rule)
        return "DOMAIN-SUFFIX," + rule + ",REJECT"

def GetBlockRules():
    ssRule = ""
    for i in range(1,3):
        f=open(fileName[i])
        for line in f:
            newline=GetBlockRule(line)
            if  newline!="":
                ssRule+=newline+"\n"
        f.close()
    return ssRule

def WriteRules():
    f=open("baserule.txt")
    w=open("rule.txt","w")
    wwithad=open("rulewithad.txt","w")
    toWrite=""
    w.write("# Shadowrocket: "+str(datetime.datetime.now())+"\n")
    for line in f:
        w.write(line)
        wwithad.write(line)
        if line=="[Rule]\n":
            proxyRules=GetProxyRules()
            blockRules=GetBlockRules()
            w.write(proxyRules)
            wwithad.write(proxyRules)
            wwithad.write(blockRules)
    f.close()
    w.close()
    wwithad.close()

baseUrl=["https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt",
         "https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_thirdparty.txt",
         "https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_adservers.txt"
        ]

fileName=["gfwbase64.txt",
          "easylist_thirdparty.txt",
          "easylist_adservers.txt"
         ]
def Downloadlist():
    for i in range(len(fileName)):
        response = urllib.request.urlopen(baseUrl[i])
        data = response.read()
        text = data.decode('utf-8')
        w=open(fileName[i],'w')
        w.write(text)
        w.close()


Downloadlist()
WriteRules()
