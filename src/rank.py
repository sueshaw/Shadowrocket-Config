#!/usr/bin/env python
# encoding: utf-8

import requests
import re
import base64
import time
import random
import os


class Rank:
    def __init__(self):
        sep = os.sep
        self.__session = requests.session()
        self.rank_path = '..' + sep + 'third_party' + sep + 'rank.txt'
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
        }
        self.rank_dict = {}
        self.main_rank_dict = {}
        self.__rules = []
        self.__read_rank()

    def get_rank(self, website):

        api_url = "http://www.alexa.com/siteinfo/" + website
        try:
            result = self.__session.get(api_url, headers=self.headers)
            rank = re.findall('"global":(\d+)}', result.content.decode("utf-8"))[0]
            return rank
        except Exception as ex:
            print(ex.args)
            print(website)
            time.sleep(random.randint(10, 20))
            return -1

    def get_gfw_webite(self):
        gfw_url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
        try:
            result = self.__session.get(gfw_url, headers=self.headers)
            rules = pureRules = base64.b64decode(result.content).decode('utf-8').split("\n")
            for rule in rules:
                host_url = self.__process_gfw_rule(rule)
                if host_url and host_url not in self.rank_dict and host_url not in self.__rules:
                    self.__rules.append(host_url)
            self.__rules = list(set(self.__rules))
        except Exception as ex:
            print(ex.args)

    def process(self):
        len_all = len(self.__rules)
        current = 0
        for rule in self.__rules:
            rank = self.get_rank(rule)
            self.__write_rank(rule, rank)
            current = current + 1
            print("%s %s %d/%d" % (rule, rank, current, len_all))

    def __process_gfw_rule(self, rule):
        if rule.startswith('!') or rule.startswith('[') or rule.startswith('@') or rule.startswith('/'):
            return False
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
        if rule.startswith('.'):
            rule = rule[1:]
        if re.findall("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", rule):
            return False
        if rule == "":
            return False
        return rule

    def __read_rank(self):
        f = open(self.rank_path)
        lines = f.readlines()
        for line in lines[:-1]:
            website, rank = line.replace("\n", "").split(" ")
            self.rank_dict[website] = rank
        f.close()

    def __write_rank(self, website, rank):
        if website not in self.rank_dict:
            f = open(self.rank_path, 'a')
            f.write("%s %s\n" % (website, rank))
            f.close()

    def sort(self):
        f = open(self.rank_path, 'w')
        new_dict = sorted(self.rank_dict.items(), key=lambda d: int(d[1]))
        for item in new_dict:
            f.write("%s %s\n" % (item[0], item[1]))
        f.close()
        print("ok")


if __name__ == "__main__":
    rk = Rank()
    # rn = rk.get_rank("baidu.com")
    # rk.get_gfw_webite()
    # rk.process()
    # rk.sort()
    # rk.clear_by_host()
    # rk.sort()
