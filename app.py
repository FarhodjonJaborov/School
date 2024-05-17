import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Загрузка данных
data = pd.read_csv('students_recommendations_with_materials_and_professions.csv')

# Функции для рекомендаций
def find_closest_matches(interest, interests_list, threshold=80):
    matches = process.extract(interest, interests_list, scorer=fuzz.partial_ratio)
    return [match for match, score in matches if score >= threshold]

def recommend_study_materials(user_data, data):
    recommendations = []
    all_interests = data['Интересы'].str.split(', ').explode().unique()

    interests = user_data['Интересы'].split(', ')
    for interest in interests:
        matched_rows = data[data['Интересы'].str.contains(interest, case=False, na=False)]
        if not matched_rows.empty:
            for _, row in matched_rows.iterrows():
                recommendations.extend(row['Рекомендации по учебным материалам'].split(', '))
        else:
            close_matches = find_closest_matches(interest, all_interests)
            if close_matches:
                for match in close_matches:
                    matched_rows = data[data['Интересы'].str.contains(match, case=False, na=False)]
                    for _, row in matched_rows.iterrows():
                        recommendations.extend(row['Рекомендации по учебным материалам'].split(', '))

    return ', '.join(set(recommendations))

def recommend_profession(user_data, data):
    recommendations = []
    all_interests = data['Интересы'].str.split(', ').explode().unique()

    interests = user_data['Интересы'].split(', ')
    for interest in interests:
        matched_rows = data[data['Интересы'].str.contains(interest, case=False, na=False)]
        if not matched_rows.empty:
            for _, row in matched_rows.iterrows():
                recommendations.extend(row['Рекомендации по профессиям'].split(', '))
        else:
            close_matches = find_closest_matches(interest, all_interests)
            if close_matches:
                for match in close_matches:
                    matched_rows = data[data['Интересы'].str.contains(match, case=False, na=False)]
                    for _, row in matched_rows.iterrows():
                        recommendations.extend(row['Рекомендации по профессиям'].split(', '))

    return ', '.join(set(recommendations))

# Создание приложения Streamlit
st.title('Рекомендательная система для студентов')

st.header('Введите свои данные')
age = st.number_input('Возраст', min_value=10, max_value=100, value=18)
gender = st.selectbox('Пол', ['Мужской', 'Женский'])
interests = st.text_input('Интересы (разделяйте запятой)', 'Философия, Информатика')
knowledge_level = st.selectbox('Уровень знаний', ['Низкий', 'Средний', 'Высокий'])
learning_style = st.text_input('Стиль обучения (разделяйте запятой)', 'Визуальный, Кинестетический')
learning_goals = st.text_input('Цели обучения', 'Понять основы биологии')

# Собираем данные пользователя
user_data = {
    'Возраст': age,
    'Пол': gender,
    'Интересы': interests,
    'Уровень знаний': knowledge_level,
    'Стиль обучения': learning_style,
    'Цели обучения': learning_goals
}

if st.button('Получить рекомендации'):
    study_materials = recommend_study_materials(user_data, data)
    professions = recommend_profession(user_data, data)
    st.header('Ваши рекомендации')
    st.subheader('Учебные материалы:')
    st.write(study_materials if study_materials else "Не найдено подходящих учебных материалов.")
    st.subheader('Профессии:')
    st.write(professions if professions else "Не найдено подходящих профессий.")


print("hello world")