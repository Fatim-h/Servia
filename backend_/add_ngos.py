# add_ngos.py
from app import create_app, db
from app.models import Category, Location, NGO
from werkzeug.security import generate_password_hash

app = create_app()

def add_sample_data():
    with app.app_context():
        print("Adding sample data...")
        
        # Create categories
        categories = [
            Category(name='Welfare', description='General social welfare services'),
            Category(name='Emergency Services', description='Ambulance and emergency response'),
            Category(name='Disability Care', description='Care and rehabilitation for disabled individuals'),
            Category(name='Disaster Relief', description='Emergency response and disaster management'),
            Category(name='Healthcare', description='Medical and health services'),
            Category(name='Education', description='Educational institutions and programs'),
            Category(name='Arts & Culture', description='Promotion of arts and cultural activities'),
            Category(name='Human Rights', description='Human rights advocacy and legal aid'),
            Category(name='Poverty Alleviation', description='Poverty reduction and social welfare')
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        print(f"Added {len(categories)} categories")
        
        # Create locations
        locations = [
            Location(city='Karachi', county='Sindh', address='Multiple locations across Karachi'),
            Location(city='Karachi', county='Sindh', address='A-25, Bahadurabad, Karachi'),
            Location(city='Karachi', county='Sindh', address='Plot C-76, Sector 31/5, Korangi Crossing, Karachi'),
            Location(city='Karachi', county='Sindh', address='M.R. Kiyani Road, Karachi'),
            Location(city='Karachi', county='Sindh', address='159 H-3, Kashmir Road, PECHS'),
            Location(city='Karachi', county='Sindh', address='B-24, Federal B Area Ancholi Block 20')
        ]
        
        for location in locations:
            db.session.add(location)
        
        db.session.commit()
        print(f"Added {len(locations)} locations")
        
        # Create NGOs
        category_map = {cat.name: cat.category_id for cat in Category.query.all()}
        
        ngos = [
            NGO(name='Chhipa Welfare Association', location_id=1, category_id=category_map['Welfare'],
                contact='+92-21-111-111-134; +92-21-111-92-1020', email='info@chhipa.org', year_established=1987,
                organization_head='Ramzan Chhipa (Founder)', website='https://chhipa.org/', is_verified=True,
                description='Provides ambulance services, free meals (Dastarkhawan), morgue, graveyard, shelter, etc., operating with a humanitarian mission.'),
            
            NGO(name='Edhi Foundation', location_id=1, category_id=category_map['Welfare'],
                contact='(021) 32413232 (Edhi Head Office)', email='edhikarachi@hotmail.com', year_established=1951,
                organization_head='Abdul Sattar Edhi', website='https://edhi.org/', is_verified=True,
                description='One of Pakistan\'s biggest welfare organizations — ambulance service, orphanages, langar, hospitals, homes for elderly, etc.'),
            
            NGO(name='Darul Sukun', location_id=5, category_id=category_map['Disability Care'],
                contact='0337 7778586; (021)34558797 / 98 / 99', email='darulsukunpak@gmail.com', year_established=1969,
                organization_head='Sr. Gertrude Lemmens', website='https://darulsukun.com/', is_verified=True,
                description='Home for physically and mentally disabled children / adults, provides rehabilitation, education, shelter, care.'),
            
            NGO(name='JDC Welfare Organization', location_id=6, category_id=category_map['Disaster Relief'],
                contact='(021) 36341059', email='info@jdcwelfare.org', year_established=2009,
                organization_head='Syed Zafar Abbas Jafri', website='https://jdcwelfare.org/', is_verified=True,
                description='Provides ambulance service, disaster relief, free education, shelter, etc.'),
            
            NGO(name='Saylani Welfare International Trust', location_id=2, category_id=category_map['Poverty Alleviation'],
                contact='(021) 111-729526; (021)34130786 / 87', email='info@saylaniwelfare.com', year_established=1999,
                organization_head='Maulana Bashir Farooq Qadri', website='https://saylaniwelfare.com/', is_verified=True,
                description='Very active trust: food distribution (dastarkhawan), welfare, education, ambulance, social development.'),
            
            NGO(name='Indus Hospital', location_id=3, category_id=category_map['Healthcare'],
                contact='(021) 3511 2709–17', email='crd@tih.org.pk', year_established=2007,
                organization_head='Dr. Abdul Bari Khan', website='https://indushealthnetwork.org/', is_verified=True,
                description='Non-profit healthcare network providing free, high-quality healthcare across Pakistan. Started as a 150-bed tertiary hospital in Karachi; now has a network of hospitals, blood centers, and rehab centers.'),
            
            NGO(name='The Citizens Foundation', location_id=1, category_id=category_map['Education'],
                contact='(021) 35113445–59 (Head Office Karachi)', email='info@tcf.org.pk', year_established=1995,
                organization_head='Zia Akhter Abbas', website='https://www.tcf.org.pk/', is_verified=True,
                description='Builds & runs low-cost formal schools in Pakistan, especially for underprivileged children.'),
            
            NGO(name='The Arts Council of Pakistan', location_id=4, category_id=category_map['Arts & Culture'],
                contact='(021) 111-227-544', email='info@acpkhi.com', year_established=1995,
                organization_head='Dr. Esmat Rahim, Syed Amjad Ali, and Jalaluddin Ahmed', website='https://artscouncil.org.pk/', is_verified=True,
                description='Promotes arts, cultural events, theater, literature in Pakistan.'),
            
            NGO(name='Zindagi Trust', location_id=1, category_id=category_map['Education'],
                contact='(021) 34305614 / 111-111-439', email='info@zindagitrust.org', year_established=2007,
                organization_head='Shehryar Kapadia', website='https://zindagitrust.org/', is_verified=True,
                description='Works to improve public education in Pakistan, builds model schools, supports underprivileged students.'),
            
            NGO(name='Ansar Burney Trust', location_id=1, category_id=category_map['Human Rights'],
                contact='(021) 32623382-3; (021) 34120146-7', email='info@ansarburneytrust.com', year_established=1980,
                organization_head='Ansar Burney', website='https://ansarburney.org/', is_verified=True,
                description='Human rights advocacy, legal aid for prisoners, missing persons, civil liberties.')
        ]
        
        for ngo in ngos:
            db.session.add(ngo)
        
        db.session.commit()
        print(f"Added {len(ngos)} NGOs")
        
        print("\nSample data added successfully!")
        print(f"Total NGOs: {NGO.query.count()}")
        print(f"Total Categories: {Category.query.count()}")
        print(f"Total Locations: {Location.query.count()}")

if __name__ == '__main__':
    add_sample_data()