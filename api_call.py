import openai

def tts_api_call(prompt, voice, api_key, file_folder, file_name, model="tts-1", format=".mp3") -> None:
    """ Takes in user prompt, desired voice, and filepath, makes an API call to the openAI text to speech model.
    Saves the result to the desired filepath."""
    client = openai.OpenAI(api_key=api_key)
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=prompt
    )
    file_path = f"{file_folder}/{file_name}{format}"
    response.stream_to_file(file_path)
    return None


if __name__ == "__main__":
    ...