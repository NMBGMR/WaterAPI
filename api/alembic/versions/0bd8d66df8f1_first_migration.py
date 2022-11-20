"""first migration

Revision ID: 0bd8d66df8f1
Revises: 
Create Date: 2022-11-19 23:30:41.156054

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision = '0bd8d66df8f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('LU_DataSource',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('meaning', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_LU_DataSource_id'), 'LU_DataSource', ['id'], unique=False)
    op.create_table('LU_MeasurementMethod',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('meaning', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_LU_MeasurementMethod_id'), 'LU_MeasurementMethod', ['id'], unique=False)
    op.create_table('LU_Status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('meaning', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_LU_Status_id'), 'LU_Status', ['id'], unique=False)
    op.create_table('Location',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('point', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('point_id', sa.String(), nullable=True),
    sa.Column('elevation', sa.Float(), nullable=True),
    sa.Column('elevation_datum', sa.String(), nullable=True),
    sa.Column('public_release', sa.Boolean(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('county', sa.String(), nullable=True),
    sa.Column('quad', sa.String(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.Column('township', sa.Integer(), nullable=True),
    sa.Column('township_direction', sa.String(), nullable=True),
    sa.Column('range', sa.Integer(), nullable=True),
    sa.Column('range_direction', sa.String(), nullable=True),
    sa.Column('section', sa.Integer(), nullable=True),
    sa.Column('quarter', sa.Integer(), nullable=True),
    sa.Column('half_quarter', sa.Integer(), nullable=True),
    sa.Column('quarter_quarter', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # op.create_index('idx_Location_point', 'Location', ['point'], unique=False, postgresql_using='gist')
    op.create_index(op.f('ix_Location_id'), 'Location', ['id'], unique=False)
    op.create_table('ObservedProperty',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('units', sa.String(), nullable=True),
    sa.Column('definition', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ObservedProperty_id'), 'ObservedProperty', ['id'], unique=False)
    op.create_table('Project',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('point_id_prefix', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Project_id'), 'Project', ['id'], unique=False)
    op.create_table('QC',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('note', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_QC_id'), 'QC', ['id'], unique=False)
    op.create_table('Sensor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('install_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Sensor_id'), 'Sensor', ['id'], unique=False)
    op.create_table('ProjectLocation',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['Location.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['Project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ProjectLocation_id'), 'ProjectLocation', ['id'], unique=False)
    op.create_table('Well',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('public_release', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['Location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Well_id'), 'Well', ['id'], unique=False)
    op.create_table('WellConstruction',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('measuring_point_height', sa.Float(), nullable=True),
    sa.Column('casing_diameter', sa.Float(), nullable=True),
    sa.Column('hole_depth', sa.Float(), nullable=True),
    sa.Column('well_depth', sa.Float(), nullable=True),
    sa.Column('well_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['well_id'], ['Well.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_WellConstruction_id'), 'WellConstruction', ['id'], unique=False)
    op.create_table('WellMeasurement',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('well_id', sa.Integer(), nullable=True),
    sa.Column('method_id', sa.Integer(), nullable=True),
    sa.Column('observed_property_id', sa.Integer(), nullable=True),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.Column('note', sa.String(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('qc_id', sa.Integer(), nullable=True),
    sa.Column('public_release', sa.Boolean(), nullable=True),
    sa.Column('data_source_id', sa.Integer(), nullable=True),
    sa.Column('measuring_agency', sa.String(), nullable=True),
    sa.Column('measured_by', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['data_source_id'], ['LU_DataSource.id'], ),
    sa.ForeignKeyConstraint(['method_id'], ['LU_MeasurementMethod.id'], ),
    sa.ForeignKeyConstraint(['observed_property_id'], ['ObservedProperty.id'], ),
    sa.ForeignKeyConstraint(['qc_id'], ['QC.id'], ),
    sa.ForeignKeyConstraint(['sensor_id'], ['Sensor.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['LU_Status.id'], ),
    sa.ForeignKeyConstraint(['well_id'], ['Well.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_WellMeasurement_id'), 'WellMeasurement', ['id'], unique=False)
    op.create_table('ScreenInterval',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('top', sa.Float(), nullable=True),
    sa.Column('bottom', sa.Float(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('aquifer', sa.String(), nullable=True),
    sa.Column('well_construction_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['well_construction_id'], ['WellConstruction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ScreenInterval_id'), 'ScreenInterval', ['id'], unique=False)
    # op.drop_table('spatial_ref_sys')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('(srid > 0) AND (srid <= 998999)', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    op.drop_index(op.f('ix_ScreenInterval_id'), table_name='ScreenInterval')
    op.drop_table('ScreenInterval')
    op.drop_index(op.f('ix_WellMeasurement_id'), table_name='WellMeasurement')
    op.drop_table('WellMeasurement')
    op.drop_index(op.f('ix_WellConstruction_id'), table_name='WellConstruction')
    op.drop_table('WellConstruction')
    op.drop_index(op.f('ix_Well_id'), table_name='Well')
    op.drop_table('Well')
    op.drop_index(op.f('ix_ProjectLocation_id'), table_name='ProjectLocation')
    op.drop_table('ProjectLocation')
    op.drop_index(op.f('ix_Sensor_id'), table_name='Sensor')
    op.drop_table('Sensor')
    op.drop_index(op.f('ix_QC_id'), table_name='QC')
    op.drop_table('QC')
    op.drop_index(op.f('ix_Project_id'), table_name='Project')
    op.drop_table('Project')
    op.drop_index(op.f('ix_ObservedProperty_id'), table_name='ObservedProperty')
    op.drop_table('ObservedProperty')
    op.drop_index(op.f('ix_Location_id'), table_name='Location')
    op.drop_index('idx_Location_point', table_name='Location', postgresql_using='gist')
    op.drop_table('Location')
    op.drop_index(op.f('ix_LU_Status_id'), table_name='LU_Status')
    op.drop_table('LU_Status')
    op.drop_index(op.f('ix_LU_MeasurementMethod_id'), table_name='LU_MeasurementMethod')
    op.drop_table('LU_MeasurementMethod')
    op.drop_index(op.f('ix_LU_DataSource_id'), table_name='LU_DataSource')
    op.drop_table('LU_DataSource')
    # ### end Alembic commands ###
