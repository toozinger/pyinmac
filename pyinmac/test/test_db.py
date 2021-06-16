"""
IN-MaC Database tests

Copyright (c) 2021 IN-MaC, Purdue University
Author: Benjamin P. Haley

LICENSE
"""

from unittest import TestCase
from datetime import datetime
from pyinmac import connect_inmac_db, check_machine_table, get_time, add_data, \
                    get_data

class TestDB(TestCase):

    def test_db(self):
        server = 'OT2'  # 'private'
        db = connect_inmac_db(server, 'test_user', 't35tP455', 
                              db_name='test_db')
        mach = 'test_machine'
        ret = check_machine_table(db, mach)
        self.assertEqual(True, ret)
        dt = get_time()  # string
        add_data(db, mach, dt, 1.1, 'MetricA')
        add_data(db, mach, dt, 1.2, 'MetricB')
        add_data(db, mach, dt, 1.3, 'MetricB')
        add_data(db, mach, dt, 1.4, 'MetricA')
        t,x = get_data(db, mach, 'MetricA')
        ts = datetime.fromisoformat(dt)
        self.assertEqual(t, [ts,ts])
        self.assertEqual(x, ['1.1', '1.4'])
        t,y = get_data(db, mach, 'MetricB')
        self.assertEqual(t, [ts,ts])
        self.assertEqual(y, ['1.2', '1.3'])
        t,z = get_data(db, mach, 'MetricB', where='Value > 1.21')
        self.assertEqual(t, [ts])
        self.assertEqual(z, ['1.3'])

        db.cursor().execute('drop table '+mach)
        db.commit()
        db.close()
