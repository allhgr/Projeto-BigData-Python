import requests
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
    

def produto_por_categoria(categoria):
    categoria_api = {
        'Eletrônicos': 'electronics',
        'Joalheria': 'jewelery',
        'Roupas Masculinas': "men's clothing",
        'Roupas Femininas': "women's clothing"
    }

    url = f'https://fakestoreapi.com/products/category/{categoria_api[categoria]}'
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        # Traduzindo colunas para português
        df = df.rename(columns={'title': 'Título', 'price': 'Preço'})
        
        # Extraindo rate e count para colunas separadas e removendo coluna 'rating' se não for mais necessária
        df['Avaliação'] = df['rating'].apply(lambda x: x['rate'])
        df['Qtd'] = df['rating'].apply(lambda x: x['count'])
        df = df.drop(columns=['rating'])
        
        # Formatação das colunas
        df['Preço BRL'] = df['Preço'].apply(lambda x: f'R$ {x:,.2f}')
        df['Avaliação'] = df['Avaliação'].apply(lambda x: f'{x:,.2f} ☆')

        return df
    else:
        st.error("Erro ao acessar a API")
        return None


def salvar_e_calcular(df):

    # Gerar custos aleatórios (Entre 60% e 80%) e calculo do lucro
    np.random.seed(42)
    df['Custo'] = df['Preço'] * np.random.uniform(0.6, 0.8, size=len(df))
    df['Lucro'] = df['Preço'] - df['Custo']
    df['Produto'] = df['Título'].apply(lambda x: x[:15])
    
    # Visualizar vendas por produto em gráfico com barras
    st.write("### Gráfico de Vendas por Produto (Preços)")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Produto', y='Preço', data=df, ax=ax)
    plt.xticks(rotation=15)
    st.pyplot(fig)

    # Formatação dos valores numéricos para duas casas decimais
    df['Preço'] = df['Preço'].apply(lambda x: f'R$ {x:,.2f}')
    df['Custo'] = df['Custo'].apply(lambda x: f'R$ {x:,.2f}')
    df['Lucro'] = df['Lucro'].apply(lambda x: f'R$ {x:,.2f}')
    
    # Criação de um array de dicionários com os dados formatados
    produtos_array = df[['Título', 'Preço', 'Custo', 'Lucro']].to_dict(orient='records')

    # Exibir DataFrame no app com Título, Preço, Custo e Lucro
    st.write("### Tabela com Vendas (Preço), Custo e Lucro")
    st.dataframe(df[['Título', 'Preço', 'Custo', 'Lucro']])

    return produtos_array


def main():
    st.title("Análise de Produtos por Categoria")

    categorias = ['Eletrônicos', 'Joalheria', 'Roupas Masculinas', 'Roupas Femininas']
    categoria = st.selectbox("Escolha uma categoria", categorias)
    produtos_categoria = produto_por_categoria(categoria)
    
    # Exibindo algumas opções de produtos da categoria
    if produtos_categoria is not None:
        st.write(f"### Produtos da categoria '{categoria}':")
        st.dataframe(produtos_categoria[['Título', 'Preço BRL', 'Avaliação', 'Qtd']].head())  
        
        # Opção ao usuário para salvar os dados e calcular lucro
        if st.button("Calcular Lucro e Exibir Gráfico"):
            salvar_e_calcular(produtos_categoria)

if __name__ == "__main__":
    main()
