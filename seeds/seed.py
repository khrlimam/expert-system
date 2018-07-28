from seeds.Seeders import GejalaSeeder
from seeds.Seeders import PenyakitSeeder

seeders = [PenyakitSeeder(), GejalaSeeder()]


def start():
    for seeder in seeders:
        seeder.run()
