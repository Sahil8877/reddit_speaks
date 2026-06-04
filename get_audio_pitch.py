import modules



def get_pitch_value(caption_list):
    audio_pitch_list = []
    for i in range(len(caption_list)):
        pitch = modules.ollama.generate(
            model='llava:13b',
            prompt=f"""
            You are a strict integer output system.

            Image description: "{caption_list[i]}"

            Based on this description, choose a single integer pitch (in Hertz) for a calm, pleasant, audible sine wave.
            - Calm/peaceful scenes → low pitches 
            - Neutral/everyday scenes → medium pitches 
            - Energetic/awe‑inspiring scenes → higher but still pleasant
            - Never exceed 3000 Hz (would be harsh)

            Output ONLY the integer pitch. No words, no units, no punctuation.""",
            options={'temperature': 0.3}
        )
        try:
            output_pitch = int(pitch['response'])
        except:
            output_pitch = 440 ##added a fallback value if llm fails to give single integer pitch value
        audio_pitch_list.append(output_pitch)
        print(f"FOR IMAGE : {caption_list[i]} | PITCH VALUE RECIEVED : ",output_pitch)
    return audio_pitch_list

