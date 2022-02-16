from xml.dom.expatbuilder import ParseEscape
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration
import streamlit as st
import torch

def sentiment(text_to_classify):
    if len(text_to_classify) > 0:
        model1 = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        tokenizer1 = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        # torch.save(model1.state_dict(), 'sentiment_model')
        model1.load_state_dict(torch.load('sentiment_model'))

        nlp1 = pipeline("sentiment-analysis", model=model1, tokenizer=tokenizer1)

        classified_text = []
        for i in range(len(text_to_classify)):
      
            sentences = text_to_classify[i]
            results = nlp1(sentences)
            classified_text.append(results[0]['label'])
        return classified_text
    else:
        pass


def summarization(text_to_summarize):
    model_name2 = "human-centered-summarization/financial-summarization-pegasus"
    # tokenizer2 = PegasusTokenizer.from_pretrained(model_name2)
    # tokenizer2.save_pretrained("./models/tokenizer2/")

    tokenizer2 = PegasusTokenizer.from_pretrained("./models/tokenizer2/")
    model2 = PegasusForConditionalGeneration.from_pretrained(model_name2) # If you want to use the Tensorflow model 
    # torch.save(model2.state_dict(), 'summarization_model')
    model2.load_state_dict(torch.load('summarization_model'))
    
    summarized_list = []
    for i in range(len(text_to_summarize)):
        input_ids = tokenizer2(text_to_summarize[i], return_tensors="pt").input_ids

        output = model2.generate(
            input_ids, 
            max_length=32, 
            num_beams=5, 
            early_stopping=True
        )
        out = tokenizer2.decode(output[0], skip_special_tokens=True)

        summarized_list.append(out)
    # sel_col, disp_col = st.column_stack(2)
    # st.text(out)
    return summarized_list


def question_answering(question_to_qa, text_to_qa):
    if len(question_to_qa) > 0:
        model_name_qa = "deepset/roberta-base-squad2"
        model_qa = AutoModelForQuestionAnswering.from_pretrained(model_name_qa)
        tokenizer_qa = AutoTokenizer.from_pretrained(model_name_qa)
        # torch.save(model_qa.state_dict(), 'qa_model')

        model_qa.load_state_dict(torch.load('qa_model'))

        nlp1 = pipeline('question-answering', model=model_qa, tokenizer=tokenizer_qa)

        QA_input = {
            'question': question_to_qa,
            'context': text_to_qa
        }
        res = nlp1(QA_input)
        return st.text(res['answer'])
    else:
        pass