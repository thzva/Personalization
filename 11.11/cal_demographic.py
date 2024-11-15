import json
from sentence_transformers import SentenceTransformer
import numpy as np

def calculate_and_save_similarity(data):
    if isinstance(data, str):
        data = json.loads(data)
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def get_location_similarity(loc1, loc2):
        if not loc1 or not loc2:
            return 0.0
            
        regions = {
            'east_asia_developed': ['Japan', 'South Korea', 'Taiwan', 'Hong Kong', 'Macau'],
            'east_asia_developing': ['China', 'Mongolia', 'North Korea'],
            'southeast_asia_developed': ['Singapore', 'Brunei'],
            'southeast_asia_developing': ['Thailand', 'Vietnam', 'Malaysia', 'Indonesia', 'Philippines', 'Myanmar', 'Cambodia', 'Laos', 'Timor-Leste'],
            'south_asia_major': ['India', 'Pakistan', 'Bangladesh'],
            'south_asia_minor': ['Sri Lanka', 'Nepal', 'Bhutan', 'Maldives', 'Afghanistan'],
            'central_asia': ['Kazakhstan', 'Uzbekistan', 'Kyrgyzstan', 'Tajikistan', 'Turkmenistan'],
            'middle_east_gcc': ['Saudi Arabia', 'UAE', 'Qatar', 'Kuwait', 'Bahrain', 'Oman'],
            'middle_east_levant': ['Syria', 'Lebanon', 'Israel', 'Jordan', 'Palestine'],
            'middle_east_other': ['Iran', 'Iraq', 'Turkey', 'Yemen'],
            'western_europe_nordic': ['Norway', 'Sweden', 'Denmark', 'Finland', 'Iceland'],
            'western_europe_central': ['Germany', 'France', 'Belgium', 'Netherlands', 'Luxembourg', 'Switzerland', 'Austria'],
            'western_europe_south': ['Italy', 'Spain', 'Portugal', 'Greece', 'Malta', 'Cyprus'],
            'western_europe_islands': ['United Kingdom', 'Ireland'],
            'eastern_europe_eu': ['Poland', 'Czech Republic', 'Slovakia', 'Hungary', 'Romania', 'Bulgaria', 'Croatia', 'Slovenia', 'Estonia', 'Latvia', 'Lithuania'],
            'eastern_europe_non_eu': ['Russia', 'Ukraine', 'Belarus', 'Moldova'],
            'eastern_europe_balkan': ['Serbia', 'Bosnia and Herzegovina', 'Montenegro', 'North Macedonia', 'Albania', 'Kosovo'],
            'north_america_anglo': ['United States', 'Canada'],
            'north_america_latin': ['Mexico'],
            'central_america_north': ['Guatemala', 'Honduras', 'El Salvador'],
            'central_america_south': ['Nicaragua', 'Costa Rica', 'Panama', 'Belize'],
            'caribbean_greater': ['Cuba', 'Haiti', 'Dominican Republic', 'Jamaica', 'Puerto Rico'],
            'caribbean_lesser': ['Trinidad and Tobago', 'Bahamas', 'Barbados', 'Saint Lucia', 'Grenada', 'Antigua and Barbuda', 
                               'Dominica', 'Saint Kitts and Nevis', 'Saint Vincent and the Grenadines'],
            'south_america_andean': ['Colombia', 'Venezuela', 'Ecuador', 'Peru', 'Bolivia'],
            'south_america_southern': ['Chile', 'Argentina', 'Uruguay', 'Paraguay'],
            'south_america_brazil': ['Brazil'],
            'south_america_guianas': ['Guyana', 'Suriname', 'French Guiana'],
            'north_africa_maghreb': ['Morocco', 'Algeria', 'Tunisia', 'Libya'],
            'north_africa_nile': ['Egypt', 'Sudan', 'South Sudan'],
            'west_africa_coastal': ['Nigeria', 'Ghana', 'Ivory Coast', 'Senegal', 'Guinea', 'Sierra Leone', 'Liberia'],
            'west_africa_sahel': ['Mali', 'Burkina Faso', 'Niger', 'Mauritania', 'Chad'],
            'west_africa_small': ['Benin', 'Togo', 'Gambia', 'Guinea-Bissau', 'Cape Verde'],
            'east_africa_great_lakes': ['Kenya', 'Tanzania', 'Uganda', 'Rwanda', 'Burundi'],
            'east_africa_horn': ['Ethiopia', 'Somalia', 'Djibouti', 'Eritrea'],
            'east_africa_islands': ['Seychelles', 'Comoros', 'Mauritius', 'Madagascar'],
            'central_africa_major': ['Democratic Republic of the Congo', 'Republic of the Congo', 'Cameroon'],
            'central_africa_minor': ['Central African Republic', 'Gabon', 'Equatorial Guinea', 'São Tomé and Príncipe'],
            'southern_africa_developed': ['South Africa', 'Namibia', 'Botswana'],
            'southern_africa_developing': ['Zimbabwe', 'Zambia', 'Mozambique', 'Angola', 'Malawi'],
            'southern_africa_small': ['Lesotho', 'Eswatini'],
            'oceania_developed': ['Australia', 'New Zealand'],
            'oceania_melanesia': ['Papua New Guinea', 'Fiji', 'Solomon Islands', 'Vanuatu', 'New Caledonia'],
            'oceania_polynesia': ['Samoa', 'Tonga', 'French Polynesia', 'American Samoa', 'Tuvalu']
        }
        
        region_groups = {
            'east_asia': ['east_asia_developed', 'east_asia_developing'],
            'southeast_asia': ['southeast_asia_developed', 'southeast_asia_developing'],
            'south_asia': ['south_asia_major', 'south_asia_minor'],
            'middle_east': ['middle_east_gcc', 'middle_east_levant', 'middle_east_other'],
            'western_europe': ['western_europe_nordic', 'western_europe_central', 'western_europe_south', 'western_europe_islands'],
            'eastern_europe': ['eastern_europe_eu', 'eastern_europe_non_eu', 'eastern_europe_balkan'],
            'north_america': ['north_america_anglo', 'north_america_latin'],
            'central_america': ['central_america_north', 'central_america_south'],
            'caribbean': ['caribbean_greater', 'caribbean_lesser'],
            'south_america': ['south_america_andean', 'south_america_southern', 'south_america_brazil', 'south_america_guianas'],
            'north_africa': ['north_africa_maghreb', 'north_africa_nile'],
            'west_africa': ['west_africa_coastal', 'west_africa_sahel', 'west_africa_small'],
            'east_africa': ['east_africa_great_lakes', 'east_africa_horn', 'east_africa_islands'],
            'central_africa': ['central_africa_major', 'central_africa_minor'],
            'southern_africa': ['southern_africa_developed', 'southern_africa_developing', 'southern_africa_small'],
            'oceania': ['oceania_developed', 'oceania_melanesia', 'oceania_polynesia']
        }
        
        def find_region(loc):
            for region, countries in regions.items():
                if any(country.lower() in loc.lower() for country in countries):
                    return region
            return None
        
        def find_group(region):
            for group, subregions in region_groups.items():
                if region in subregions:
                    return group
            return None
            
        loc1_region = find_region(loc1)
        loc2_region = find_region(loc2)
        loc1_group = find_group(loc1_region) if loc1_region else None
        loc2_group = find_group(loc2_region) if loc2_region else None
        
        if loc1.lower() == loc2.lower():
            return 1.0
        elif loc1_region and loc2_region:
            if loc1_region == loc2_region:
                return 0.9
            elif loc1_region.rsplit('_', 1)[0] == loc2_region.rsplit('_', 1)[0]:
                return 0.8
            elif loc1_group == loc2_group:
                return 0.7
            elif loc1_group and loc2_group:
                high_similarity_pairs = {
                    ('east_asia', 'southeast_asia'),
                    ('south_asia', 'southeast_asia'),
                    ('western_europe', 'eastern_europe'),
                    ('north_america', 'western_europe'),
                    ('north_africa', 'middle_east')
                }
                medium_similarity_pairs = {
                    ('central_asia', 'east_asia'),
                    ('central_asia', 'south_asia'),
                    ('central_asia', 'middle_east'),
                    ('south_america', 'central_america'),
                    ('caribbean', 'central_america'),
                    ('west_africa', 'north_africa'),
                    ('east_africa', 'north_africa'),
                    ('central_africa', 'west_africa'),
                    ('southern_africa', 'east_africa')
                }
                if {loc1_group, loc2_group} in high_similarity_pairs:
                    return 0.6
                elif {loc1_group, loc2_group} in medium_similarity_pairs:
                    return 0.5
                return 0.4
        return 0.3

    def calculate_text_similarity(text1, text2):
        if not text1 or not text2:
            return 0.0
        embeddings1 = model.encode([str(text1)])
        embeddings2 = model.encode([str(text2)])
        similarity = float(np.dot(embeddings1, embeddings2.T)[0][0])
        return max(0.0, min(1.0, similarity))

    def calculate_age_similarity(age1, age2):
        if not age1 or not age2:
            return 0.0
        try:
            age1, age2 = int(age1), int(age2)
            return 1 - min(abs(age1 - age2) / 100, 1)
        except:
            return 0.0

    weights = {
        'age': 0.10, 'gender': 0.10, 'geographic': 0.10,
        'location': 0.05, 'birth_country': 0.15, 'nationality': 0.15,
        'ethnicity': 0.15, 'languages': 0.10, 'household': 0.10
    }

    similarity_results = []
    keys = list(data.keys())

    for i in range(len(keys)-1):
        for j in range(i+1, len(keys)):
            user1_id = keys[i]
            user2_id = keys[j]
            user1 = data[user1_id]
            user2 = data[user2_id]
            
            scores = {
                'age': calculate_age_similarity(user1.get('age'), user2.get('age')),
                'gender': calculate_text_similarity(user1.get('gender'), user2.get('gender')),
                'geographic': calculate_text_similarity(str(user1.get('geographic_information')), str(user2.get('geographic_information'))),
                'location': get_location_similarity(user1.get('geographic_information', {}).get('location'), user2.get('geographic_information', {}).get('location')),
                'birth_country': calculate_text_similarity(user1.get('geographic_information', {}).get('country_of_birth'), user2.get('geographic_information', {}).get('country_of_birth')),
                'nationality': calculate_text_similarity(user1.get('geographic_information', {}).get('nationality'), user2.get('geographic_information', {}).get('nationality')),
                'ethnicity': calculate_text_similarity(user1.get('ethnicity_race'), user2.get('ethnicity_race')),
                'languages': calculate_text_similarity(str(user1.get('languages_spoken_or_written')), str(user2.get('languages_spoken_or_written'))),
                'household': calculate_text_similarity(str(user1.get('household_composition')), str(user2.get('household_composition')))
            }
            
            total_similarity = sum(scores[k] * weights[k] for k in scores)
            total_similarity = max(0.0, min(1.0, total_similarity))  # 确保最终结果也在0~1之间
            
            similarity_results.append({
                "person1": user1_id,
                "person2": user2_id,
                "similarity": total_similarity,
                "detailed_scores": scores  # 添加详细分数便于调试
            })
            print(f"Processed: {user1_id} - {user2_id}")

    output = {"physical_and_health_characteristics": similarity_results}
    
    with open('similarity_results1.json', 'w') as f:
        json.dump(output, f, indent=2)

    return output

if __name__ == "__main__":
    with open('demographic_information.json', 'r') as f:
        json_data = f.read()
    results = calculate_and_save_similarity(json_data)