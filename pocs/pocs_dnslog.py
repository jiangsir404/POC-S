#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Author: rivir
Date: 2020/2/29

DNSLog平台, 一个公网域名和ip即可搭建的简易快速DNSLog平台, 用于命令执行以及盲注的验证。
目前只能验证dns log, 无法验证web log,

Usage
    运行dnslog脚本: python pocs-dnslog.py
    获取dnslog命令: nslookup poc.xxxx.com 1.1.1.1  (xxxx.com是你的公网域名, 1.1.1.1是你的公网ip)
    通过api获取结果: curl "http://1.1.1.1:88/api/?token={token}&type={dns}&filter=xxxx.com
"""

import os, time
import copy
import click
import multiprocessing
import logging
import tempfile
import paste
import json
from dnslib import RR, QTYPE, RCODE, TXT
from dnslib.server import DNSServer, BaseResolver
from bottle import route,run,get,post,request, response

class JsonLogger(object):
    def __init__(self, domain, file):
        self.file = file
        self.domain = domain

    def log_data(self, dnsobj):
        pass

    def log_error(self, handler, e):
        pass

    def log_pass(self, *args):
        pass

    def log_prefix(self, handler):
        pass

    def log_recv(self, handler, data):
        pass

    def log_reply(self, handler, reply):
        pass

    def log_request(self, handler, request):
        """记录dns请求
        json格式:
            {
                "host":{
                    "type":"dns",
                    "dns_type": "A",
                    "time": ""
                }
            }
        """
        domain = request.q.qname.__str__().lower()
        if self.domain in domain:
            type = QTYPE[request.q.qtype]
            # 只记录A记录
            if type == "A":
                data = {
                    domain:
                        {
                            "type": "dns",
                            "dns_type": type,
                            "time": str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
                        }
                }
                # print("[DEBUG] %s %s", self.file, data)
                dnslog_content = {"dns": {}}
                try:
                    if os.path.exists(self.file):
                        with open(self.file) as f:
                            dnslog_content = json.load(f)
                    dnslog_content["dns"].update(data)
                    with open(self.file, 'w') as ff:
                        json.dump(dnslog_content, ff, indent=4)
                except Exception as e:
                    logging.error(e)

    def log_send(self, handler, data):
        pass

    def log_truncated(self, handler, reply):
        pass


class ZoneResolver(BaseResolver):
    """
        Simple fixed zone file resolver.
    """

    def __init__(self, zone, glob=False):
        """
            Initialise resolver from zone file.
            Stores RRs as a list of (label,type,rr) tuples
            If 'glob' is True use glob match against zone file
        """
        self.zone = [(rr.rname, QTYPE[rr.rtype], rr)
                     for rr in RR.fromZone(zone)]
        self.glob = glob
        self.eq = 'matchGlob' if glob else '__eq__'

    def resolve(self, request, handler):
        """
            Respond to DNS request - parameters are request packet & handler.
            Method is expected to return DNS response
        """
        reply = request.reply()
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        if qtype == 'TXT':
            txtpath = os.path.join(tempfile.gettempdir(), str(qname).lower())
            if os.path.isfile(txtpath):
                reply.add_answer(
                    RR(qname, QTYPE.TXT, rdata=TXT(open(txtpath).read().strip())))
        for name, rtype, rr in self.zone:
            # Check if label & type match
            if getattr(qname,
                       self.eq)(name) and (qtype == rtype or qtype == 'ANY'
                                           or rtype == 'CNAME'):
                # If we have a glob match fix reply label
                print("Request Record: %s %s" % (qtype, qname))
                if self.glob:
                    a = copy.copy(rr)
                    a.rname = qname
                    reply.add_answer(a)
                else:
                    reply.add_answer(rr)
                # Check for A/AAAA records associated with reply and
                # add in additional section
                if rtype in ['CNAME', 'NS', 'MX', 'PTR']:
                    for a_name, a_rtype, a_rr in self.zone:
                        if a_name == rr.rdata.label and a_rtype in [
                            'A', 'AAAA'
                        ]:
                            reply.add_ar(a_rr)
        if not reply.rr:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply


def run_dns_server(dnsdomain, outfile):
    """运行dns服务器, 监听53端口"""
    dnsdomain = dnsdomain
    ns1domain = "ns1." + dnsdomain
    ns2domain = "ns2." + dnsdomain
    serverip = "0.0.0.0"
    zone = '''
*.{dnsdomain}.       IN      NS      {ns1domain}.
*.{dnsdomain}.       IN      NS      {ns2domain}.
*.{dnsdomain}.       IN      A       {serverip}
{dnsdomain}.       IN      A       {serverip}
'''.format(
        dnsdomain=dnsdomain,
        ns1domain=ns1domain,
        ns2domain=ns2domain,
        serverip=serverip)
    resolver = ZoneResolver(zone, True)
    logger = JsonLogger(dnsdomain, outfile)
    print("Starting Zone Resolver (%s:%d) [%s] Dns Domain: %s" % ("*", 53, "UDP", dnsdomain))

    udp_server = DNSServer(resolver, port=53, address='', logger=logger)
    udp_server.start()

class DNSLogApi(object):
    """dnslog api接口, 获取dns请求数据"""
    api_key = ""
    file = "./dnslog.json"
    dnsdomain = ""

    @staticmethod
    @route("/weblog/<randomstr>")
    def weblog(randomstr="test"):
        """
        :param randomstr: 随机字符串
        :return:
                {
                "host2:{
                    "type": "web",
                    "remote_addr": "",
                    "user_agent": "",
                    "time": ""
                }
        """
        dnslog_content = {"web": {}}
        host = "http://" + request.headers.get('Host') + request.path
        if DNSLogApi.dnsdomain not in host:
            return "bad boy"
        http_user_agent = request.headers.get("User-Agent", None)
        remote_addr = request.headers.get('X_REAL_IP') or request.headers.get('REMOTE_ADDR')
        log_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        data = {
            host : {
                "type": "web",
                "user_agent": http_user_agent,
                "remote_addr": remote_addr,
                "time": str(log_time)
            }
        }

        try:
            if os.path.exists(DNSLogApi.file):
                with open(DNSLogApi.file) as f:
                    dnslog_content = json.load(f)
            dnslog_content["web"].update(data)
            with open(DNSLogApi.file, 'w') as ff:
                json.dump(dnslog_content, ff, indent=4)
        except Exception as e:
            logging.error(e)
        response.set_header('Content-Type', 'application/json')
        return json.dumps({"status": "success"})

    @staticmethod
    @route("/api/")
    def api():
        token = request.query.get("token", None)
        type = request.query.get("type", "dns")
        filter = request.query.get("filter", "")
        response.set_header('Content-Type', 'application/json')
        message = {"status": "fail", "data": {}}
        if token != DNSLogApi.api_key or type not in ["dns", "web"]:
            return json.dumps(message)
        data = {}

        try:
            with open(DNSLogApi.file) as f:
                dnslog_content = json.load(f)
            data = dnslog_content.get(type, {})
            if filter:
                if data.get(filter, {}):
                    data = {filter: data.get(filter, {})}
                else:
                    data = {}
        except Exception as e:
            logging.error(e)
        message["status"] = "success"
        message["data"] = data
        return json.dumps(message)

    @staticmethod
    @route("/sleep/<delay>")
    def sleep(delay=3):
        time.sleep(float(delay))
        return "time sleep %s" % delay

    @staticmethod
    def start(host, port):
        run(server='paste', host=host, port=port, debug=True)

@click.command()
@click.option('-h', '--host', default="127.0.0.1", help='host')
@click.option('-p', '--port', default=88, help="port")
@click.option('-o', '--output', default="./dnslog.json")
@click.option('--dns-domain', prompt="dns domain")
@click.option('--api-key', prompt="api key")
def main(host, port, output, dns_domain, api_key):
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("paste").setLevel(logging.WARNING)
    logging.debug("%s, %s, %s", api_key, dns_domain, output)
    p = multiprocessing.Process(target=run_dns_server, args=(dns_domain, output))
    p.daemon = True
    p.start()

    DNSLogApi.api_key = api_key
    DNSLogApi.file = output
    DNSLogApi.dnsdomain = dns_domain
    DNSLogApi().start(host, int(port))

if __name__ == "__main__":
    main()