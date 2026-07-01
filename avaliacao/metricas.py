#!pip install nltk rouge-score sentence-transformers scikit-learn

from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def calcular_bleu(referencia, gerado):
    referencia_tokens = referencia.split()
    gerado_tokens = gerado.split()

    score = sentence_bleu([referencia_tokens], gerado_tokens)
    return score
def calcular_rouge(referencia, gerado):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(referencia, gerado)
    return scores
modelo = SentenceTransformer('all-MiniLM-L6-v2')

def similaridade_semantica(referencia, gerado):
    emb1 = modelo.encode([referencia])
    emb2 = modelo.encode([gerado])

    sim = cosine_similarity(emb1, emb2)[0][0]
    return sim