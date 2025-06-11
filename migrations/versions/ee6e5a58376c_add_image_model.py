"""add image model

Revision ID: ee6e5a58376c
Revises: bcf23d13e2e7
Create Date: 2024-03-14 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'ee6e5a58376c'
down_revision = 'bcf23d13e2e7'
branch_labels = None
depends_on = None

def upgrade():
    # Create image table
    op.create_table('image',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Migrate existing image_urls to Image records
    connection = op.get_bind()
    
    # Get all posts with image_urls
    posts = connection.execute(
        sa.text("SELECT id, image_urls FROM post WHERE image_urls IS NOT NULL AND image_urls != '[]'::jsonb")
    ).fetchall()
    
    # For each post, create Image records
    for post in posts:
        post_id = post[0]
        image_urls = post[1]
        
        if image_urls:
            for url in image_urls:
                connection.execute(
                    sa.text("""
                        INSERT INTO image (url, created_at, post_id)
                        VALUES (:url, :created_at, :post_id)
                    """),
                    {
                        'url': url,
                        'created_at': datetime.utcnow(),
                        'post_id': post_id
                    }
                )
    
    # Remove the image_urls column
    op.drop_column('post', 'image_urls')

def downgrade():
    # Add back the image_urls column
    op.add_column('post', sa.Column('image_urls', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    
    # Migrate Image records back to image_urls array
    connection = op.get_bind()
    
    # Get all posts with images
    posts = connection.execute(
        sa.text("SELECT DISTINCT post_id FROM image")
    ).fetchall()
    
    # For each post, collect image URLs
    for post in posts:
        post_id = post[0]
        images = connection.execute(
            sa.text("SELECT url FROM image WHERE post_id = :post_id ORDER BY created_at"),
            {'post_id': post_id}
        ).fetchall()
        
        image_urls = [img[0] for img in images]
        
        # Update post with image_urls array
        connection.execute(
            sa.text("UPDATE post SET image_urls = :image_urls WHERE id = :post_id"),
            {
                'image_urls': image_urls,
                'post_id': post_id
            }
        )
    
    # Drop the image table
    op.drop_table('image')
