# Generated by Django 3.0.2 on 2020-03-21 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking_portal', '0002_aas_bet_rheometer_tga'),
    ]

    operations = [
        migrations.CreateModel(
            name='CDSpectrophotometer',
            fields=[
                ('userdetails_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='booking_portal.UserDetails')),
                ('sample_code', models.CharField(max_length=75)),
                ('wavelength_scan_start', models.CharField(max_length=75)),
                ('wavelength_scan_end', models.CharField(max_length=75)),
                ('wavelength_fixed', models.CharField(max_length=75)),
                ('temp_range_scan_start', models.CharField(max_length=75)),
                ('temp_range_scan_end', models.CharField(max_length=75)),
                ('temp_range_fixed', models.CharField(max_length=75)),
                ('concentration', models.CharField(max_length=75)),
                ('cell_path_length', models.CharField(max_length=75)),
            ],
            bases=('booking_portal.userdetails',),
        ),
        migrations.CreateModel(
            name='DSC',
            fields=[
                ('userdetails_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='booking_portal.UserDetails')),
                ('sample_code', models.CharField(max_length=75)),
                ('chemical_composition', models.CharField(max_length=75)),
                ('sample_amount', models.CharField(max_length=75)),
                ('heating_program', models.CharField(choices=[('Dynamic', 'Dynamic'), ('Isothermal', 'Isothermal')], max_length=15)),
                ('temp_range', models.CharField(max_length=75)),
                ('atmosphere', models.CharField(choices=[('N2', 'N2'), ('Ar', 'Ar'), ('Air', 'Air')], max_length=5)),
                ('heating_rate', models.CharField(max_length=75)),
            ],
            bases=('booking_portal.userdetails',),
        ),
        migrations.CreateModel(
            name='GC',
            fields=[
                ('userdetails_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='booking_portal.UserDetails')),
                ('sample_code', models.CharField(max_length=75)),
                ('appearance', models.CharField(max_length=75)),
                ('no_of_gc_peaks', models.IntegerField()),
                ('solvent_solubility', models.CharField(max_length=75)),
                ('column_details', models.CharField(max_length=75)),
                ('exp_mol_wt', models.CharField(max_length=75)),
                ('mp_bp', models.CharField(max_length=75)),
                ('sample_source', models.CharField(choices=[('Natural', 'Natural'), ('Synthesis', 'Synthesis'), ('Waste', 'Waste')], max_length=15)),
            ],
            bases=('booking_portal.userdetails',),
        ),
        migrations.CreateModel(
            name='LSCM',
            fields=[
                ('userdetails_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='booking_portal.UserDetails')),
                ('sample_description', models.CharField(max_length=75)),
                ('dye', models.CharField(max_length=75)),
                ('excitation_wavelength', models.CharField(max_length=75)),
                ('emission_range', models.CharField(max_length=75)),
                ('analysis_details', models.CharField(max_length=75)),
            ],
            bases=('booking_portal.userdetails',),
        ),
    ]