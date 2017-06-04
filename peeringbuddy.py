#!/usr/bin/env python3
import requests
import pprint
import jinja2
import argparse

template = '''
protocols {
    bgp {
        {% for lan in lans %}
        group PEERSv6 {
            neighbor {{ lan.ipaddr6 }} {
                description "{{ net.name }} {{ lan.asn }} - {{ lan.name }}";
                remote-as {{ lan.asn }};
            }
        }
        group PEERSv4 {
            neighbor {{ lan.ipaddr4 }} {
                description "{{ net.name }} {{ lan.asn }} - {{ lan.name }}";
                remote-as {{ lan.asn }};
            }
        }
        {% endfor %}
    }
}
'''

def pdb_query_net(asn):
    r = requests.get(
        "https://www.peeringdb.com/api/net?asn={}&depth=2".format(asn))
    return r.json()['data'][0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--asn", type=int, required=True)
    parser.add_argument("--ixid", type=int, required=True)
    args = parser.parse_args()

    data = pdb_query_net(args.asn)

    lans = []
    for lan in data['netixlan_set']:
        if lan['ix_id'] == args.ixid:
            lans.append(lan)

    t = jinja2.Template(template)
    out = t.render(net=data, lans=lans)

    print(out)

if __name__ == "__main__":
    main()
