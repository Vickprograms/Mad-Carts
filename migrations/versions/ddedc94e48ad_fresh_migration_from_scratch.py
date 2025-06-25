"""Fresh migration from scratch

Revision ID: ddedc94e48ad
Revises: 
Create Date: 2025-06-24 23:46:19.315180
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ddedc94e48ad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ✅ Create carts table
    op.create_table('carts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # ✅ Create recent_searches
    op.create_table('recent_searches',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('search_term', sa.Text(), nullable=False),
        sa.Column('searched_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # ✅ Create recent_visits
    op.create_table('recent_visits',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('product_id', sa.UUID(), nullable=True),
        sa.Column('visited_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # ✅ Create cart_items
    op.create_table('cart_items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('cart_id', sa.UUID(), nullable=False),
        sa.Column('product_id', sa.UUID(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['cart_id'], ['carts.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # ✅ Create order_items
    op.create_table('order_items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('order_id', sa.UUID(), nullable=False),
        sa.Column('product_id', sa.UUID(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # 🚫 DO NOT DROP existing tables
    # op.drop_table('recentsearches')
    # op.drop_table('recentvisits')
    # op.drop_table('orderitems')

    # ✅ Update feedback table
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column('rating', existing_type=sa.INTEGER(), nullable=False)

    # ✅ Update orders table
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_amount', sa.Float(), nullable=False))
        batch_op.drop_constraint(batch_op.f('orders_user_id_fkey'), type_='foreignkey')
        #batch_op.drop_constraint(batch_op.f('orders_delivery_driver_id_fkey'), type_='foreignkey', if_exists=True)
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

        # 🚫 Only drop these columns if you're ABSOLUTELY SURE
        # batch_op.drop_column('delivery_driver_id')
        # batch_op.drop_column('condition')
        # batch_op.drop_column('pickup_location')
        # batch_op.drop_column('payment_method')
        # batch_op.drop_column('delivery_date')
        # batch_op.drop_column('received_at')


def downgrade():
    # 🔁 Reverse the upgrade (keep as is unless you’re customizing rollback)
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('total_amount')

    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column('rating', existing_type=sa.INTEGER(), nullable=True)

    op.drop_table('order_items')
    op.drop_table('cart_items')
    op.drop_table('recent_visits')
    op.drop_table('recent_searches')
    op.drop_table('carts')
