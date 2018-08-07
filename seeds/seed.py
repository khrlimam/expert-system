from seeds.Seeders import GejalaSeeder, PenyakitSeeder, DefaultUser

seeders = [PenyakitSeeder(), GejalaSeeder(), DefaultUser()]


def start():
    for seeder in seeders:
        seeder.run()
