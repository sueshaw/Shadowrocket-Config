# Shadowrocket Config

this project convert [GfwList](https://github.com/gfwlist/gfwlist) and 
~~[easylist_general_block](https://github.com/easylist/easylist) to Shadowrocket Config file~~

Shadowrocket does not support url regex and it will crash when the amount of  url rewrite rules too much
So it can not convert easylist to shadowrocket config.


## How to use

``` Python
python main.py 
```
to get lastest gfwlist config to ```rule.txt```

## Shadowrocket Config

Open Shadowrocket and add config file from 
 
url:  https://raw.githubusercontent.com/Hsiny/Shadowrocket-Config/master/rule.txt

or scan the QR code below

![QR code](qr.png)

## To do
>* ~~add ad block rules~~
>* ~~fix some regex rules in gfwlist~~
>* ~~add other easylist ad-block rulus~~
>* add some rules to block ads





