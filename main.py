import base64
def Base64toPure():
    base64file=open("gfwbase64.txt")
    pure=base64.b64decode(base64file.read()).decode('utf-8')
    base64file.close()
    pureFile=open("gfwpure.txt",'w')
    pureFile.write(pure)
    pureFile.close()

def getDomain(rule):
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

def getRules():
    f=open("gfwpure.txt")
    ssRule=""
    for line in f:
        newline=getDomain(line)
        if  newline!="":
            ssRule+=newline+"\n"
    f.close()
    return ssRule



#Base64toPure()

