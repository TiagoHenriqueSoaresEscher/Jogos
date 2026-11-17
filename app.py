#Usa este codigo pra executar o app: uvx streamlit run app.py
import streamlit as st

# Configuração da pagina
st.set_page_config(
    page_title="Meu Catalogo de Jogos",
    page_icon="🎮",
    layout="wide"
)

# Tema preto com detalhes roxos
st.markdown("""
<style>
.stApp {
    background-color: #080808;
    color: white;
}

[data-testid="stHeader"] {
    background-color: #080808;
}

h1, h2, h3, p, label {
    color: white;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button {
    background-color: #9146ff;
    color: white;
    border: none;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #772ce8;
    color: white;
    border-color: #9146ff;
}

div[data-testid="stMetric"] {
    background-color: #191919;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #333333;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #333333;
}
</style>
""", unsafe_allow_html=True)


# Lista para guardar os jogos
if "jogos" not in st.session_state:
    st.session_state.jogos = []


# Funcao para cadastrar um jogo
def cadastrar_jogo(nome, genero, plataforma, nota):
    jogo = {
        "nome": nome,
        "genero": genero,
        "plataforma": plataforma,
        "nota": nota
    }

    st.session_state.jogos.append(jogo)


# Titulo do site
st.title("🎮 Meu Catalogo de Jogos")
st.write("Cadastre, pesquise e avalie seus jogos favoritos!")

st.divider()

# Criando as abas
aba1, aba2, aba3 = st.tabs([
    "➕ Cadastrar",
    "🎮 Meus Jogos",
    "📊 Estatisticas"
])


# ABA 1 - CADASTRAR
with aba1:

    st.subheader("Cadastrar novo jogo")

    with st.form("formulario_jogo", clear_on_submit=True):

        nome = st.text_input("Nome do jogo")

        genero = st.selectbox(
            "Genero",
            [
                "Ação",
                "Aventura",
                "Terror",
                "Corrida",
                "RPG",
                "Simulção",
                "Esportes",
                "Estrategia",
                "Outros"
            ]
        )

        plataforma = st.selectbox(
            "Plataforma",
            [
                "PC",
                "PlayStation",
                "Xbox",
                "Nintendo Switch",
                "Celular",
                "Outros"
            ]
        )

        nota = st.slider(
            "Sua nota para o jogo",
            0, 10, 5
        )

        salvar = st.form_submit_button(
            "Salvar jogo",
            type="primary"
        )

    if salvar:

        if nome.strip() == "":
            st.warning("Digite o nome do jogo!")

        else:
            cadastrar_jogo(
                nome.strip(),
                genero,
                plataforma,
                nota
            )

            st.success("Jogo cadastrado com sucesso!")


# ABA 2 - MEUS JOGOS
with aba2:

    st.subheader("Meus jogos cadastrados")

    pesquisa = st.text_input(
        "🔎 Pesquisar pelo nome"
    )

    filtro = st.selectbox(
        "Filtrar por genero",
        [
            "Todos",
            "Ação",
            "Aventura",
            "Terror",
            "Corrida",
            "RPG",
            "Simulação",
            "Esportes",
            "Estrategia",
            "Outros"
        ]
    )

    encontrados = []

    # Procurando jogos na lista
    for indice, jogo in enumerate(st.session_state.jogos):

        nome_combina = (
            pesquisa.lower() in jogo["nome"].lower()
        )

        genero_combina = (
            filtro == "Todos"
            or jogo["genero"] == filtro
        )

        if nome_combina and genero_combina:
            encontrados.append((indice, jogo))

    st.write("Jogos encontrados:", len(encontrados))

    if len(encontrados) == 0:
        st.info("Nenhum jogo encontrado.")

    else:

        for indice, jogo in encontrados:

            with st.container(border=True):

                coluna1, coluna2 = st.columns([4, 1])

                with coluna1:

                    st.subheader("🎮 " + jogo["nome"])

                    st.write("Genero:", jogo["genero"])

                    st.write("Plataforma:", jogo["plataforma"])

                    st.write("⭐ Nota:", jogo["nota"], "/ 10")

                with coluna2:

                    if st.button(
                        "🗑️ Excluir",
                        key="excluir_" + str(indice)
                    ):

                        st.session_state.jogos.pop(indice)

                        st.rerun()


# ABA 3 - ESTATISTICAS
with aba3:

    st.subheader("Estatisticas do catalogo")

    total = len(st.session_state.jogos)

    soma_notas = 0

    for jogo in st.session_state.jogos:
        soma_notas += jogo["nota"]

    if total > 0:
        media = soma_notas / total
    else:
        media = 0

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        st.metric("🎮 Total de jogos", total)

    with coluna2:
        st.metric("⭐ Media das notas", f"{media:.1f}/10")

    st.divider()

    if total > 0:

        st.subheader("Jogos por genero")

        generos = {}

        for jogo in st.session_state.jogos:

            genero = jogo["genero"]

            if genero in generos:
                generos[genero] += 1
            else:
                generos[genero] = 1

        st.bar_chart(generos)

    else:
        st.info("Cadastre jogos para visualizar estatisticas.")
