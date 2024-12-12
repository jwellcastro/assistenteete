import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from flask import Flask, request, jsonify
from nltk.data import find
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Função para verificar e baixar pacotes do NLTK
def download_package(package):
    try:
        find(f"corpora/{package}")
    except LookupError:
        nltk.download(package)

# Baixar apenas se necessário
download_package('stopwords')
download_package('punkt')

# Função para pré-processar (limpeza) texto
def preprocess_text(text):
    stop_words = set(stopwords.words('portuguese'))
    tokens = word_tokenize(text.lower())
    filtered_words = [word for word in tokens if word.isalnum() and word not in stop_words]
    return " ".join(filtered_words)

#tratamento de erros
# Carregar o banco de dados (Excel)
try:
    faq_data = pd.read_excel("perguntas_assistente_ete.xlsx")
    print("Colunas disponíveis no arquivo Excel:", faq_data.columns)
except FileNotFoundError:
    print("Erro: O arquivo 'perguntas_assistente_ete.xlsx' não foi encontrado.")
    exit()

# Verificar se as colunas esperadas estão presentes
required_columns = ['Pergunta', 'Resposta']
if not all(col in faq_data.columns for col in required_columns):
    print(f"Erro: O arquivo Excel deve conter as colunas {required_columns}.")
    exit()

# Pré-processar as perguntas no arquivo Excel
faq_data['Pergunta_Processed'] = faq_data['Pergunta'].apply(preprocess_text)

# Criar modelo TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(faq_data['Pergunta_Processed'])

# Função para encontrar a melhor resposta
def get_best_response(user_input):
    user_input_processed = preprocess_text(user_input)
    user_vector = vectorizer.transform([user_input_processed])
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix)
    max_score_index = similarity_scores.argmax()
    max_score = similarity_scores[0, max_score_index]

    # Limite de similaridade para respostas relevantes
    if max_score >= 0.1:  # Ajuste conforme necessário
        return faq_data.iloc[max_score_index]['Resposta']
    else:
        return "Desculpe, não entendi sua pergunta. Pode reformular?"

# API usando Flask
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message or not isinstance(user_message, str):
        return jsonify({"response": "Mensagem inválida"}), 400

    response = get_best_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
