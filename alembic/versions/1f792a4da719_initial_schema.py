"""initial schema

Revision ID: 1f792a4da719
Revises: 
Create Date: 2021-06-17 23:18:27.402790

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '1f792a4da719'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'patient',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False)
    )

    op.create_table(
        'practitioner',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('npi', sa.String(), nullable=False)
    )

    op.create_table(
        'appointment',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('patient_id', sa.Integer, nullable=False),
        sa.Column('practitioner_id', sa.Integer, nullable=False),
        sa.Column('start_time', sa.DateTime, nullable=False),
        sa.Column('end_time', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
        sa.ForeignKeyConstraint(['practitioner_id'], ['practitioner.id'], ),
    )


def downgrade():
    op.drop_table('appointment')
    op.drop_table('patient')
    op.drop_table('practitioner')
