# Generated manually to add missing assistant_items_total field
# Made safe for fresh databases where field may already exist

from django.db import migrations, models, connection


def add_field_safe(apps, schema_editor):
    """Safely add assistant_items_total field if it doesn't exist"""
    Order = apps.get_model('orders', 'Order')
    table_name = Order._meta.db_table
    
    with connection.cursor() as cursor:
        # Check if column exists
        cursor.execute("""
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = %s AND column_name = %s
        """, [table_name, 'assistant_items_total'])
        
        if not cursor.fetchone():
            # Column doesn't exist, add it
            cursor.execute(f'''
                ALTER TABLE "{table_name}" 
                ADD COLUMN "assistant_items_total" NUMERIC(10, 2) NULL;
            ''')
            cursor.execute(f'''
                COMMENT ON COLUMN "{table_name}"."assistant_items_total" 
                IS 'Final items total from receipt, set by assistant';
            ''')


def reverse_add(apps, schema_editor):
    pass  # Cannot reverse safely


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0030_ensure_mpesa_columns_exist'),
    ]

    operations = [
        migrations.RunPython(add_field_safe, reverse_add),
    ]
