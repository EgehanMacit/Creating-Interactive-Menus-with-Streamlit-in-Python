import streamlit as st
import requests as req

url = "https://dummyjson.com/recipes?limit=0"

def fetch_recipes():
    response = req.get(url)
    if response.ok:  # Eğer istek başarılı ise, status kodu 2xx veya 3xx ise
        return response.json()['recipes']


def app():
    st.title("Tarifler Uygulaması")
    # Tarifleri çek
    recipes = fetch_recipes()
    if recipes:
        with st.sidebar:
            st.subheader("Filtreler")
            # Burada filtreleme seçenekleri eklenecektir.
            kelime = st.text_input("Tarif Adında Ara", placeholder="Tarif adı girin")
            if kelime:
                recipes = [recipe for recipe in recipes if kelime.lower() in recipe['name'].lower()]

            mutfaklar = {recipe['cuisine'] for recipe in recipes}
            cuisine = st.selectbox("Mutfak Türü", ["Tüm Mutfaklar"] + sorted(list(mutfaklar)))
            if cuisine != "Tüm Mutfaklar":
                recipes = [recipe for recipe in recipes if recipe['cuisine'] == cuisine]

            meal_types = set()
            for recipe in recipes:
                for meal_type in recipe['mealType']:
                    meal_types.add(meal_type)
            meal_type = st.multiselect("Öğün Türü", sorted(list(meal_types)))
            if meal_type:
                recipes = [recipe for recipe in recipes if any(mt in recipe['mealType'] for mt in meal_type)]
        # Tarifleri listele
        for recipe in recipes:
            with st.container(border=True):
                cols = st.columns((1, 3))
                with cols[0]:
                    st.image(recipe['image'], use_container_width=True)
                with cols[1]:
                    st.subheader(recipe['name'])
                    st.write("**Cuisine:**", recipe['cuisine'])
                    st.write("**Meal Type:**", ", ".join(recipe['mealType']))
                    st.write("**Tags:**", ", ".join(recipe['tags']))
    else:
        st.error("Tarifler alınamadı.")


if __name__ == "__main__":
    app()