"""
IN-MaC server info

Copyright (c) 2021 IN-MaC, Purdue University
Author: Benjamin P. Haley

LICENSE
"""

servers = {
    'dev': {
        'host': 'ldvinmac01.itap.purdue.edu',
        'ports': {
            'ptcm':    2112,
            'grafana': 3030,
            'mysql':   3317
        }
    },
    'prod': {
        'host': 'lpvinmac01.itap.purdue.edu',
        'ports': {
            'ptcm':    2112,
            'grafana': 3030,
            'mysql':   3317
        }
    },
    'OT2': {
        'host': 'ecn-inmactb2.ecn.purdue.edu',
        'ports': {
            'grafana': 3030,
            'mysql':   3317,
            'influx':  8086
        }
    }
}
