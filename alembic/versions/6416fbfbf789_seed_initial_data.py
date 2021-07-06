"""seed initial data

Revision ID: 6416fbfbf789
Revises: 1f792a4da719
Create Date: 2021-06-18 11:47:09.662723

"""
import datetime

from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy import table, column, Integer, String, DateTime

revision = '6416fbfbf789'
down_revision = '1f792a4da719'
branch_labels = None
depends_on = None


def upgrade():
    patient_table = table('patient',
                          column('id', Integer),
                          column('first_name', String),
                          column('last_name', String)
                          )

    practitioner_table = table('practitioner',
                               column('id', Integer),
                               column('first_name', String),
                               column('last_name', String),
                               column('npi', String),
                               )

    appointment_table = table('appointment',
                              column('id', Integer),
                              column('patient_id', Integer),
                              column('practitioner_id', Integer),
                              column('start_time', DateTime),
                              column('end_time', DateTime)
                              )

    op.bulk_insert(patient_table,
                   [
                       {'id': 1, 'first_name': 'Alexei', 'last_name': 'Isac'},
                       {'id': 2, 'first_name': 'Mathew', 'last_name': 'Isac'},
                   ]
                   )

    op.bulk_insert(practitioner_table,
                   [
                       {'id': 1, 'first_name': 'Bob', 'last_name': 'Dr', 'npi':'100'},
                       {'id': 2, 'first_name': 'Alice', 'last_name': 'Dr', 'npi':'200'},
                   ]
                   )

    op.bulk_insert(appointment_table,
                   [
                       {
                           'id': 1,
                           'patient_id': 1,
                           'practitioner_id': 1,
                           'start_time': datetime.datetime(year=2021, month=1, day=1, hour=0, minute=0, second=0),
                           'end_time': datetime.datetime(year=2021, month=1, day=1, hour=0, minute=30, second=0)
                       },
                       {
                           'id': 2,
                           'patient_id': 1,
                           'practitioner_id': 2,
                           'start_time': datetime.datetime(year=2021, month=2, day=1, hour=0, minute=0, second=0),
                           'end_time': datetime.datetime(year=2021, month=2, day=1, hour=0, minute=30, second=0)
                       }
                   ]
                   )

def downgrade():
    op.execute('delete from appointment')
    op.execute('delete from patient')
    op.execute('delete from practitioner')
