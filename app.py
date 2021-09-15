from flask import Flask,render_template,url_for,request
import time
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer


nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def lex_summary(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result

def luhn_summary(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	summarizer_luhn = LuhnSummarizer()
	summary_1 =summarizer_luhn(parser.document,3)
	summary_list = [str(sentence) for sentence in summary_1]
	result = ' '.join(summary_list)
	return result


def isa_summary(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	summarizer_lsa = LsaSummarizer()
	summary_2 =summarizer_lsa(parser.document,3)
	summary_list = [str(sentence) for sentence in summary_2]
	result = ' '.join(summary_list)
	return result


# Reading Time
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/process',methods=['GET','POST'])
def process():
    start = time.time()
    if request.method == 'POST':
        input_text = request.form['input_text']
        model_choice = request.form['model_choice']
        final_reading_time = readingTime(input_text)
        if model_choice == 'default':
            final_summary = lex_summary(input_text)
        elif model_choice == 'lex_summarizer':
            final_summary = lex_summary(input_text)
        elif model_choice == 'luhn_summarizer':
            final_summary= luhn_summary(input_text)
        elif model_choice == 'isa_summarizer':
            final_summary= isa_summary(input_text)
    summary_reading_time = readingTime(final_summary)
    end = time.time()
    final_time = end-start
    return render_template('result.html',ctext=input_text,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,final_summary=final_summary,model_selected=model_choice)



from bs4 import BeautifulSoup
# from urllib.request import urlopen
from urllib.request import urlopen

def get_text(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

@app.route('/process_url',methods=['GET','POST'])
def process_url():
	start = time.time()
	if request.method == 'POST':
		input_url = request.form['input_url']
		raw_text = get_text(input_url)
		final_reading_time = readingTime(raw_text)
		final_summary = lex_summary(raw_text)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('result.html',ctext=raw_text,
                        final_summary=final_summary,
                        final_time=final_time,
                        final_reading_time=final_reading_time,
                        summary_reading_time=summary_reading_time)


if __name__ == '__main__':
	app.run(debug=True)
    
    
    
    
    
    
    