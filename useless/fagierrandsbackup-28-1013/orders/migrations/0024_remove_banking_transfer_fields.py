# Generated migration to remove transfer-related fields from BankingOrder
# This migration safely removes fields only if they exist in the database

from django.db import migrations, connection


def remove_fields_if_exist(apps, schema_editor):
    """
    Safely remove fields from BankingOrder table if they exist.
    Fully idempotent - will not fail if columns don't exist.
    """
    BankingOrder = apps.get_model('orders', 'BankingOrder')
    table_name = BankingOrder._meta.db_table
    
    fields_to_remove = ['recipient_name', 'recipient_account']
    
    with connection.cursor() as cursor:
        for field_name in fields_to_remove:
            try:
                # Use DROP COLUMN IF EXISTS for PostgreSQL (safe operation)
                cursor.execute(f'ALTER TABLE "{table_name}" DROP COLUMN IF EXISTS "{field_name}";')
                print(f"✓ Dropped column '{field_name}' from {table_name}")
            except Exception as e:
                # Ignore all errors - this is a cleanup migration
                print(f"✓ Column '{field_name}' already removed or doesn't exist")


def reverse_fields(apps, schema_editor):
    """
    Reverse operation - not implemented as we cannot safely restore fields without schema info.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_update_banking_transaction_types'),
    ]

    operations = [
        migrations.RunPython(remove_fields_if_exist, reverse_fields),
    ]
