import uuid

import sqlalchemy

metadata = sqlalchemy.MetaData()

rides = sqlalchemy.Table(
    "rides",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.UUID(), primary_key=True, default=uuid.uuid4),
    sqlalchemy.Column("taxi_id", sqlalchemy.UUID(), nullable=False, default=uuid.uuid4),
    sqlalchemy.Column("user_id", sqlalchemy.UUID(), nullable=False, default=uuid.uuid4),
    sqlalchemy.Column("requested_at", sqlalchemy.DateTime(), nullable=True),
    sqlalchemy.Column("picked_up_at", sqlalchemy.DateTime(), nullable=True),
    sqlalchemy.Column("dropped_off_at", sqlalchemy.DateTime(), nullable=True),
    sqlalchemy.Column("pick_up_coordinates", sqlalchemy.JSON(), nullable=False),
    sqlalchemy.Column("drop_off_coordinates", sqlalchemy.JSON(), nullable=False),
)
