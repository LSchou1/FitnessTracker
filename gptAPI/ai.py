from openai import OpenAI



# OPEN AI
API_KEY = open("API_KEY", "r").read()
client = OpenAI(api_key=API_KEY)

response = client.chat.completions.create(model="ft:gpt-4o-mini-2024-07-18:personal:fitnesstracker1:A5Fzwfzz",
messages=[
        {"role": "system", "content": "You are an assistant that generates structured workout programs."},
        {"role": "user", "content": "lav et upperbody træningsprogram"}
])

print(response.choices[0].message.content)

"""# image
imageResponse = openai.Image.create(
    model="dall-e-3",
    prompt="Lav et billede af Donald trump der poser på ryggen af en Bjørn, Med Michael Bay eksplosioner og kampfly i baggrunden. Manden SKAL ligne Donald trump og have en cigar i munden. Stilen skal være hardcore amerikansk 60'er stil under vietnamkrigen",
    size="1024x1024",
    quality="standard",
    n=1,
)"""

response = {"program": [
                {
                    "exercise": "Pull-Up",
                    "sets": 4,
                    "reps": "10"
                },
                {
                    "exercise": "Bent-Over Barbell Row",
                    "sets": 4,
                    "reps": "12"
                },
                {
                    "exercise": "Single-Arm Dumbbell Row",
                    "sets": 3,
                    "reps": "12"
                },
                {
                    "exercise": "Seated Cable Row",
                    "sets": 3,
                    "reps": "12"
                },
                {
                    "exercise": "Lat Pulldown",
                    "sets": 3,
                    "reps": "12"
                },
                {
                    "exercise": "Face Pull",
                    "sets": 3,
                    "reps": "20"
                }
            ]}

print("test")
#chat_response = response['choices'][0]['message']['content']
#for exercise in response["program"]:
    #print(exercise["exercise"])


# TODO
## lav 10 prompt eksempler til fine tuning - chatten har allerede lavet en, få den til at lave flere
## lav fine tuning


## lav backend i python
### få response JSON format
### træk data ud og print
### gem programmet i sql

## lav frontend
### input prompt til AI
### output content fra AI
### mulighed for at gemme programmet