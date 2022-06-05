"""Create Borrow_log table

Revision ID: a0773d7859ab
Revises: 5669f7207245
Create Date: 2022-06-05 13:18:17.122135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0773d7859ab'
down_revision = '5669f7207245'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Book', sa.Column('isbn', sa.String(length=20), nullable=True))
    op.drop_column('Borrow_log', 'qty')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Borrow_log', sa.Column('qty', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('Book', 'isbn')
    # ### end Alembic commands ###
