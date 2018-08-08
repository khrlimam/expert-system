from seeds.Seeders import GejalaSeeder, PenyakitSeeder, DefaultUser, RuleModelSeeder

seeders = [PenyakitSeeder(), GejalaSeeder(), DefaultUser(), RuleModelSeeder()]


def start():
    for seeder in seeders:
        seeder.run()
