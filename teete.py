import os
import openai

openai.api_key = "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"
messages=[{
      "role": "system",
      "content": "You're now a diet chatbot"
    },
    {
      "role": "user",
      "content": "If the user tells me the food I ate today, calories, nutrients, and the standard of daily video intake, I need to recommend the next food I will eat accordingly. Also, please recommend a diet according to the current time\nThe five conditions must be determined comprehensively. [Except for allergies and foods you don't like,If the nutritional intake standard is exceeded, low-nutritive food is recommended if the nutrient content is insufficient, high-nutritive food is recommended, and all nutrients are comprehensively determined]\nFirst, I'll tell you the standard of video intake per day [{\"kcal\": 1500.0, \"protein\": 55.0, \"fat\": 54.0, \"glucide\": 324.0, \"sugar\": 100.0, \"dietaryfiber\": 25.0, \"calcium\": 700.0, \"Iron\": 12.0, \"magnesium\": 315, \"caffeine\": 0, \"Potassium\": 3500.0, \"Natrium\": 2000.0, \"vitamin\": 0.0, \"cholesterol\": 300.0, \"fatty\": 0.0, \"transfat\": 0}]\nThen I'll tell you what the user ate today. [햄버거,마라탕,바나나킥] And the total calories and nutrients that I ate today are\n{\"kcal\": 500.0, \"protein\": 60.0, \"fat\": 5.0, \"glucide\": 10.0, \"sugar\": 15.0, \"dietaryfiber\": 0.0, \"calcium\": 0.0, \"Iron\": 0.0, \"magnesium\": 0, \"caffeine\": 0, \"Potassium\": 0.0, \"Natrium\": 45.0, \"vitamin\": 0.0, \"cholesterol\": 0.0, \"fatty\": 0.0, \"transfat\": 0} It's 18 o'clock now Allergy is[우유,밀가루,콩,샐러리], food I hate is[피망,짜장면,상추]\nAs for the output format, the current time is 18:00, so let's consider dinner. Here are some of the options that are appropriate for your diet:\n\n1. Grilled chicken breast salad: Chicken breast is known as a low-fat, high-protein food. If you eat it as a salad with fresh vegetables, you can get various nutrients.\n\n2. Noodles: Noodles are high in carbohydrates, and when eaten with vegetables, they help you get nutrients. However, you should be careful because you are allergic to flour.\n\n3. Fish Cuisine: Fish is known as a low-fat, high-protein food. You can get healthy nutrients if you grill it or eat it in an oven.\n\n4. Soybean dishes: Soybeans are healthy because they are rich in vegetable protein and dietary fiber. You can eat it in various ways, such as bean sprouts and braised beans.\n\nPlease let me know if you want to choose from these or if you need any other food recommendations.\nFrom now on, only when the user asks about the diet, \"Only list with the diet and reason and recommend 3 or 4 of them\" and \"Unconditionally print it within 200 characters.\" Print out in Korean"
    },
    {
      "role": "assistant",
      "content": "yes"
    }]
while True:
    content=input("User: ")
    messages.append({"role": "user","content": content})
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages,
    temperature=0,
    max_tokens=538,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    chat_response=response.choices[0].message.content
    print(chat_response)
    messages.append({"role": "assistant","content": chat_response})