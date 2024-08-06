import spacy

def extract_top_words(phrase, top_words_number=3):
    nlp = spacy.load('it_core_news_sm')
    doc = nlp(phrase)

    word_scores = {}
    for token in doc:
        if not token.is_punct and not token.is_stop and len(token.text) >= 3:
            word_scores[token.text] = token.rank

    words_sorted_by_score = sorted(word_scores, key=word_scores.get, reverse=True)
    extracted_top_words = words_sorted_by_score[:top_words_number]

    return extracted_top_words
