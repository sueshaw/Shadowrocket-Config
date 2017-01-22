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
    if rule.endswith('/'):
        rule=rule[:-1]
    if "/" in rule or rule=="":
        return ""
    return "DOMAIN-SUFFIX,"+rule+",Proxy"

def GetBlockRule1(rule):
    #rule=""
    if rule.startswith('!'):
        return ""
    elif rule.startswith('||'):
        rule=rule[2:]
    if rule.endswith('\n'):
        rule=rule[:-1]

    if ("$" in rule):
        rule = rule[:rule.index("$")]

    if(rule.endswith('*')):
        rule=rule[:-1]

    if ("$" in rule) or ("*" in rule) or("|" in rule):
        return ""
    return "DOMAIN-KEYWORD,"+rule+",REJECT"

def GetBlockRule2(rule):
    #rule=""
    if rule.startswith('!'):
        return ""
    elif rule.startswith('||'):
        rule=rule[2:]
    if rule.endswith('\n'):
        rule=rule[:-1]
    if ("$" in rule):
        rule = rule[:rule.index("$")]
    if (rule.endswith('*')):
        rule = rule[:-1]

    if ("$" in rule) or ("*" in rule) or("|" in rule):
        return rule+" reject"

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

def GetBlockRules(ruletype):
    Base64toPure()
    f=open("easylist_general_block.txt")
    ssRule=""
    for line in f:
        if ruletype==1:
            newline=GetBlockRule1(line)
        else:
            newline = GetBlockRule2(line)
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
            #w.write(GetProxyRules())
            w.write(GetBlockRules(1))
        if line=="[URL Rewrite]\n":
            w.write(GetBlockRules(2))
    f.close()
    w.close()

def Downloadlist():
    baseUrl=["https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt",
             "https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_general_block.txt"]
    fileName=["gfwbase64.txt",
              "easylist_general_block.txt"]
    for i in range(len(baseUrl)):
        response = urllib.request.urlopen(baseUrl[i])
        data = response.read()
        text = data.decode('utf-8')
        w=open(fileName[i],'w')
        w.write(text)
        w.close()


Downloadlist()
WriteRules()
