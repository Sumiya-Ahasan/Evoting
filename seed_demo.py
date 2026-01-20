import os
import django
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "election_portal.settings")
django.setup()

from django.contrib.auth.models import User
from accounts.models import District, Upazila, Voter, ElectionCommissionerProfile
from elections.models import Election, Symbol

def get_or_create_district(name):
    obj, _ = District.objects.get_or_create(name=name)
    return obj

def get_or_create_upazila(district, name):
    obj, _ = Upazila.objects.get_or_create(district=district, name=name)
    return obj

def create_voter(nid, dob, full_name, district, upazila, father="", mother="", gender="Male", blood="O+"):
    obj, created = Voter.objects.get_or_create(
        nid=nid,
        defaults={
            "dob": dob,
            "full_name": full_name,
            "father_name": father,
            "mother_name": mother,
            "gender": gender,
            "blood_group": blood,
            "district": district,
            "upazila": upazila,
        }
    )
    if not created:
        # update basic fields if already exists
        obj.dob = dob
        obj.full_name = full_name
        obj.father_name = father
        obj.mother_name = mother
        obj.gender = gender
        obj.blood_group = blood
        obj.district = district
        obj.upazila = upazila
        obj.save()
    return obj

def create_symbols(symbol_names):
    for s in symbol_names:
        Symbol.objects.get_or_create(name=s)

def ensure_active_election():
    e, _ = Election.objects.get_or_create(name="General Election 2026", defaults={"is_active": True})
    # optional: make only this active
    Election.objects.exclude(id=e.id).update(is_active=False)
    e.is_active = True
    e.save()
    return e

def create_ec_user(username, password, district):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.is_staff = True  # admin panel access if needed
        user.save()
    else:
        # keep password unchanged if already exists
        pass

    ElectionCommissionerProfile.objects.get_or_create(user=user, defaults={"district": district})
    # if existed but district changed, update
    profile = ElectionCommissionerProfile.objects.get(user=user)
    profile.district = district
    profile.save()

def run():
    print("=== Seeding demo data... ===")

    # Districts
    dhaka = get_or_create_district("Dhaka")
    chattogram = get_or_create_district("Chattogram")

    # Upazilas
    dhaka_savar = get_or_create_upazila(dhaka, "Savar")
    dhaka_dhanmondi = get_or_create_upazila(dhaka, "Dhanmondi")

    ctg_pahartoli = get_or_create_upazila(chattogram, "Pahartoli")
    ctg_panchlaish = get_or_create_upazila(chattogram, "Panchlaish")

    # Voters (Demo)
    create_voter(
        nid="1234567890",
        dob=date(2001, 1, 10),
        full_name="Rahim Uddin",
        district=dhaka,
        upazila=dhaka_savar,
        father="Karim Uddin",
        mother="Rokeya Begum",
        gender="Male",
        blood="A+",
    )
    create_voter(
        nid="2234567890",
        dob=date(2002, 2, 20),
        full_name="Karima Akter",
        district=dhaka,
        upazila=dhaka_dhanmondi,
        father="Jamal Hossain",
        mother="Shirin Akter",
        gender="Female",
        blood="B+",
    )
    create_voter(
        nid="3234567890",
        dob=date(2000, 5, 5),
        full_name="Sajid Hasan",
        district=chattogram,
        upazila=ctg_pahartoli,
        father="Abdul Hasan",
        mother="Selina Hasan",
        gender="Male",
        blood="O+",
    )
    create_voter(
        nid="4234567890",
        dob=date(1999, 12, 12),
        full_name="Nusrat Jahan",
        district=chattogram,
        upazila=ctg_panchlaish,
        father="Mizanur Rahman",
        mother="Nasima Rahman",
        gender="Female",
        blood="AB+",
    )

    # Symbols
    create_symbols(["Boat", "Eagle", "Tiger", "Plough", "Sun", "Star"])

    # Election
    ensure_active_election()

    # Zilla EC Users (Demo)
    create_ec_user("ec_dhaka", "12345", dhaka)
    create_ec_user("ec_ctg", "12345", chattogram)

    print("✅ Done!")
    print("Demo voters created with NID/DOB:")
    print(" - Rahim Uddin: 1234567890 / 2001-01-10")
    print(" - Karima Akter: 2234567890 / 2002-02-20")
    print(" - Sajid Hasan: 3234567890 / 2000-05-05")
    print(" - Nusrat Jahan: 4234567890 / 1999-12-12")
    print("\nDemo EC logins:")
    print(" - Dhaka EC: username=ec_dhaka password=12345")
    print(" - Ctg EC: username=ec_ctg password=12345")

if __name__ == "__main__":
    run()
