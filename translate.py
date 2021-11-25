""" from google.cloud import translate

def translate_text(text="Hello, world!", project_id="clever-airship-332610"):

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate(text,target_language = target)

    for translation in response.translations:
        print("Translated text: {}".format(translation.translated_text)) """

def translate_text(text = "Hallo, das Welt!"):

    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language='en')

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


translate_text("A čistý záchody, to mám rád!")
