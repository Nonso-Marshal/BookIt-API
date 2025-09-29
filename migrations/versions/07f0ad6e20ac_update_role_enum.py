from alembic import op

def upgrade():
    op.execute("ALTER TYPE role RENAME TO role_old")
    op.execute("CREATE TYPE role AS ENUM ('USER', 'ADMIN')")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE role USING (role::text::role)")
    op.execute("DROP TYPE role_old")

def downgrade():
    op.execute("ALTER TYPE role RENAME TO role_old")
    op.execute("CREATE TYPE role AS ENUM ('user', 'ADMIN')")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE role USING (role::text::role)")
    op.execute("DROP TYPE role_old")