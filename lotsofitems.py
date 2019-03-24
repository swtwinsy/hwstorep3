from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Hardware_Category, Hardware_Item, User


engine = create_engine('sqlite:///hardwarestorecatalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# adding user
User1 = User(name="soeh wong", email="wongsoeh@gmail.com",
             picture='https://lh3.googleusercontent.com/n-FzagHAa6Ay5w1XGm6K'
             'inwEKTJBIF87ZzHGCEv-8sg8DeM4uY7Z1rPmjmoc1YfKKg-sOj11BOy5iES54'
             'DDSRwsUjvbByJgBFvyWw13E451e4QjWJ6GlJFD4VOHPRBGS5NdyWKpzzuhBaBf'
             '8gf4E2khHp0LKaIzzWR_GR1rVCewi-Pu7BNIIi1fBnbrnCEpQWNSEsOuG0YIoS'
             'KKQ3HXwDfAlcumPuqvOWOFgc9tyknnpe-OhAjwZ-7a_A-d5Vy6koc9JOLN9ZZS'
             '2noND_uLAR2hoL12RkOrZF0RPR8XH0yuFTkxrxPn3NjKZmr6mNOUhY_UQEYWt'
             'rfHL_GzZhtw0vRpV8H6C_HfaPtLZAHsoex9zIH3sWSbURuKA0fynIZQnIHVfeQ'
             '2n59R-MKBvMRiyhpCQ4e_L1vYZBXtdVNYRkqstoDAzcXjll7vcvcGmdHQd8FP0'
             'wuRUS0Oj4O6TkHSLpqFPWRsgPXG-OUi0zWACE82OlmYRtAUdJJ-QKfqmk8UUreh'
             'Ld35KagpAwpeZXoSiXnZ3MOhh2NfWzH6mL7W5uq2PvgvoM8IAs7NkjqJrxarNe'
             '3G6nsRJcIZTdwgK_oFARv-9aG9Gf-cJxVE2qrnixikXI7XVarFOSYc_O336FM39'
             '7xovm1A1X5meFdfSxj_Tn3hDdicdOJXURov3FsOROdp-uppfbVWj3cj0CdK6QE4y'
             '69l8_goh-2dpRjMAyMIiK3M=w326-h266-no')
session.add(User1)
session.commit()

User2 = User(name="Marina Urrutia", email="murrutia.aws@gmail.com",
             picture='https://lh3.googleusercontent.com/QHXvKBPbzk7g'
             'aOREyokdbOMX23ucCJ0gdx-TkfcbJsqLAxCZZ-pDojpabD4Nfn6R3YBb'
             'AKik6Xzv9bIKnadSroDp5YzHFWRrqF-H_cejunEQj-aBakKODWdYTFNf'
             'n681jskVPPm9D3oS_oCiyLx1HAVbdYlBkMevy44A-47O0BcGvuuymhQT'
             'WogwQmwQ1NhgxvZFFcyZPx3j5FI23l4godjNre9CIQ_lr9UqGuBpPDI'
             'LlP6EsT1GrdnG6CdDFN16d-Of5tZslf1u6st8OAJps0uJBLDR22MUos_mV'
             'vMG5NNMBb0YJVetjt1l1JweEiwdjh3cdXp1ofveipKmm7X_fUzLZHVtsN0'
             'AAmhxxZeNTvg6p-ICZgKEYkI6ep7K6jwi28aBSeJgIBl_iUuxLtZkBKqq'
             'VF_8X0nL9m0nDE3oyEkc754yYZzgwsuyH7Dd8SKbKSxqLTIID5DDdllgzcp'
             '6xPO2CcrOTYqShCupVCjReYKpdgk9mRyhXKUvQJSCQoEZ5wzWnuOtcT7Ya55'
             'uU0kH1xLEpSpeWRmGtYPjMD0EG6ouF59Skbsvlrvc7bAIwTECczYLcLdhWVx'
             '2kv3b_8Mpx7BdN-MhPmpGyaI8bmfVSobBCQEeo_rOX7Z91aH99F87mc_xNgkX'
             'SGTqyppoN-w4TdcfBcOrQZDPF12LuI1SJnQUsYEe7hz4xz6FhUmyQyQ4IWats'
             'F2eFioUL8xMJ-g1Q70=w329-h338-no')
session.add(User2)
session.commit()


# First Category "Building Materials"
category1 = Hardware_Category(user_id=1, name="Building Materials",
                              description='Within this category you will '
                              'find all materials necesary to build walls '
                              'and fences.')
session.add(category1)
session.commit()

# Items in category Building Materials
Item1 = Hardware_Item(user_id=1, name="Concrete Mix",
                      description="dries completely within 24 hours,"
                      "ideal for patios and walkways. 40 lbs",
                      price="$24.47", category=category1)
session.add(Item1)
session.commit()


Item2 = Hardware_Item(user_id=1, name="Drywall Panel",
                      description="Gypsum patcing panel drywall,"
                      " Small design is ideal for lightweight repair jobs.",
                      price="$4.98", category=category1)
session.add(Item2)
session.commit()

Item3 = Hardware_Item(user_id=1, name="Bricks",
                      description="Flat bricks , box of 50 units,"
                      " dimmensions: 2 x 7 x 1/2",
                      price="$68.00", category=category1)
session.add(Item3)
session.commit()

# Second Category Bath and Faucets

category2 = Hardware_Category(user_id=2, name="Bath and Faucets",
                              description="within this category you will"
                              "find all items necesary for the average "
                              "bathroom")
session.add(category2)
session.commit()

Item1 = Hardware_Item(user_id=2, name="Faucet",
                      description="single hole bathroom faucet in chrome.",
                      price="$89.00", category=category2)
session.add(Item1)
session.commit()

Item2 = Hardware_Item(user_id=2, name="Bathtub",
                      description="everyday bathtub , Acrylic Bath and Shower"
                      "kit with Left Drain in White.",
                      price="$379.00", category=category2)
session.add(Item2)
session.commit()

Item3 = Hardware_Item(user_id=2, name="Sink",
                      description="Pedestal Combo Bathromm Sink in white.",
                      price="$144.00", category=category2)
session.add(Item3)
session.commit()

# Third Category Electrical
category3 = Hardware_Category(user_id=1, name="Electrical",
                              description="withing this category you will "
                              "find all items necesary to all electrical "
                              "installations necesary for a home.")
session.add(category3)
session.commit()

Item1 = Hardware_Item(user_id=1, name="Lightbulb",
                      description="Watt equivalent spiral non-dimmaable CFL"
                      "light Bulb soft white . 4 pack",
                      price="$5.97", category=category3)
session.add(Item1)
session.commit()

Item2 = Hardware_Item(user_id=1, name="Wire",
                      description="250ft 14/2 solid romex simpull cu /G wire",
                      price="$45.97", category=category3)
session.add(Item2)
session.commit()

Item3 = Hardware_Item(user_id=1, name="Electrical Pliers",
                      description="combination electricians wire strippers.",
                      price="$24.97", category=category3)
session.add(Item3)
session.commit()


# Fourth category Flooring
category4 = Hardware_Category(user_id=1, name="Flooring",
                              description="In this category you will find all"
                              "necesary items to install and accessories the"
                              " floor of your home.")
session.add(category4)
session.commit()

Item1 = Hardware_Item(user_id=1, name="Tile",
                      description="Bengal Brown 11.77 in x 11.57 in x 8 nn "
                      "Stone. Self- Adhesive Wall Mosaic.",
                      price="$13.66", category=category4)
session.add(Item1)
session.commit()

Item2 = Hardware_Item(user_id=1, name="Rug",
                      description="Asha gray 9 ft. x 13 ft. Area Rug.",
                      price="$39.98", category=category4)
session.add(Item2)
session.commit()

Item3 = Hardware_Item(user_id=1, name="Hardware Flooring",
                      description="Hickory Heritage Grey Hand Sculputed 3/4"
                      " in thick x4 in Wide x Randon Lenght Solid Hardwood. ",
                      price="$5.99", category=category4)

session.add(Item3)
session.commit()


print("added items by categories!")
