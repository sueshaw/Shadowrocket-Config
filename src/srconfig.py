import base64
import datetime
import urllib.request


class SRConfig:
    __DownloadFilePath = "..\\third_party\\"
    __GFWListRuleFileName = "gfw.txt"
    __BlockRuleFileName = "block.txt"
    __BaseRuleFileName = "baserule.txt"
    __OutputRuleName = "..\\rule.txt"
    __OutputRuleWithAdBlockName = "..\\rulewithad.txt"

    __GFWListUrl = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
    __BlockRulesUrls = ["https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_thirdparty.txt",
                        "https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_adservers.txt"]

    __ProxyList = []
    __BlockList = []

    def __init__(self):
        self.__downloadFile(self.__GFWListUrl, self.__DownloadFilePath + self.__GFWListRuleFileName)
        self.__downloadFiles(self.__BlockRulesUrls, self.__DownloadFilePath + self.__BlockRuleFileName)

    def getRules(self):

        baseRules = open(self.__DownloadFilePath + self.__BaseRuleFileName)
        proxyRules = self.__getProxyRules(self.__DownloadFilePath + self.__GFWListRuleFileName)
        blockRules = self.__getBlockRules(self.__DownloadFilePath + self.__BlockRuleFileName)

        proxyFile = open(self.__OutputRuleName, 'w')
        proxyWithAdBlockFile = open(self.__OutputRuleWithAdBlockName, 'w')

        proxyFile.write("# Shadowrocket: " + str(datetime.datetime.now()) + "\n")
        proxyWithAdBlockFile.write("# Shadowrocket: " + str(datetime.datetime.now()) + "\n")
        for line in baseRules:
            proxyFile.write(line)
            proxyWithAdBlockFile.write(line)
            if line == "[Rule]\n":
                proxyFile.write(proxyRules)
                proxyWithAdBlockFile.write(proxyRules)
                proxyWithAdBlockFile.write(blockRules)
        proxyFile.close()
        proxyWithAdBlockFile.close()

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
