from faker import Faker
import datetime
import random
import argparse
import pycountry
from mongoengine import connect
from api.models import Attack, Location

fake = Faker()

def mongoengine_connection():
    connect('attack_data', host='mongodb://localhost:27017')

def generate_random_location():
    """
    Create a random location using realistic latitude, longitude, and country.
    """
    top_30_country_codes = ["US", "CN", "IN", "JP", "DE", "GB", "FR", "BR", "IT", "CA", "KR", "RU", "AU", "ES", "MX", "ID",
                           "NL", "SA", "TR", "CH", "AR", "SE", "NG", "PL", "BE", "TH", "EG", "PK", "BD", "VN"]
    country_code = random.choice(top_30_country_codes)
    try:
        coords = fake.local_latlng(country_code)
        country = pycountry.countries.get(alpha_2=country_code.upper())
        if not coords or not country:
            raise ValueError("Invalid coordinates or country")
        return {"latitude":float(coords[0]),"longitude": float(coords[1]), "country": country.name}
    except (AttributeError, ValueError):
        # Fallback to random coordinates if Faker fails
        return {"latitude":random.uniform(-90, 90),"longitude": random.uniform(-180, 180),"country":  pycountry.countries.get(alpha_2=country_code.upper()).name}
    
def generate_random_attack():
    """
    Generate an Attack document with random values.
    """
    
    source = generate_random_location()
    destination = generate_random_location()

            
    attack_types = ['DDoS', 'Phishing', 'Malware Injection', 'SQL Injection', 
                   'Brute Force Login', "Port Scan", "Man-in-the-Middle", "Cross-Site Scripting"]
    attack_type = random.choice(attack_types)
    severity = random.randint(1, 10)
    print("attack_types:",attack_type)
    # Safer datetime generation
    
    timestamp = datetime.datetime.now() - datetime.timedelta(seconds=random.uniform(0, datetime.timedelta(days=60).total_seconds()))

    print("timesstamp",timestamp)
    additional_details = {
        "description": fake.text(max_nb_chars=200),
        "notes": fake.sentence()
    }
    return Attack(
        source_location=source,
        destination_location=destination,
        attack_type=attack_type,
        severity=severity,
        timestamp=timestamp,
        additional_details=additional_details
    )

def generate_and_save_attacks(num_attacks=10):
    """
    Generate a given number of attack records and save them to the database.
    """
    for i in range(num_attacks):
        try:
            attack = generate_random_attack()
            print("attack:",attack)
            attack.save()
            print(f"Saved attack with id: {attack.id}")
        except Exception as e:
            print(f"Error saving attack: {str(e)}")
            continue

def main():
    parser = argparse.ArgumentParser(
        description='Generate random attack data for the MongoDB database.'
    )
    parser.add_argument(
        '-n', '--num', type=int, default=10,
        help='Number of attack records to generate.'
    )
    args = parser.parse_args()

    try:
        mongoengine_connection()  # Ensure connection is established first
        generate_and_save_attacks(args.num)
        print(f"Generated {args.num} attack record(s).")
    except Exception as e:
        print(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    main()