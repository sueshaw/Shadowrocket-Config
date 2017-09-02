import base64
import datetime
import urllib.request
import os

class SRConfig:
    __DownloadFilePath = os.path.join("third_party",os.pardir)
    __GFWListRuleFileName = "gfw.txt"
    __BlockRuleFileName = "block.txt"
    __BaseRuleFileName = "baserule.txt"
    __RankRuleFileName = "rank.txt"
    __OutputRuleName = os.path.join("rule.txt",os.pardir)
    __OutputSimplifyRuleName = os.path.join("simplifyrule.txt",os.pardir)
    __OutputRuleWithAdBlockName = os.path.join("rulewithad.txt",os.pardir)

    __SimplifyLength = 2000

    __GFWListUrl = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
    __BlockRulesUrls = ["https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_thirdparty.txt",
                        "https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_adservers.txt"]

    __ProxyList = []
    __BlockList = []
    __SimplifyList = []

    def __init__(self):
        self.__downloadFile(self.__GFWListUrl, self.__DownloadFilePath + self.__GFWListRuleFileName)
        self.__downloadFiles(self.__BlockRulesUrls, self.__DownloadFilePath + self.__BlockRuleFileName)

    def getRules(self):

        baseRules = open(self.__DownloadFilePath + self.__BaseRuleFileName)
        proxyRules = self.__getProxyRules(self.__DownloadFilePath + self.__GFWListRuleFileName)
        blockRules = self.__getBlockRules(self.__DownloadFilePath + self.__BlockRuleFileName)
        simplfyRules = self.__getSimplifyRules(self.__DownloadFilePath + self.__RankRuleFileName)

        proxyFile = open(self.__OutputRuleName, 'w')
        proxyWithAdBlockFile = open(self.__OutputRuleWithAdBlockName, 'w')
        proxySimplifyFile = open(self.__OutputSimplifyRuleName, 'w')

        proxyFile.write("# Shadowrocket: " + str(datetime.datetime.now()) + "\n")
        proxyWithAdBlockFile.write("# Shadowrocket: " + str(datetime.datetime.now()) + "\n")
        proxySimplifyFile.write("# Shadowrocket: " + str(datetime.datetime.now()) + "\n")

        for line in baseRules:
            proxyFile.write(line)
            proxyWithAdBlockFile.write(line)
            proxySimplifyFile.write(line)

            if line == "[Rule]\n":
                proxyFile.write(proxyRules)
                proxyWithAdBlockFile.write(proxyRules)
                proxyWithAdBlockFile.write(blockRules)
                proxySimplifyFile.write(simplfyRules)

        proxyFile.close()
        proxyWithAdBlockFile.close()
        proxySimplifyFile.close()

    def __downloadFile(self, fileUrl, fileName):
        response = urllib.request.urlopen(fileUrl)
        data = response.read().decode('utf-8')
        oFile = open(fileName, 'w')
        oFile.write(data)
        oFile.close()

    def __downloadFiles(self, fileUrls, fileName):
        writeData = ""
        for url in fileUrls:
            response = urllib.request.urlopen(url)
            data = response.read().decode("utf-8")
            writeData += data + "\n"
        oFile = open(fileName, 'w')
        oFile.write(writeData)
        oFile.close()

    def __getProxyRules(self, fileName):
        proxyRules = ""
        base64file = open(fileName)
        pureRules = base64.b64decode(base64file.read()).decode('utf-8').split("\n")
        for rule in pureRules:
            newLine = self.__processProxyRule(rule)
            if newLine in self.__ProxyList:
                continue
            else:
                self.__ProxyList.append(newLine)
            if newLine != "":
                proxyRules += newLine + "\n"
        return proxyRules

    def __getSimplifyRules(self, fileName):
        simplifyRules = ""
        cnt = 0
        f = open(fileName).readlines()
        for line in f:
            domain = line.split(" ")[0]
            rank = line.split(" ")[1]
            if rank != '-1\n':
                rule = "DOMAIN-SUFFIX," + domain + ",Proxy"
                simplifyRules += rule + "\n"
                cnt = cnt + 1
                if cnt > self.__SimplifyLength:
                    return simplifyRules
        return simplifyRules

    def __processProxyRule(self, rule):
        if rule.startswith('!') or rule.startswith('[') or rule.startswith('@') or rule.startswith('/'):
            return ""
        elif rule.startswith('.'):
            rule = rule[1:]
        elif rule.startswith('||'):
            rule = rule[2:]
        elif rule.startswith('|https'):
            rule = rule[9:]
        elif rule.startswith('|http://'):
            rule = rule[8:]
        if rule.endswith('\n'):
            rule = rule[:-1]
        if "/" in rule:
            rule = rule[:rule.index("/")]
        if "*" in rule:
            rule = rule[rule.index("*") + 1:]
        if rule == "":
            return ""
        return "DOMAIN-SUFFIX," + rule + ",Proxy"

    def __getBlockRules(self, fileName):
        blockRules = ""
        orignRules = open(fileName)
        for rule in orignRules:
            newLine = self.__processBlockRule(rule)
            if newLine in self.__BlockList:
                continue
            else:
                self.__BlockList.append(newLine)
            if newLine != "":
                blockRules += newLine + "\n"
        return blockRules

    def __processBlockRule(self, rule):
        if rule.startswith('!') or rule.startswith('-'):
            return ""
        if "/" in rule:
            return ""
        if rule.startswith('||'):
            rule = rule[2:]
        if rule.endswith("\n"):
            rule = rule[:-1]
        if rule.endswith("^"):
            rule = rule[:rule.index("^")]
        if "^" in rule:
            if "third-party" in rule:
                rule = rule[:rule.index("^")]
            else:
                return ""
        if "$" in rule:
            rule = rule[:rule.index("$")]
        if "/" in rule:
            return ""
        return "DOMAIN-SUFFIX," + rule + ",REJECT"


if __name__ == "__main__":
    sConfig = SRConfig()
    sConfig.getRules()
