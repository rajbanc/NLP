import requests
import spacy

from bs4 import BeautifulSoup
import networkx as nx

nlp = spacy.load("en_core_web_sm")

def get_articles(article_links):
	articles = []
	for link in article_links:
	    try:
	        response = requests.get(link)
	        soup = BeautifulSoup(response.content, "html.parser")
	    
	        tag_a = soup.findAll("a", {"class": "ok-post-image"})
	        for a in tag_a:
	            article_link =  a['href']
	            article_soup = BeautifulSoup(requests.get(article_link).content, "html.parser")

	            for tag_p in article_soup.find_all("p"):
	                articles.append(tag_p.text)

	    except Exception  as e:
	        pass
	return articles


def get_sentences(articles):
	sentences = []
	for text in articles:
	    doc = nlp(text)
	    for sent in doc.sents:
	        sentences.append(sent)
	return sentences

def extract_subject_object_relationship(sentence):
    doc = nlp(sentence)
    subject = None
    obj = None
    relationship = None
    for token in doc:
        if "subj" in token.dep_:
            subject = token.text
            relationship = token.dep_
        if "obj" in token.dep_:
            obj = token.text
            relationship = token.dep_
    return (subject, relationship, obj)


def get_answer(question):
    triple = extract_subject_object_relationship(question)
    if triple[0] and triple[2]:
        try:
            path = nx.shortest_path(G, source=triple[0], target=triple[2])
            return path
        except:
            return "No answer found."
    else:
        return 