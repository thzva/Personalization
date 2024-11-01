import json
import numpy as np
from datetime import datetime
from collections import Counter

def calculate_basic_info_similarity(profile1, profile2):
    """计算基本信息的相似度"""
    score = 0
    total = 5
    
    # 性别相似度
    if profile1['basicPersonalInformation']['gender'] == profile2['basicPersonalInformation']['gender']:
        score += 1
    
    # 婚姻状态相似度
    if profile1['basicPersonalInformation']['maritalStatus'] == profile2['basicPersonalInformation']['maritalStatus']:
        score += 1
    
    # 国籍相似度
    if profile1['additionalPersonalInformation']['nationality'] == profile2['additionalPersonalInformation']['nationality']:
        score += 1
    
    # 城市相似度
    if profile1['additionalPersonalInformation']['cityOfResidence'] == profile2['additionalPersonalInformation']['cityOfResidence']:
        score += 1
    
    # 语言相似度
    languages1 = set(profile1['additionalPersonalInformation']['languagesSpoken'])
    languages2 = set(profile2['additionalPersonalInformation']['languagesSpoken'])
    if len(languages1.intersection(languages2)) / max(len(languages1), len(languages2)) > 0.5:
        score += 1
    
    return score / total

def calculate_professional_similarity(profile1, profile2):
    """计算职业相关的相似度"""
    score = 0
    total = 4
    
    # 职业相似度
    if profile1['professionalInformation']['currentOccupation'] == profile2['professionalInformation']['currentOccupation']:
        score += 1
    
    # 行业相似度
    if profile1['professionalInformation']['industry'] == profile2['professionalInformation']['industry']:
        score += 1
    
    # 经验水平相似度
    if profile1['professionalInformation']['experienceLevel'] == profile2['professionalInformation']['experienceLevel']:
        score += 1
    
    # 技能相似度
    skills1 = set(profile1['professionalInformation']['skills'])
    skills2 = set(profile2['professionalInformation']['skills'])
    if len(skills1.intersection(skills2)) / max(len(skills1), len(skills2)) > 0.3:
        score += 1
    
    return score / total

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

def calculate_overall_similarity(profile1, profile2):
    """计算总体相似度"""
    weights = {
        'basic': 0.2,
        'professional': 0.3,
        'interests': 0.25,
        'lifestyle': 0.25
    }
    
    similarities = {
        'basic': calculate_basic_info_similarity(profile1, profile2),
        'professional': calculate_professional_similarity(profile1, profile2),
        'interests': calculate_interests_similarity(profile1, profile2),
        'lifestyle': calculate_lifestyle_similarity(profile1, profile2)
    }
    
    overall_similarity = sum(similarities[k] * weights[k] for k in weights)
    return round(overall_similarity, 2)

def process_profiles():
    """处理所有档案并计算相似度矩阵"""
    # 读取数据
    with open('results.json', 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    
    n = len(profiles)
    similarity_matrix = np.zeros((n, n))
    names = []
    
    # 获取所有用户名
    for profile in profiles:
        full_name = f"{profile['profile']['basicPersonalInformation']['fullName']['firstName']} {profile['profile']['basicPersonalInformation']['fullName']['lastName']}"
        names.append(full_name)
    
    # 计算相似度矩阵
    for i in range(n):
        for j in range(n):
            similarity = calculate_overall_similarity(profiles[i]['profile'], profiles[j]['profile'])
            similarity_matrix[i][j] = similarity
    
    return names, similarity_matrix.tolist()

# 主处理流程
if __name__ == "__main__":
    names, similarity_matrix = process_profiles()
    
    # 保存结果
    result = {
        "timestamp": datetime.now().isoformat(),
        "names": names,
        "similarity_matrix": similarity_matrix
    }
    
    with open('similarity_results.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("相似度计算完成，结果已保存到 similarity_results.json")