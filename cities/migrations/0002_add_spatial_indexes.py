from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('cities', '0001_initial'),
    ]
   
    operations = [
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS cities_spatialcity_location_gist_idx ON cities_spatialcity USING GIST (location);",
            reverse_sql="DROP INDEX IF EXISTS cities_spatialcity_location_gist_idx;"
        ),
    ]


