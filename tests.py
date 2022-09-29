import requests
from treebuilder import TreeBuilder
import time

start = time.time()

markup = "" \
         "<!DOCTYPE html>" \
         "<html class=\"dd\" on_click=\"function fjjgl<slkn>sjjjdl =>\">" \
            "<head>" \
                "<meta>" \
                "<script>" \
                    "sggdh udh kkd c<b.hfjhfg b>0 hhhs <div>dhdhdhd</div>" \
                "</script>" \
                "<noscript>" \
                    "sggdh udh kkd c<b.hfjhfg b>0 hhhs <div>dhdhdhd</div>" \
                "</noscript>" \
                "<title>" \
                    "А я тайтл" \
                "</title>" \
            "</head>" \
            "<body>" \
                "<div id=\"div1\">" \
                    "Я внутри первого дива"\
                    "<br>" \
                    "<span>Я внутри спана</span>" \
                    "<p>" \
                        "<span id=\"div2\"> Лабдубай </span>" \
                    "</p>" \
                    "И я внутри дива" \
                "</div>" \
                "<footer class=\"footer\">" \
                "</footer>" \
            "</body>" \
         "</html>"

# with open("zagonka.txt", "r", encoding='utf-8') as zagonka:
#     m = zagonka.read()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
c = requests.get(url="https://mdn.github.io/web-components-examples/popup-info-box-web-component/", headers=headers).text

builder = TreeBuilder()

tree2 = builder.build_tree(markup=c)

finish = time.time()

print("Время выполнения скрипта: %.2f сек" % (finish-start))