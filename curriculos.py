import streamlit as st
import pypdf
from google import genai
from google.genai import types

# Configuração da página web (Título e Layout)
st.set_page_config(page_title="Analisador de Currículos IA", page_icon="📄", layout="centered")

# Sua chave de API do Gemini
import streamlit as st
API_KEY = st.secrets["AQ.Ab8RN6LHLGRsJyQtqLXgYJZKZ5WeIEG4Zxy71BSKfxq4y6LvQg"]

# Estilo visual moderno via CSS corporativo e rodapé fixo
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #007acc; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; text-align: center; }
    .stButton>button { background-color: #007acc; color: white; border-radius: 8px; width: 100%; font-weight: bold; height: 45px; font-size: 16px; border: none; }
    .stButton>button:hover { background-color: #005a9e; color: white; }
    
    /* Estilo do Rodapé Acadêmico Fixo */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #161b22;
        color: #8b949e;
        text-align: center;
        padding: 12px 0;
        font-size: 13px;
        border-top: 1px solid #21262d;
        font-family: 'Helvetica Neue', sans-serif;
        z-index: 100;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Analisador de Currículos Inteligente")
st.markdown("<p style='text-align: center; color: #8b949e;'>Plataforma inteligente de triagem e análise de perfis profissionais com Inteligência Artificial.</p>", unsafe_allow_html=True)
st.write("---")

# 1. Entrada da Vaga
st.subheader("1. Requisitos da Vaga de Emprego")
texto_vaga = st.text_area(
    "Insira a descrição ou as competências desejadas para a vaga:",
    height=140,
    placeholder="Exemplo: Vaga de Estágio em Administração. Requisitos: Cursando superior, conhecimento em Excel..."
)

# 2. Upload do Currículo (Visual arrastar e soltar muito moderno)
st.subheader("2. Currículo do Candidato")
arquivo_pdf = st.file_uploader("Faça o upload do currículo em formato PDF", type=["pdf"])

# Função para extrair o texto do PDF
def extrair_texto(pdf_file):
    try:
        texto = ""
        leitor = pypdf.PdfReader(pdf_file)
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""
        return texto
    except Exception as e:
        return f"Erro ao ler PDF: {str(e)}"

st.write("") # Espaçador

# 3. Processamento e Exibição do Resultado
if st.button("Iniciar Análise Estruturada"):
    if not texto_vaga:
        st.warning("Por favor, insira a descrição da vaga antes de continuar.")
    elif not arquivo_pdf:
        st.warning("Por favor, selecione ou arraste um arquivo de currículo em PDF.")
    elif API_KEY == "SUA_CHAVE_AQUI":
        st.error("Configure sua chave de API do Gemini na linha 12 para ativar o sistema.")
    else:
        with st.spinner("Efetuando leitura do PDF e gerando parecer técnico..."):
            texto_curriculo = extrair_texto(arquivo_pdf)
            
            try:
                client = genai.Client(api_key=API_KEY)
                
                prompt = (
                    f"Você é um sistema especialista em triagem de currículos e ATS profissional.\n"
                    f"Avalie o currículo fornecido cruzando rigorosamente com os requisitos da vaga.\n\n"
                    f"REQUISITOS DA VAGA:\n{texto_vaga}\n\n"
                    f"CONTEÚDO DO CURRÍCULO:\n{texto_curriculo}\n\n"
                    f"Gere um parecer estruturado exatamente com estes tópicos (use emojis para os tópicos):\n"
                    f"⭐ NOTA DO PERFIL: (Dê uma nota clara de 0 a 10)\n"
                    f"✅ PONTOS FORTES ENCONTRADOS: (Destaque o que ele atende de forma clara)\n"
                    f"❌ GAP TÉCNICO / PONTOS FRACOS: (O que o candidato não mencionou ou falta para a vaga)\n"
                    f"⚖️ PARECER DO RECRUTADOR: (Uma conclusão direta recomendando avançar para entrevista ou descartar)."
                )
                
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                )
                
                st.success("Análise de Perfil Concluída!")
                st.subheader("📋 Relatório de Avaliação Automatizada")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"Falha de comunicação com o motor de IA: {str(e)}")

# Adiciona espaço no final para o conteúdo não sumir atrás do rodapé fixo
st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- RODAPÉ ACADÊMICO FIXO ---
st.markdown("""
    <div class="footer">
        Trabalho desenvolvido para a disciplina de <b>Inteligência Artificial e Tecnologia</b> | Desenvolvido por Diogo Erik © 2026
    </div>
""", unsafe_allow_html=True)
