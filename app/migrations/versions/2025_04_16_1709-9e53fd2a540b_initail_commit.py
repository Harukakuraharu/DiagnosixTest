"""initail commit

Revision ID: 9e53fd2a540b
Revises: 
Create Date: 2025-04-16 17:09:03.550474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e53fd2a540b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
user_role = sa.Enum('PATIENT', 'DOCTOR', 'ADMIN', name='userrole')

def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=72), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('active', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('role', user_role, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    user_role.drop(op.get_bind())
    # ### end Alembic commands ###
