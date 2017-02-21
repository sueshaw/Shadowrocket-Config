# Shadowrocket Config

this project converts [GfwList](https://github.com/gfwlist/gfwlist) to a Shadowrocket config to break the GFW  and
convert [easylist_adservers](https://github.com/easylist/easylist/blob/master/easylist/easylist_adservers.txt),
[easylist_thirdparty](https://github.com/easylist/easylist/blob/master/easylist/easylist_thirdparty.txt) to Shadowrocket config to lock ads

>* Convert gfwlist rules to ```DOMAIN-SUFFIX,rule,Proxy```
>* Convert easylist rules to ```DOMAIN-SUFFIX,rule,REJECT```

## How to use

``` Python
python main.py 
```
to get lastest gfwlist config to ```rule.txt``` and ```rulewithad.txt```

## Shadowrocket Config only Wall-break

Open Shadowrocket and add config file from 
 
url:  https://raw.githubusercontent.com/Hsiny/Shadowrocket-Config/master/rule.txt

or scan the QR code below

![QR code](proxy.png)

## Shadowrocket Config Wall-break and Ad-block

Open Shadowrocket and add config file from 
 
url:  https://raw.githubusercontent.com/Hsiny/Shadowrocket-Config/master/rulewithad.txt

or scan the QR code below

![QR code](proxyandadblock.png)


## To do
>* ~~add ad block rules~~
>* ~~fix some regex rules in gfwlist~~
>* ~~add other easylist ad-block rulus~~
>* ~~add some rules to block ads~~
>* reduce the number of ad-block rules





