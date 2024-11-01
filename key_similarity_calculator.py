import json
from datetime import datetime

def calculate_interests_similarity(profile1, profile2):
    """计算兴趣爱好的相似度"""
    score = 0
    total = 4
    
    # 兴趣爱好相似度
    hobbies1 = set(profile1['preferencesAndInterests']['hobbiesAndInterests'])
    hobbies2 = set(profile2['preferencesAndInterests']['hobbiesAndInterests'])
    if len(hobbies1.intersection(hobbies2)) / max(len(hobbies1), len(hobbies2)) > 0.3:
        score += 1
    
    # 内容偏好相似度
    content1 = set(profile1['preferencesAndInterests']['contentPreferences'])
    content2 = set(profile2['preferencesAndInterests']['contentPreferences'])
    if len(content1.intersection(content2)) / max(len(content1), len(content2)) > 0.3:
        score += 1
    
    # 品牌偏好相似度
    brands1 = set(profile1['preferencesAndInterests']['shoppingPreferences']['preferredBrands'])
    brands2 = set(profile2['preferencesAndInterests']['shoppingPreferences']['preferredBrands'])
    if len(brands1.intersection(brands2)) / max(len(brands1), len(brands2)) > 0.3:
        score += 1
    
    # 饮食偏好相似度
    diet1 = set(profile1['preferencesAndInterests']['dietaryPreferences'])
    diet2 = set(profile2['preferencesAndInterests']['dietaryPreferences'])
    if len(diet1.intersection(diet2)) / max(len(diet1), len(diet2)) > 0.3:
        score += 1
    
    return score / total

def calculate_lifestyle_similarity(profile1, profile2):
    """计算生活方式的相似度"""
    score = 0
    total = 4
    
    # 政治观点相似度
    if profile1['politicalViews'] == profile2['politicalViews']:
        score += 1
    
    # 生活习惯相似度
    habits1 = set(profile1['psychographicInformation']['lifestyle']['dailyHabits'])
    habits2 = set(profile2['psychographicInformation']['lifestyle']['dailyHabits'])
    if len(habits1.intersection(habits2)) / max(len(habits1), len(habits2)) > 0.3:
        score += 1
    
    # 健康目标相似度
    health1 = set(profile1['fitness']['healthGoals'])
    health2 = set(profile2['fitness']['healthGoals'])
    if len(health1.intersection(health2)) / max(len(health1), len(health2)) > 0.3:
        score += 1
    
    # 运动偏好相似度
    exercise1 = set(profile1['fitness']['exercisePreferences'])
    exercise2 = set(profile2['fitness']['exercisePreferences'])
    if len(exercise1.intersection(exercise2)) / max(len(exercise1), len(exercise2)) > 0.3:
        score += 1
    
    return score / total

def process_key_similarities():
    """处理档案并计算关键相似度"""
    # 读取数据
    with open('results.json', 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    
    results = []
    for i, profile1 in enumerate(profiles):
        for j, profile2 in enumerate(profiles[i+1:], start=i+1):
            similarity = {
                'person1': f"{profile1['profile']['basicPersonalInformation']['fullName']['firstName']} {profile1['profile']['basicPersonalInformation']['fullName']['lastName']}",
                'person2': f"{profile2['profile']['basicPersonalInformation']['fullName']['firstName']} {profile2['profile']['basicPersonalInformation']['fullName']['lastName']}",
                'interests_similarity': calculate_interests_similarity(profile1['profile'], profile2['profile']),
                'lifestyle_similarity': calculate_lifestyle_similarity(profile1['profile'], profile2['profile'])
            }
            results.append(similarity)
    
    # 保存结果
    output = {
        "timestamp": datetime.now().isoformat(),
        "similarities": results
    }
    
    with open('key_similarity.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    process_key_similarities()
    print("关键相似度计算完成，结果已保存到 key_similarity.json")