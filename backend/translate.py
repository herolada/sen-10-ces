def translate_text(text = "Hallo, das Welt!"):

    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language='en')

    return(result["translatedText"])