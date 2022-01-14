from django.apps import apps
from django.conf import settings
from django.db import migrations


def get_user_model_table_name() -> str:
    app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    return apps.get_model(app_label, model_name)._meta.db_table


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunSQL(
            f"""
            CREATE FUNCTION application_user_id_to_db_username(p_application_user_id text)
            RETURNS text
            LANGUAGE sql
            IMMUTABLE
            RETURNS NULL ON NULL INPUT
            PARALLEL SAFE
            AS $$ SELECT CONCAT('user_', p_application_user_id); $$;
            
            COMMENT ON FUNCTION application_user_id_to_db_username IS
            'Find the DB user''s username corresponding to the application user with the given ID.';
            
            CREATE FUNCTION create_db_user_corresponding_to_application_user() RETURNS trigger AS
            $$BEGIN
            EXECUTE format('CREATE ROLE %I', application_user_id_to_db_username(NEW.id::text));
            END;$$
            LANGUAGE plpgsql
            SECURITY DEFINER
            SET search_path = public, pg_temp;
            
            CREATE TRIGGER create_db_user_corresponding_to_application_user
            AFTER INSERT ON {get_user_model_table_name()}
            FOR EACH ROW
            EXECUTE FUNCTION create_db_user_corresponding_to_application_user();
            
            CREATE FUNCTION drop_db_user_corresponding_to_application_user() RETURNS trigger AS
            $$BEGIN
            EXECUTE format('DROP ROLE IF EXISTS %I', application_user_id_to_db_username(OLD.id::text));
            END;$$
            LANGUAGE plpgsql
            SECURITY DEFINER
            SET search_path = public, pg_temp;
            
            CREATE TRIGGER drop_db_user_corresponding_to_application_user
            AFTER DELETE ON {get_user_model_table_name()}
            FOR EACH ROW
            EXECUTE FUNCTION drop_db_user_corresponding_to_application_user();
            """
        )
    ]
