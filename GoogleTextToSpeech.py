from google.cloud import texttospeech
from datetime import datetime
from google.oauth2 import service_account

class GoogleTextToSpeech:

    def __init__(self):
        # set credentials
        self.credentials = service_account.Credentials.from_service_account_file('key/key.json')

        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient(credentials=self.credentials)

    def synthesize(self, text, filename ="output"):
        """Synthesizes speech from the input string of text or ssml.

        Note: ssml must be well-formed according to:
            https://www.w3.org/TR/speech-synthesis/
        """

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        output = self.output_path_generator(filename)

        # The response's audio_content is binary.
        with open(output, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file "{output}"')

    def synthesize_with_audio_profile(self, text, effects_profile_id, filename="output"):
        """Synthesizes speech from the input string of text."""

        input_text = texttospeech.SynthesisInput(text=text)

        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        voice = texttospeech.VoiceSelectionParams(language_code="en-US")

        # Note: you can pass in multiple effects_profile_id. They will be applied
        # in the same order they are provided.
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            effects_profile_id=[effects_profile_id],
        )

        response = self.client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        output = self.output_path_generator(filename)

        # The response's audio_content is binary.
        with open(output, "wb") as out:
            out.write(response.audio_content)
            print('Audio content written to file "%s"' % output)


    def list_voices(self):
        """Lists the available voices."""

        # Performs the list voices request
        voices = self.client.list_voices()

        for voice in voices.voices:
            # Display the voice's name. Example: tpc-vocoded
            print(f"Name: {voice.name}")

            # Display the supported language codes for this voice. Example: "en-US"
            for language_code in voice.language_codes:
                print(f"Supported language: {language_code}")

            ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

            # Display the SSML Voice Gender
            print(f"SSML Voice Gender: {ssml_gender.name}")

            # Display the natural sample rate hertz for this voice. Example: 24000
            print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

    def output_path_generator(self, filename):
        timestamp = datetime.now().strftime("%b-%d-%Y_%H-%M-%S")
        output = f"output/{filename}-{timestamp}.mp3"
        return output
