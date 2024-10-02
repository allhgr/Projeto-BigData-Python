import requests
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

class Graficos:
    def __init__(self, df):
        self.df = df

    def grafico_precos_custos_lucros(self):
        fig, ax = plt.subplots(figsize=(12, 6))

        # Posicionamento e Largura das Barras
        bar_width = 0.25
        index = np.arange(len(self.df['Produto']))

        # Criando as barras
        barra1 = ax.bar(index, self.df['Preço'], bar_width, label='Preço', color='skyblue')
        barra2 = ax.bar(index + bar_width, self.df['Custo'], bar_width, label='Custo', color='coral')
        barra3 = ax.bar(index + 2 * bar_width, self.df['Lucro'], bar_width, label='Lucro', color='palegreen')

        # Adicionando rótulos e título
        self.df['Produto'] = self.df['Produto'].apply(lambda x: x[:20])
        ax.set_xlabel('Produto')
        ax.set_ylabel('Valores em BRL')
        ax.set_title('Comparação entre Preço, Custo e Lucro')
        ax.set_xticks(index + bar_width)
        ax.set_xticklabels(self.df['Produto'], rotation=15)
        ax.legend()

        # Exibindo os valores em cima de cada barra
        for bar in barra1:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

        for bar in barra2:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

        for bar in barra3:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

        st.pyplot(fig)

def produto_por_categoria(categoria):
    categoria_api = {
        'Eletrônicos': 'electronics',
        'Joalheria': 'jewelery',
        'Roupas Masculinas': "men's clothing",
        'Roupas Femininas': "women's clothing"
    }

    url = f'https://fakestoreapi.com/products/category/{categoria_api[categoria]}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        # Traduzindo colunas para português
        df = df.rename(columns={'title': 'Produto', 'price': 'Preço'})

        # Extraindo 'rate' e 'count' para colunas separadas e removendo a coluna 'rating'
        df['Avaliação'] = df['rating'].apply(lambda x: x['rate'])
        df['Qtd'] = df['rating'].apply(lambda x: x['count'])
        df = df.drop(columns=['rating'])

        # Formatação das colunas
        df['Valor'] = df['Preço'].apply(lambda x: f'R$ {x:,.2f}')
        df['Avaliação'] = df['Avaliação'].apply(lambda x: f'{x:,.2f} ☆')
        df['Produto'] = df['Produto'].apply(lambda x: x[:40])

        return df
    else:
        st.error("Erro ao acessar a API")
        return None

def calcular(df):
    np.random.seed(42)
    df['Custo'] = df['Preço'] * np.random.uniform(0.6, 0.8, size=len(df))
    df['Lucro'] = df['Preço'] - df['Custo']
    df['Produto'] = df['Produto'].apply(lambda x: x[:40])
    
    return df

def main():
    st.title("Análise de Produtos por Categoria")
    categorias = ['Eletrônicos', 'Joalheria', 'Roupas Masculinas', 'Roupas Femininas']
    categoria = st.selectbox("Escolha uma categoria", categorias)
    produtos_categoria = produto_por_categoria(categoria)

    if produtos_categoria is not None:
        st.write(f"Produtos da categoria {categoria}:")
        st.dataframe(produtos_categoria[['Produto', 'Valor', 'Avaliação', 'Qtd']].head())  

        if st.button("Tabela com Preço, Custo e Lucro"):
            df_atualizado = calcular(produtos_categoria)
            
            # Formatação dos valores numéricos para duas casas decimais
            df_atualizado['Preço'] = df_atualizado['Preço'].apply(lambda x: f'R$ {x:,.2f}')
            df_atualizado['Custo'] = df_atualizado['Custo'].apply(lambda x: f'R$ {x:,.2f}')
            df_atualizado['Lucro'] = df_atualizado['Lucro'].apply(lambda x: f'R$ {x:,.2f}')
            st.dataframe(df_atualizado[['Produto', 'Preço', 'Custo', 'Lucro']])

        if st.button("Gráfico Preços, Custos e Lucros"):
            df_atualizado = calcular(produtos_categoria)
            graficos = Graficos(df_atualizado)
            graficos.grafico_precos_custos_lucros() 

if __name__ == "__main__":
    main()
