import pandas as pd
import folium

# Load the dataset
df_londonstations = pd.read_csv('/Users/marijn/Downloads/London stations.csv')

# List of stations you want to show
stations_to_show = [
    "Acton Town", "Aldgate", "Aldgate East", "Alperton", "Amersham", "Angel", "Archway", "Arnos Grove", "Arsenal",
    "Baker Street", "Balham LU", "Bank and Monument", "Barbican", "Barking", "Barkingside", "Barons Court", "Bayswater",
    "Becontree", "Belsize Park", "Bermondsey", "Bethnal Green LU", "Blackfriars LU", "Blackhorse Road", "Bond Street",
    "Borough", "Boston Manor", "Bounds Green", "Bow Road", "Brent Cross", "Brixton LU", "Bromley-by-Bow", "Buckhurst Hill",
    "Burnt Oak", "Caledonian Road", "Camden Town", "Canada Water", "Canary Wharf LU", "Canning Town", "Cannon Street LU",
    "Canons Park", "Chalfont & Latimer", "Chalk Farm", "Chancery Lane", "Charing Cross LU", "Chesham", "Chigwell", "Chiswick Park",
    "Chorleywood", "Clapham Common", "Clapham North", "Clapham South", "Cockfosters", "Colindale", "Colliers Wood", "Covent Garden",
    "Croxley", "Dagenham East", "Dagenham Heathway", "Debden", "Dollis Hill", "Ealing Broadway", "Ealing Common", "Earl's Court",
    "East Acton", "East Finchley", "East Ham", "East Putney", "Eastcote", "Edgware", "Edgware Road (Bak)", "Edgware Road (DIS)",
    "Elephant & Castle LU", "Elm Park", "Embankment", "Epping", "Euston LU", "Euston Square", "Fairlop", "Farringdon", "Finchley Central",
    "Finchley Road", "Finsbury Park", "Fulham Broadway", "Gants Hill", "Gloucester Road", "Golders Green", "Goldhawk Road", "Goodge Street",
    "Grange Hill", "Great Portland Street", "Green Park", "Greenford", "Gunnersbury", "Hainault", "Hammersmith (DIS)", "Hammersmith (H&C)",
    "Hampstead", "Hanger Lane", "Harlesden", "Harrow & Wealdstone", "Harrow-on-the-Hill", "Hatton Cross", "Heathrow Terminal 4 LU",
    "Heathrow Terminal 5 LU", "Heathrow Terminals 123 LU", "Hendon Central", "High Barnet", "High Street Kensington", "Highbury & Islington",
    "Highgate", "Hillingdon", "Holborn", "Holland Park", "Holloway Road", "Hornchurch", "Hounslow Central", "Hounslow East", "Hounslow West",
    "Hyde Park Corner", "Ickenham", "Kennington", "Kensal Green", "Kensington (Olympia)", "Kentish Town", "Kenton", "Kew Gardens", "Kilburn",
    "Kilburn Park", "King's Cross St. Pancras", "Kingsbury", "Knightsbridge", "Ladbroke Grove", "Lambeth North", "Lancaster Gate", "Latimer Road",
    "Leicester Square", "Leyton", "Leytonstone", "Liverpool Street LU", "London Bridge LU", "Loughton", "Maida Vale", "Manor House",
    "Mansion House", "Marble Arch", "Marylebone LU", "Mile End", "Mill Hill East", "Moor Park", "Moorgate", "Morden", "Mornington Crescent",
    "Neasden", "Newbury Park", "North Acton", "North Ealing", "North Greenwich", "North Harrow", "North Wembley", "Northfields", "Northolt",
    "Northwick Park", "Northwood", "Northwood Hills", "Notting Hill Gate", "Oakwood", "Old Street", "Osterley", "Oval", "Oxford Circus",
    "Paddington TfL", "Park Royal", "Parsons Green", "Perivale", "Piccadilly Circus", "Pimlico", "Pinner", "Plaistow", "Preston Road",
    "Putney Bridge", "Queen's Park", "Queensbury", "Queensway", "Ravenscourt Park", "Rayners Lane", "Redbridge", "Regent's Park", "Richmond",
    "Rickmansworth", "Roding Valley", "Royal Oak", "Ruislip", "Ruislip Gardens", "Ruislip Manor", "Russell Square", "Seven Sisters",
    "Shepherd's Bush LU", "Shepherd's Bush Market", "Sloane Square", "Snaresbrook", "South Ealing", "South Harrow", "South Kensington",
    "South Kenton", "South Ruislip", "South Wimbledon", "South Woodford", "Southfields", "Southgate", "Southwark", "St. James's Park",
    "St. John's Wood", "St. Paul's", "Stamford Brook", "Stanmore", "Stepney Green", "Stockwell", "Stonebridge Park", "Stratford", "Sudbury Hill",
    "Sudbury Town", "Swiss Cottage", "Temple", "Theydon Bois", "Tooting Bec", "Tooting Broadway", "Tottenham Court Road", "Tottenham Hale LU",
    "Totteridge & Whetstone", "Tower Hill", "Tufnell Park", "Turnham Green", "Turnpike Lane", "Upminster", "Upminster Bridge", "Upney",
    "Upton Park", "Uxbridge", "Vauxhall LU", "Victoria LU", "Walthamstow Central", "Wanstead", "Warren Street", "Warwick Avenue", "Waterloo LU",
    "Watford", "Wembley Central", "Wembley Park", "West Acton", "West Brompton", "West Finchley", "West Ham", "West Hampstead LU",
    "West Harrow", "West Kensington", "West Ruislip", "Westbourne Park", "Westminster", "White City", "Whitechapel", "Willesden Green",
    "Willesden Junction", "Wimbledon", "Wimbledon Park", "Wood Green", "Wood Lane", "Woodford", "Woodside Park", "Nine Elms", "Battersea Power Station",
    "Acton Central", "Anerley", "Barking", "Battersea Park", "Bethnal Green LO", "Blackhorse Road", "Brockley", "Brondesbury", "Brondesbury Park",
    "Bruce Grove", "Bush Hill Park", "Bushey", "Caledonian Road & Barnsbury", "Cambridge Heath", "Camden Road", "Canada Water", "Canonbury",
    "Carpenders Park", "Cheshunt", "Chingford", "Clapham High Street", "Clapham Junction", "Clapton", "Crouch Hill", "Crystal Palace", "Dalston Junction",
    "Dalston Kingsland", "Denmark Hill", "Edmonton Green", "Emerson Park", "Enfield Town", "Euston NR", "Finchley Road & Frognal", "Forest Hill",
    "Gospel Oak", "Gunnersbury", "Hackney Central", "Hackney Downs", "Hackney Wick", "Haggerston", "Hampstead Heath", "Harlesden",
    "Harringay Green Lanes", "Harrow & Wealdstone", "Hatch End", "Headstone Lane", "Highams Park", "Highbury & Islington", "Homerton", "Honor Oak Park",
    "Hoxton", "Imperial Wharf", "Kensal Green", "Kensal Rise", "Kensington (Olympia)", "Kentish Town West", "Kenton", "Kew Gardens", "Kilburn High Road",
    "Leyton Midland Road", "Leytonstone High Road", "Liverpool Street NR", "London Fields", "New Cross", "New Cross Gate", "North Wembley", "Norwood Junction",
    "Peckham Rye", "Penge West", "Queen's Park", "Queens Road Peckham", "Rectory Road", "Richmond", "Romford", "Rotherhithe", "Seven Sisters", "Shadwell LO",
    "Shepherd's Bush NR", "Shoreditch High Street", "Silver Street", "South Acton", "South Hampstead", "South Kenton", "South Tottenham", "Southbury",
    "St James Street", "Stamford Hill", "Stoke Newington", "Stonebridge Park", "Stratford", "Surrey Quays", "Sydenham", "Theobalds Grove", "Turkey Street",
    "Upminster", "Upper Holloway", "Walthamstow Central", "Walthamstow Queen's Road", "Wandsworth Road", "Wanstead Park", "Wapping", "Watford High Street",
    "Watford Junction", "Wembley Central", "West Brompton", "West Croydon NR", "West Hampstead LO", "White Hart Lane", "Whitechapel", "Willesden Junction",
    "Wood Street", "Woodgrange Park", "Abbey Road", "All Saints", "Bank and Monument", "Beckton", "Beckton Park", "Blackwall", "Bow Church", "Canary Wharf DLR",
    "Canning Town", "Crossharbour", "Custom House", "Cutty Sark", "Cyprus", "Deptford Bridge", "Devons Road", "East India", "Elverson Road", "Gallions Reach",
    "Greenwich", "Heron Quays", "Island Gardens", "King George V", "Langdon Park", "Lewisham DLR", "Limehouse DLR", "London City Airport", "Mudchute",
    "Pontoon Dock", "Poplar", "Prince Regent", "Pudding Mill Lane", "Royal Albert", "Royal Victoria", "Shadwell DLR", "South Quay", "Star Lane", "Stratford",
    "Stratford High Street", "Stratford International DLR", "Tower Gateway", "West Ham", "West India Quay", "West Silvertown", "Westferry", "Woolwich Arsenal",
    "Acton Main Line", "Brentwood", "Burnham", "Chadwell Heath", "Ealing Broadway", "Forest Gate", "Gidea Park", "Goodmayes", "Hanwell", "Harold Wood",
    "Hayes & Harlington", "Heathrow Terminal 4 EL", "Heathrow Terminal 5 EL", "Heathrow Terminals 2 & 3 EL", "Ilford", "Iver", "Langley", "Liverpool Street NR",
    "Maidenhead", "Manor Park", "Maryland", "Paddington NR", "Reading", "Romford", "Seven Kings", "Shenfield", "Slough", "Southall", "Stratford", "Taplow",
    "Twyford", "West Drayton", "West Ealing"
]

# Filter the DataFrame to keep only the stations in the list
df_filtered = df_londonstations[df_londonstations['Station'].isin(stations_to_show)]

# Create a map centered on London
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

# Add markers for each station in the filtered DataFrame
for index, row in df_filtered.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['Station']
    ).add_to(m)

m
