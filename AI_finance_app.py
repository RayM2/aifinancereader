import streamlit as st
import pandas as pd
import openai

# Set your OpenAI API key here
openai.api_key = 'your-api-key'

def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error: {e}")
            return None
    return None

def generate_financial_context(data):
    if data is not None and isinstance(data, pd.DataFrame):
        # Calculate total monthly expenses
        total_expenses = data.sum(axis=1).mean()  # Assuming each row represents a month

        # Find the highest spending category
        highest_spending_category = data.sum().idxmax()

        # Generate the dynamic context summary
        context_summary = f"Total monthly expenses: ${total_expenses:.2f}. Highest spending: {highest_spending_category}."
        return context_summary
    else:
        return "Invalid or missing financial data."

def ask_openai(question, financial_context):
    try:
        full_prompt = (
            "As a financial advisor, I help manage expenses and predict future costs "
            "based on current spending patterns. I offer advice on whether financial decisions "
            "are sound and suggest improvements.\n\n"
            f"Financial Summary: {financial_context}\n"
            f"Question: {question}\nAnswer:"
        )

        response = openai.Completion.create(
            engine="text-davinci-003",  
            prompt=full_prompt,
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    st.title("Personal AI Finance Advisor")

    uploaded_file = st.file_uploader("Upload your Excel file", type="xlsx")
    data_context = ""
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        if data is not None:
            st.write("Data from your Excel file:")
            st.write(data)
            data_context = generate_financial_context(data)

    user_question = st.text_input("Ask a financial advice question:")
    if user_question and data_context:
        openai_response = ask_openai(user_question, data_context)
        st.text_area("OpenAI Response:", openai_response, height=150)

if __name__ == "__main__":
    main()
