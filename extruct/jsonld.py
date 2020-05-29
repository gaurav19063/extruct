# -*- coding: utf-8 -*-
"""
JSON-LD extractor
"""

import json
import re
import string
import lxml.etree

from extruct.utils import parse_html

HTML_OR_JS_COMMENTLINE = re.compile(r'^\s*(//.*|<!--.*-->)')
def debugg_json(jsonld):

    # print(jsonld)
    count1=jsonld.count('{')
    count2 = jsonld.count('}')
    st_t="{"
    st_p="}"
    if(count1==0):
        jsonld=st_t*count2+jsonld
    elif(count2==0):
        jsonld=jsonld+st_p*count1


    if(count1<count2):
        jsonld=jsonld[:-1]
    elif(count1>count2):
        jsonld = jsonld[1:]
    return jsonld

def validate_json(jsonld):
    i = 0
    jsonld = jsonld.translate({ord(c): None for c in (string.whitespace)})
    while 1:
        try:
            y = json.loads(jsonld)

            # print("Json is valid")
            # print(y)
            break
        except:
            jsonld_list = list(jsonld)
            for k in range(len(jsonld_list) - 1):
                if (jsonld_list[k] == '{' and jsonld_list[k + 1] == '{'):
                    jsonld_list[k + 1] = ""
            jsonld = "".join(jsonld_list)
            # print(jsonld)

            jsonld = debugg_json(jsonld)
            i += 1
            if (i == 10):
                # print("Invalid json ")
                break
            # print(".",end="")
            continue
    return jsonld






class JsonLdExtractor(object):
    _xp_jsonld = lxml.etree.XPath('descendant-or-self::script[@type="application/ld+json"]')
    # print(str(object))

    def extract(self, htmlstring, base_url=None, encoding="UTF-8"):
        # print(htmlstring)
        tree = parse_html(htmlstring, encoding=encoding)

        return self.extract_items(tree, base_url=base_url)


    def extract_items(self, document, base_url=None):
        return [
            item
            for items in map(self._extract_items, self._xp_jsonld(document))
            if items for item in items if item
        ]

    def _extract_items(self, node):
        script = node.xpath('string()')
        try:
            # TODO: `strict=False` can be configurable if needed
            script='{{'+str(script)+'}}}'
            # script=str(script)[:-1]
            # print(script)
            data = json.loads(script, strict=False)


            # print(data)
            #
            # print(str(script))
            #
            # print(type(str(script)))
        except ValueError:
            # print("here")
            script=validate_json(str(script))
            script=str(script)
            # print(script)
            # sometimes JSON-decoding errors are due to leading HTML or JavaScript comments
            data = json.loads(
                HTML_OR_JS_COMMENTLINE.sub('', script), strict=False)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
