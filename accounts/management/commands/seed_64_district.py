import random
import string
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import District, Upazila, Voter, ElectionCommissionerProfile


# কতজন voter বানাবেন প্রতি জেলায়
VOTERS_PER_DISTRICT = 2  # change to 5/10/20 if you want

DISTRICT_NAMES = [
    "Dhaka","Chattogram","Rajshahi","Khulna","Barishal","Sylhet","Rangpur","Mymensingh",
    "Comilla","Noakhali","Feni","Brahmanbaria","Chandpur","Lakshmipur",
    "Cox's Bazar","Bandarban","Rangamati","Khagrachari",
    "Bogura","Joypurhat","Naogaon","Natore","Chapainawabganj","Pabna","Sirajganj",
    "Jessore","Jhenaidah","Magura","Narail","Kushtia","Chuadanga","Meherpur","Satkhira",
    "Bagerhat","Pirojpur","Jhalokathi","Bhola","Patuakhali","Barguna",
    "Sunamganj","Habiganj","Moulvibazar",
    "Dinajpur","Thakurgaon","Panchagarh","Nilphamari","Lalmonirhat","Gaibandha","Kurigram",
    "Sherpur","Jamalpur","Netrokona","Tangail","Gazipur","Narsingdi","Munshiganj",
    "Manikganj","Narayanganj","Faridpur","Gopalganj","Madaripur","Rajbari","Shariatpur"
]

FIRST_NAMES = ["Rahim","Karim","Hasan","Hossain","Sajid","Rafi","Nusrat","Ayesha","Sadia","Mim","Tania","Jannat"]
LAST_NAMES = ["Uddin","Islam","Ahmed","Khan","Akter","Begum","Rahman","Chowdhury","Sarker"]


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_nid(existing):
    while True:
        nid = "".join(random.choices(string.digits, k=10))
        if nid not in existing:
            existing.add(nid)
            return nid


def random_dob(min_age=18, max_age=70):
    today = date.today()
    days_ago = random.randint(min_age * 365, max_age * 365)
    return today - timedelta(days=days_ago)


class Command(BaseCommand):
    help = "Create 64 districts + default upazila + random-age voters"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true")
        parser.add_argument("--per_district", type=int, default=VOTERS_PER_DISTRICT)

    @transaction.atomic
    def handle(self, *args, **options):
        per_district = int(options["per_district"])

        if options["reset"]:
            self.stdout.write("Resetting old data...")
            # ✅ PROTECT fix: delete EC profiles first
            ElectionCommissionerProfile.objects.all().delete()
            Voter.objects.all().delete()
            Upazila.objects.all().delete()
            District.objects.all().delete()

        existing_nids = set(Voter.objects.values_list("nid", flat=True))

        created_voters = 0
        for dname in DISTRICT_NAMES:
            district, _ = District.objects.get_or_create(name=dname)

            upazila, _ = Upazila.objects.get_or_create(
                name=f"{dname} Sadar",
                district=district
            )

            for _ in range(per_district):
                Voter.objects.create(
                    nid=random_nid(existing_nids),
                    dob=random_dob(),  # ✅ random age
                    full_name=random_name(),
                    father_name=random_name(),
                    mother_name=random_name(),
                    gender=random.choice(["Male", "Female"]),
                    blood_group=random.choice(["A+", "B+", "O+", "AB+"]),
                    district=district,
                    upazila=upazila
                )
                created_voters += 1

        self.stdout.write(self.style.SUCCESS("✅ Done!"))
        self.stdout.write(f"Districts: {District.objects.count()}")
        self.stdout.write(f"Upazilas: {Upazila.objects.count()}")
        self.stdout.write(f"Voters created now: {created_voters}")
        self.stdout.write(f"Total voters: {Voter.objects.count()}")
