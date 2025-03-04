import os
import datetime
import pymongo
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]
exhibitions_collection = db["exhibitions"]

# Sample exhibition data
sample_exhibitions = [
    {
        "title": "Dreamscapes: An Impressionist Journey",
        "dates": {
            "start": "2025-03-15",
            "end": "2025-04-30"
        },
        "location": "ArtSpace Gallery, New York",
        "cost": 15.00,
        "artist": {
            "artist": "Alice Monet",
            "profile_url": "https://artistportfolio.com/alice-monet"
        },
        "art_style": "Impressionist",
        "art_medium": "Paintings",
        "event_type": "Launch Party",
        "description": "A mesmerizing collection of impressionist landscapes.",
        "image_url": "https://cdn.britannica.com/78/43678-050-F4DC8D93/Starry-Night-canvas-Vincent-van-Gogh-New-1889.jpg",
        "created_by": "alice_monet",  # Track the artist who created it
        "created_at": datetime.datetime.utcnow()
    },
    {
        "title": "Neon Realities",
        "dates": {
            "start": "2025-04-10",
            "end": "2025-05-25"
        },
        "location": "Downtown Arts Hub, LA",
        "cost": 20.00,
        "artist": {
            "artist": "Leo Stark",
            "profile_url": "https://artistportfolio.com/leo-stark"
        },
        "art_style": "Modern",
        "art_medium": "Digital Art",
        "event_type": "Pop-up",
        "description": "A deep dive into neon-inspired digital artworks.",
        "image_url": "https://d7hftxdivxxvm.cloudfront.net/?quality=80&resize_to=width&src=https%3A%2F%2Fd32dm0rphc51dk.cloudfront.net%2FGlnSAifRpCwTgh6M93pBqw%2Fnormalized.jpg&width=910",
        "created_by": "leo_stark",
        "created_at": datetime.datetime.utcnow()
    },
    {
        "title": "Abstract Wonders",
        "dates": {
            "start": "2025-02-01",
            "end": "2025-02-28"
        },
        "location": "Gallery 77, Chicago",
        "cost": 10.00,
        "artist": {
            "artist": "Samantha Raye",
            "profile_url": "https://artistportfolio.com/samantha-raye"
        },
        "art_style": "Abstract",
        "art_medium": "Mixed Media",
        "event_type": "Exhibition",
        "description": "A collection of abstract mixed-media masterpieces.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/63/Robert_Delaunay%2C_1913%2C_Premier_Disque%2C_134_cm%2C_52.7_inches%2C_Private_collection.jpg",
        "created_by": "samantha_raye",
        "created_at": datetime.datetime.utcnow()
    },
    {
        "title": "Cosmic Vibrations",
        "dates": {"start": "2025-05-20", "end": "2025-06-30"},
        "location": "Astro Arts Center, San Francisco",
        "cost": 12.00,
        "artist": {"artist": "Zane Vega", "profile_url": "https://artistportfolio.com/zane-vega"},
        "art_style": "Psychedelic",
        "art_medium": "Interactive Installations",
        "event_type": "Exhibition",
        "description": "A sensory experience of colors, sounds, and cosmic energy.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSn3DZaGkOo6Rn4L6KuxzaL6y1Y-kqOx-jN3g&s",
        "created_by": "zane_vega",
        "created_at": datetime.datetime.utcnow()
    },
    {
        "title": "Urban Decay",
        "dates": {"start": "2025-10-01", "end": "2025-11-15"},
        "location": "Metro Arts District, Berlin",
        "cost": 8.00,
        "artist": {"artist": "Kai Richter", "profile_url": "https://artistportfolio.com/kai-richter"},
        "art_style": "Street Art",
        "art_medium": "Mixed Media",
        "event_type": "Exhibition",
        "description": "A raw look at modern urban landscapes through street art.",
        "image_url": "https://images.unsplash.com/photo-1611063158871-7dd3ed4a2ac8?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dXJiYW4lMjBhcnR8ZW58MHx8MHx8fDA%3D",
        "created_by": "kai_richter",
        "created_at": datetime.datetime.utcnow()
    },
    {
        "title": "Whispering Shadows",
        "dates": {"start": "2025-08-05", "end": "2025-09-10"},
        "location": "Nocturne Gallery, Tokyo",
        "cost": 22.00,
        "artist": {"artist": "Haruto Kuroi", "profile_url": "https://artistportfolio.com/haruto-kuroi"},
        "art_style": "Gothic",
        "art_medium": "Photography & Installations",
        "event_type": "Immersive Experience",
        "description": "A hauntingly beautiful look at darkness and mystery in visual art.",
        "image_url": "https://miro.medium.com/v2/resize:fit:1400/1*hlOcXsNMWEb4vR-4zKtqow.jpeg",
        "created_by": "haruto_kuroi",
        "created_at": datetime.datetime.utcnow()
    },
    {
        "title": "The Minimalist Perspective",
        "dates": {"start": "2025-07-01", "end": "2025-07-31"},
        "location": "Modern Spaces, Copenhagen",
        "cost": 14.50,
        "artist": {"artist": "Elena Voss", "profile_url": "https://artistportfolio.com/elena-voss"},
        "art_style": "Minimalism",
        "art_medium": "Sculptures & Paintings",
        "event_type": "Exhibition",
        "description": "A calming and thought-provoking dive into minimalist aesthetics.",
        "image_url": "https://cdn.shopify.com/s/files/1/0369/6522/0411/files/550n09932-9wvtd-install_600x600.jpg?v=1670397551",
        "created_by": "elena_voss",
        "created_at": datetime.datetime.utcnow()
    },
    {
        "title": "Cybernetic Dreams",
        "dates": {"start": "2025-11-20", "end": "2026-01-10"},
        "location": "TechArts Lab, Seoul",
        "cost": 30.00,
        "artist": {"artist": "Jin Seo", "profile_url": "https://artistportfolio.com/jin-seo"},
        "art_style": "Cyberpunk",
        "art_medium": "Digital Art & VR",
        "event_type": "Showcase",
        "description": "A fusion of technology and art, exploring cyberpunk aesthetics.",
        "image_url": "https://images.pexels.com/photos/8721342/pexels-photo-8721342.jpeg",
        "created_by": "jin_seo",
        "created_at": datetime.datetime.utcnow()
    }
]

# Insert into MongoDB
exhibitions_collection.delete_many({})
exhibitions_collection.insert_many(sample_exhibitions)
print("Sample exhibitions inserted successfully!")
