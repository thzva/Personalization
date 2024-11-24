**By encoding the Summary and analyzing the diversity, it seems good.**<br>
result: embedding_viz.png<br>
code:tsne_summary.py<br>

**avg / stddev of similarity score**
result: category_ratios.png ratios.json<br>
code:avg_stddev.py<br>
1.	高比率（大于2或3）<br>
	•	如果比率高于2或3（如图中某些类别），说明该类别的特征或行为在数据中相对集中。这意味着：<br>
	•	数据点之间的差异较小。<br>
	•	该类别可能在用户群体中具有普遍性或一致性。<br>
2.	低比率（小于1或接近1）<br>
	•	如果比率接近或小于1（如图中的“media consumption and engagement”），说明该类别的特征或行为在数据中较为分散。这意味着：<br>
	•	数据点之间的差异较大。<br>
	•	该类别可能表现出更多的个体化或随机性。
3.	中等比率（介于1和2之间）<br>
	•	如果比率在1到2之间，则表明数据既不完全一致，也不是完全分散。这通常是大多数现实数据的分布特征。<br>
1.	High Ratio (Greater than 2 or 3)<br>
	•	If the ratio is greater than 2 or 3 (as seen in some categories in the chart), it indicates that the characteristics or behaviors of this category are relatively concentrated in the data. This means:<br>
	•	The differences between data points are smaller.<br>
	•	This category may exhibit universality or consistency among the user group.<br>
2.	Low Ratio (Less than or Close to 1)<br>
	•	If the ratio is close to or less than 1 (such as “media consumption and engagement” in the chart), it indicates that the characteristics or behaviors of this category are relatively dispersed in the data. This means:<br>
	•	The differences between data points are larger.<br>
	•	This category may demonstrate more individuality or randomness.<br>
3.	Moderate Ratio (Between 1 and 2)<br>
	•	If the ratio is between 1 and 2, it suggests that the data is neither completely consistent nor entirely dispersed. This is typically the distribution characteristic of most real-world data.<br>



**Mikael Jansson does not have hobbies_interests_and_lifestyle.**<br>
**Last time's abnormal data**<br>
*Alma Kodra and Callum Le Page*<br>
data: abnormal_samples.json<br>
previous result: tsne.png<br>
Why:<br>
这两个用户在一些关键维度上确实有相似之处：<br>
    两者都注重文化探索和学习新事物<br>
    都有较高的同理心水平<br>
    都重视家庭关系和稳定的社交网络<br>
    工作风格都倾向于合作和平衡<br>
    都喜欢户外活动和烹饪<br>
在t-SNE可视化中重合的原因：<br>
    嵌入向量主要捕捉了用户的行为模式和价值观，而不是具体的人口统计特征<br>
    我们的权重设置给予心理认知(0.15)、爱好兴趣(0.15)和核心价值观(0.15)较高权重，这些维度上两人比较接近<br>
    t-SNE算法在降维过程中可能过度强调了这些相似性<br>
These two users do indeed share similarities across several key dimensions:<br>
Both are focused on cultural exploration and learning new things.  <br>
Both exhibit high levels of empathy.  <br>
Both value family relationships and a stable social network.<br>  
Their work styles lean toward collaboration and balance. <br> 
Both enjoy outdoor activities and cooking.<br>  
Reasons for overlap in the t-SNE visualization:<br>
The embedding vectors primarily capture users’ behavioral patterns and values, rather than specific demographic features.  <br>
Our weighting configuration places higher emphasis on psychological cognition (0.15), hobbies and interests (0.15), and core values (0.15), dimensions where these two users are closely aligned. <br>  
The t-SNE algorithm may have overly emphasized these similarities during the dimensionality reduction process. <br> 



**Combine each user's hobbies_interests_and_lifestyle into one section and examine how many different hobbies_interests_and_lifestyle categories exist.**<br>
code: calculate_summarized_hobbies.py<br>
result: <br>
*similarity_threshold = 0.85*<br>
Total number of unique interests: 89<br>
Users with similar interests:<br>
Alexandria Petrov is similar to: Jamila Lake<br>
Arianne Chin is similar to: Andrea Salazar<br>
Chloé Desiré is similar to: Aminata Diallo<br>
Alexis Montalván is similar to: Ixel Amador<br>
Andrea Meier is similar to: Jamila Lake<br>
Olav Larsen is similar to: Callum Le Page, Alma Kodra, Ayu Kadir<br>
Fatima Mahamat is similar to: Aminata Diallo<br>
Alexios Papadimitriou is similar to: Luca Bianchi, Jean-Pierre Mbokani<br>
Callum Le Page is similar to: Alma Kodra, Ayu Kadir<br>
Alma Kodra is similar to: Ayu Kadir<br>
Oleksandr Petrovych is similar to: Vincent Browne<br>
*similarity_threshold = 0.9*<br>
Total number of unique interests: 91<br>
Users with similar interests:<br>
Andrea Meier is similar to: Jamila Lake<br>
Olav Larsen is similar to: Callum Le Page, Alma Kodra, Ayu Kadir<br>
Callum Le Page is similar to: Alma Kodra, Ayu Kadir<br>
Alma Kodra is similar to: Ayu Kadir<br>




**Data Error:**<br>
*test.py calculate all of the characteristics in generated_user_profiles.json*<br>

*The “hobbies_interests_and_lifestyle” samples and documentation are significantly mismatched.*<br>

These data points should be categorized under “lifestyle_and_daily_routine” as the primary header:<br>
lifestyle_and_daily_routine.dietary_patterns<br>
lifestyle_and_daily_routine.morning_and_evening_routines<br>
lifestyle_and_daily_routine.sleep_patterns<br>

hobbies_interests_and_lifestyle.animal_and_pet_interests.dog_cat_walking<br>
hobbies_interests_and_lifestyle.animal_and_pet_interests.pet_care<br>
hobbies_interests_and_lifestyle.collecting.art_or_antiques<br>
hobbies_interests_and_lifestyle.cooking_and_culinary_interests.baking<br>
hobbies_interests_and_lifestyle.cooking_and_culinary_interests.cooking<br>
hobbies_interests_and_lifestyle.cooking_and_culinary_interests.food_exploration<br>
hobbies_interests_and_lifestyle.creative_arts.crafts_and_diy<br>
hobbies_interests_and_lifestyle.creative_arts.music<br>
hobbies_interests_and_lifestyle.creative_arts.performing_arts<br>
hobbies_interests_and_lifestyle.creative_arts.visual_arts<br>
hobbies_interests_and_lifestyle.creative_arts.writing<br>
hobbies_interests_and_lifestyle.fashion_and_personal_style.fashion_preferences<br>
hobbies_interests_and_lifestyle.fashion_and_personal_style.trends_and_innovation<br>
hobbies_interests_and_lifestyle.food_exploration<br>
hobbies_interests_and_lifestyle.intellectual_pursuits.learning_new_skills<br>
hobbies_interests_and_lifestyle.intellectual_pursuits.puzzles_and_games<br>
hobbies_interests_and_lifestyle.intellectual_pursuits.reading<br>
hobbies_interests_and_lifestyle.intellectual_pursuits.science_and_tech<br>
hobbies_interests_and_lifestyle.lifestyle_and_daily_routine.dietary_patterns<br>
hobbies_interests_and_lifestyle.lifestyle_and_daily_routine.morning_and_evening_routines<br>
hobbies_interests_and_lifestyle.lifestyle_and_daily_routine.sleep_patterns<br>
hobbies_interests_and_lifestyle.outdoor_and_nature_activities.environmental_conservation<br>
hobbies_interests_and_lifestyle.outdoor_and_nature_activities.gardening<br>
hobbies_interests_and_lifestyle.outdoor_and_nature_activities.hiking/camping<br>
hobbies_interests_and_lifestyle.outdoor_and_nature_activities.hiking_camping<br>
hobbies_interests_and_lifestyle.outdoor_and_nature_activities.wildlife_observation<br>
hobbies_interests_and_lifestyle.personal_development.mindfulness/meditation<br>
hobbies_interests_and_lifestyle.personal_development.mindfulness_meditation<br>
hobbies_interests_and_lifestyle.personal_development.personal_growth<br>
hobbies_interests_and_lifestyle.personal_development.spiritual_practices<br>
hobbies_interests_and_lifestyle.social_entertainment.cultural_festivals<br>
hobbies_interests_and_lifestyle.social_entertainment.live_shows<br>
hobbies_interests_and_lifestyle.social_entertainment.social_gatherings<br>
hobbies_interests_and_lifestyle.sports_and_fitness.outdoor_fitness<br>
hobbies_interests_and_lifestyle.sports_and_fitness.sports_participation<br>
hobbies_interests_and_lifestyle.sports_and_fitness.yoga/pilates<br>
hobbies_interests_and_lifestyle.sports_and_fitness.yoga_pilates<br>
hobbies_interests_and_lifestyle.travel_and_exploration.cultural_exploration<br>
hobbies_interests_and_lifestyle.travel_and_exploration.eco_tourism<br>
hobbies_interests_and_lifestyle.travel_and_exploration.travel_with_family_friends<br>
hobbies_interests_and_lifestyle.volunteer_and_social_impact.activism<br>
hobbies_interests_and_lifestyle.volunteer_and_social_impact.community_service<br>
