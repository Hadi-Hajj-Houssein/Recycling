import os
import sys
from sqlalchemy import create_engine, text
from alembic.config import Config
from alembic import command

# Your database URL
DATABASE_URL = "postgresql://postgres:123@localhost:5432/your_database"

def drop_alembic_version():
    """Drop the alembic_version table"""
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
        conn.commit()
    print("✅ Dropped alembic_version table")

def delete_migration_files():
    """Delete all migration files"""
    versions_dir = "alembic/versions"
    if os.path.exists(versions_dir):
        files = [f for f in os.listdir(versions_dir) if f.endswith(".py")]
        for file in files:
            os.remove(os.path.join(versions_dir, file))
        print(f"✅ Deleted {len(files)} migration files")
    else:
        print("⚠️  No versions directory found")

def generate_and_apply_migration():
    """Generate and apply new migration"""
    alembic_cfg = Config("alembic.ini")
    
    # Generate
    command.revision(alembic_cfg, autogenerate=True, message="initial migration")
    print("✅ Migration generated")
    
    # Apply
    command.upgrade(alembic_cfg, "head")
    print("✅ Migration applied")

def main():
    print("🔄 Resetting Alembic...\n")
    
    try:
        drop_alembic_version()
        delete_migration_files()
        generate_and_apply_migration()
        
        print("\n🎉 Success! Alembic has been reset.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nIf you get 'Can't locate revision', make sure:")
        print("1. The alembic_version table is dropped")
        print("2. All migration files are deleted")
        print("3. Your models are imported in env.py")

if __name__ == "__main__":
    main()