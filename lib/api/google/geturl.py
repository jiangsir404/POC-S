#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

from googleapiclient.discovery import build
from lib.core.enums import PROXY_TYPE
from lib.utils.config import ConfigFileParser
from thirdparty.httplib2 import Http, ProxyInfo

d = {"kind": "customsearch#search", "url": {"type": "application/json",
                                            "template": "https://www.googleapis.com/customsearch/v1?q={searchTerms}&num={count?}&start={startIndex?}&lr={language?}&safe={safe?}&cx={cx?}&cref={cref?}&sort={sort?}&filter={filter?}&gl={gl?}&cr={cr?}&googlehost={googleHost?}&c2coff={disableCnTwTranslation?}&hq={hq?}&hl={hl?}&siteSearch={siteSearch?}&siteSearchFilter={siteSearchFilter?}&exactTerms={exactTerms?}&excludeTerms={excludeTerms?}&linkSite={linkSite?}&orTerms={orTerms?}&relatedSite={relatedSite?}&dateRestrict={dateRestrict?}&lowRange={lowRange?}&highRange={highRange?}&searchType={searchType}&fileType={fileType?}&rights={rights?}&imgSize={imgSize?}&imgType={imgType?}&imgColorType={imgColorType?}&imgDominantColor={imgDominantColor?}&alt=json"},
     "items": [{"kind": "customsearch#result", "title": "USPS.com\u00ae - USPS Package Intercept\u00ae",
                "displayLink": "impacttalks.org", "htmlTitle": "USPS.com\u00ae - USPS Package Intercept\u00ae",
                "formattedUrl": "impacttalks.org/006/?https://retail-pi.usps.com/.../index.action",
                "htmlFormattedUrl": "impacttalks.org/006/?https://retail-pi.usps.com/.../<b>index.action</b>",
                "pagemap": {"cse_thumbnail": [{"width": "151",
                                               "src": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTWX0fwjyp09Ui3JkSTjNP2h0jVuz9MjRW2UOpyIVEQk3tP_lCyPwy_jmU",
                                               "height": "192"}],
                            "cse_image": [{"src": "https://retail-pi.usps.com/media/images/rpi/rpi01.jpg"}]},
                "snippet": "Create a USPS.com account to... print shipping labels. request a Package Pickup\n. buy stamps and shop. manage PO Boxes. print customs forms online.",
                "htmlSnippet": "Create a USPS.com account to... print shipping labels. request a Package Pickup<br>\n. buy stamps and shop. manage PO Boxes. print customs forms online.",
                "link": "http://impacttalks.org/006/?https://retail-pi.usps.com/retailpi/actions/index.action",
                "cacheId": "hZieiG9kcxAJ"},
               {"kind": "customsearch#result", "title": "Course descriptions", "displayLink": "udapps.nss.udel.edu",
                "htmlTitle": "Course descriptions",
                "formattedUrl": "https://udapps.nss.udel.edu/CourseDesc/index.action",
                "htmlFormattedUrl": "https://udapps.nss.udel.edu/CourseDesc/<b>index.action</b>", "snippet": "",
                "htmlSnippet": "",
                "link": "https://udapps.nss.udel.edu/CourseDesc/index.action"},
               {"kind": "customsearch#result",
                "title": "WordPress \u203a Support \u00bb Notice: Undefined index: action in wp-db ...",
                "displayLink": "wordpress.org",
                "htmlTitle": "WordPress \u203a Support \u00bb Notice: Undefined index: action in wp-db ...",
                "formattedUrl": "https://wordpress.org/.../notice-undefined-index-action-in-wp-db-backupphp- on-line-222",
                "htmlFormattedUrl": "https://wordpress.org/.../notice-undefined-<b>index-action</b>-in-wp-db-backupphp- on-line-222",
                "pagemap": {
                    "metatags": [{"referrer": "always", "viewport": "width=device-width, initial-scale=1"}]},
                "snippet": "Hi there. I'm a fellow WP dev. While performing a standard debug session (\nWP_DEBUG set to true ) in one of the sites I contribute in, I saw the \naforementioned\u00a0...",
                "htmlSnippet": "Hi there. I&#39;m a fellow WP dev. While performing a standard debug session (<br>\nWP_DEBUG set to true ) in one of the sites I contribute in, I saw the <br>\naforementioned&nbsp;...",
                "link": "https://wordpress.org/support/topic/notice-undefined-index-action-in-wp-db-backupphp-on-line-222",
                "cacheId": "TK3lkryuptYJ"},
               {"kind": "customsearch#result", "title": "Oregon Business Registry", "displayLink": "sh.st",
                "htmlTitle": "Oregon Business Registry",
                "formattedUrl": "sh.st/st/ad9489ae6ba0b577f45f89f0283a185b/...or.../index.action",
                "htmlFormattedUrl": "sh.st/st/ad9489ae6ba0b577f45f89f0283a185b/...or.../<b>index.action</b>",
                "snippet": "Along with a new name, the new Oregon Business Registry has a new interface \nto make filing online easier. Additional future features to include; local\u00a0...",
                "htmlSnippet": "Along with a new name, the new Oregon Business Registry has a new interface <br>\nto make filing online easier. Additional future features to include; local&nbsp;...",
                "link": "http://sh.st/st/ad9489ae6ba0b577f45f89f0283a185b/https://secure.sos.state.or.us/cbrmanager/index.action",
                "cacheId": "9yj3f_gktioJ"}, {"kind": "customsearch#result",
                                             "title": "WordPress \u203a Support \u00bb PHP Notice: Undefined index: action",
                                             "displayLink": "wordpress.org",
                                             "htmlTitle": "WordPress \u203a Support \u00bb PHP Notice: Undefined index: action",
                                             "formattedUrl": "https://wordpress.org/support/.../php-notice-undefined-index-action",
                                             "htmlFormattedUrl": "https://wordpress.org/support/.../php-notice-undefined-<b>index-action</b>",
                                             "pagemap": {"metatags": [{"referrer": "always",
                                                                       "viewport": "width=device-width, initial-scale=1"}]},
                                             "snippet": "John -. I'll log another support thread to try to get the attention of the developer, \nbut you just need to add isset before it's used. FILE: wp-filemanager.php",
                                             "htmlSnippet": "John -. I&#39;ll log another support thread to try to get the attention of the developer, <br>\nbut you just need to add isset before it&#39;s used. FILE: wp-filemanager.php",
                                             "link": "https://wordpress.org/support/topic/php-notice-undefined-index-action",
                                             "cacheId": "u1yZ0g4MJ8sJ"}], "context": {"title": "cdxy-cse"},
     "queries": {"request": [
         {"count": 5, "outputEncoding": "utf8", "title": "Google Custom Search - inurl:index.action", "safe": "off",
          "searchTerms": "inurl:index.action", "startIndex": 1, "cx": "011385053819762433240:ljmmw2mhhau",
          "inputEncoding": "utf8", "totalResults": "19900"}], "nextPage": [
         {"count": 5, "outputEncoding": "utf8", "title": "Google Custom Search - inurl:index.action", "safe": "off",
          "searchTerms": "inurl:index.action", "startIndex": 6, "cx": "011385053819762433240:ljmmw2mhhau",
          "inputEncoding": "utf8", "totalResults": "19900"}]},
     "searchInformation": {"formattedSearchTime": "0.38", "formattedTotalResults": "19,900",
                           "totalResults": "19900", "searchTime": 0.383211}}


def _initHttpClient():
    http_client = Http()  # TODO
    proxy_str = ConfigFileParser().GoogleProxy().strip().split(' ')
    if len(proxy_str) != 3:
        raise  # TODO
    if proxy_str[0].lower() is 'http':
        type = PROXY_TYPE.HTTP
    elif proxy_str[0].lower() is 'sock5':
        type = PROXY_TYPE.SOCKS5
    elif proxy_str[0].lower() is 'sock4':
        type = PROXY_TYPE.SOCKS4
    else:
        raise  # TODO
    http_client = Http(proxy_info=ProxyInfo(type, proxy_str[1], int(proxy_str[2])))  # TODO
    return http_client


def googleSearch(query, limit=100):
    # service = build("customsearch", "v1",developerKey="[put your API key here]")
    service = build("customsearch", "v1", http=_initHttpClient(),
                    developerKey=ConfigFileParser().GoogleDeveloperKey())
    # result = service.cse().list(q=query, cx='[put your CSE key here]').execute()
    result = service.cse().list(q=query, cx=ConfigFileParser().GoogleEngine(), num=limit).execute()
    print result['searchInformation']['totalResults']
    ans = set()
    for url in result['items']:
        ans.add(url['link'])
        print url['link']
    return ans

# googleSearch('inurl:"/index.action"', 1)
