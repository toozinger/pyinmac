"""
Create new machine tables in the IMT_machines DB on the OT2 server
"""

from pyinmac import connect_inmac_db, check_machine_table

#                                      XXX
db = connect_inmac_db('OT2', 'bhaley', '', db_name='IMT_machines')

new_machine_tables = [
    'homologationStreaming', 'homologationTest'
]
for t in new_machine_tables:
    _ = check_machine_table(db, t)
    print(t)
