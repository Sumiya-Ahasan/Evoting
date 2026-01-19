import random
import string
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import District, Upazila, Voter


FIRST_NAMES = [
    "Rahim", "Karim", "Hasan", "Hossain", "Sajid", "Rafi",
    "Nusrat", "Ayesha", "Sadia", "Jannat", "Mim", "Tania"
]

LAST_NAMES = [
    "Uddin", "Islam", "Ahmed", "Khan", "Chowdhury",
    "Sarker", "Miah", "Akter", "Begum", "Rahman"
]

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
GENDERS = ["Male", "Female"]


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_nid(existing):
    while True:
        nid = "".join(random.choices(string.digits, k=10))
        if nid not in existing:
            existing.add(nid)
            return nid


def random_dob():
    # age between 18 – 70
    return date.today() - timedelta(days=random.randint(18*365, 70*365))


class Command(BaseCommand):
    help = "Insert demo voters (100 / 200 / 500 etc)"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=100)
        parser.add_argument("--reset", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["count"]

        if options["reset"]:
            self.stdout.write("Deleting existing voters...")
            Voter.objects.all().delete()

        districts = list(District.objects.all())
        if not districts:
            self.stdout.write(self.style.ERROR("❌ No District found. Run seed_bd first."))
            return

        upazilas = list(Upazila.objects.select_related("district"))
        if not upazilas:
            self.stdout.write(self.style.ERROR("❌ No Upazila found. Run seed_bd first."))
            return

        existing_nids = set(Voter.objects.values_list("nid", flat=True))

        created = 0
        for _ in range(count):
            uz = random.choice(upazilas)

            Voter.objects.create(
                nid=random_nid(existing_nids),
                dob=random_dob(),
                full_name=random_name(),
                father_name=random_name(),
                mother_name=random_name(),
                gender=random.choice(GENDERS),
                blood_group=random.choice(BLOOD_GROUPS),
                district=uz.district,
                upazila=uz,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} voters inserted successfully!"))
