import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título da aplicação
st.title("Carregar e Filtrar CSV com Interpolação e Visualização Gráfica")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

# Função para verificar a diferença na coluna 3, interpolar e visualizar a coluna 5


def process_columns(file):
    # Lendo o CSV
    df = pd.read_csv(file)

    # Verificando se o arquivo tem pelo menos 5 colunas
    if df.shape[1] >= 5:
        # Extraindo as colunas 3 e 5
        col_3 = df.iloc[:, 2].tolist()
        col_5 = df.iloc[:, 4].tolist()
        col_5_original = col_5.copy()  # Guardando uma cópia da coluna 5 original

        # Inicializando uma lista para armazenar os índices
        indices_maiores_diferenca = []

        # Iterando pelos valores da coluna 3 e verificando a diferença
        for i in range(1, len(col_3)):  # Começando do segundo elemento
            if abs(col_3[i] - col_3[i - 1]) > 1:
                indices_maiores_diferenca.append(i)

        # Realizando a interpolação na coluna 5
        if indices_maiores_diferenca:
            for idx in indices_maiores_diferenca:
                # Se o índice for o primeiro ou último, não pode interpolar
                if idx == 0 or idx == len(col_5) - 1:
                    continue
                # Interpolação simples: média entre o valor anterior e o posterior
                col_5[idx] = (col_5[idx - 1] + col_5[idx + 1]) / 2

            # Plotando o gráfico antes e depois da interpolação
            fig, ax = plt.subplots(figsize=(10, 5))

            ax.plot(range(len(col_5)), col_5, label="Interpolada", marker='x')
            ax.plot([60, 60], [np.min(col_5), np.max(col_5)], '--r')
            ax.plot([120, 120], [np.min(col_5), np.max(col_5)], '--r')
            ax.plot([180, 180], [np.min(col_5), np.max(col_5)], '--r')
            ax.plot([240, 240], [np.min(col_5), np.max(col_5)], '--r')
            ax.set_xlabel("Índice")
            ax.set_ylabel("Valores da Coluna 5")
            ax.set_title("Coluna 5: Original vs Interpolada")
            ax.legend()

            st.pyplot(fig)

            baseline_mean = np.mean(col_5[60:120])
            baseline_std = np.std(col_5[60:120])
            baseline_amplitude = np.max(col_5[60:120]) - np.min(col_5[60:120])

            interval_1_mean = np.mean(col_5[120:180])
            interval_1_std = np.std(col_5[120:180])
            interval_1_amplitude = np.max(
                col_5[120:180]) - np.min(col_5[120:180])

            interval_2_mean = np.mean(col_5[180:240])
            interval_2_std = np.std(col_5[180:240])
            interval_2_amplitude = np.max(
                col_5[180:240]) - np.min(col_5[180:240])

            st.markdown('A análise foi dividida em 3 intervalos: o repouso (entre 1 min e 2 min), o intervalo 1 (entre 2 min e 3 min) e o intervalo 2 (entre 3 min e 4 min). O intervalo 1 está relacionado ao período de contrações fásicas e o intervalo 2 está relacionado ao período da contração voluntária máxima')
            st.text('Dados do repouso')
            st.text("Média do repouso = " + str(baseline_mean))
            st.text("Amplitude do repouso = " + str(baseline_amplitude))
            st.text("Desvio padrão do repouso = " + str(baseline_std))
            st.text('Dados do intervalo 1')
            st.text("Média do intervalo 1 = " + str(interval_1_mean))
            st.text("Desvio padrão do intervalo 1 = " + str(interval_1_std))
            st.text("Amplitude do intervalo 1 = " + str(interval_1_amplitude))
            st.text('Dados do intervalo 2')
            st.text("Média do intervalo 2 = " + str(interval_2_mean))
            st.text("Desvio padrão do intervalo 2 = " + str(interval_2_std))
            st.text("Amplitude do intervalo 2 = " + str(interval_2_amplitude))

        else:
            st.write("Nenhuma diferença maior que 1 foi encontrada.")
    else:
        st.write("O arquivo CSV não possui colunas suficientes.")


# Verificando se o arquivo foi carregado
if uploaded_file is not None:
    process_columns(uploaded_file)
else:
    st.write("Por favor, carregue um arquivo CSV.")
