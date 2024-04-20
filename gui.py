__version__ = "0.0.0.0"
app_name = "Flow Tutor"


# BOILERPLATE

import streamlit as st
st.set_page_config(layout='centered', page_title=f'{app_name} {__version__}')
ss = st.session_state
if 'debug' not in ss: ss['debug'] = {}
import css
st.write(f'<style>{css.v1}</style>', unsafe_allow_html=True)
header1 = st.empty() # for errors / messages
header2 = st.empty() # for errors / messages
header3 = st.empty() # for errors / messages

# IMPORTS

import os

from time import time as now

# HANDLERS

def on_api_key_change():




	on_api_key_change() # use community key

ss['community_user'] = os.getenv('COMMUNITY_USER')
if 'user' not in ss and ss['community_user']:
	on_api_key_change() # use community key

# COMPONENTS


def ui_spacer(n=2, line=False, next_n=0):
	for _ in range(n):
		st.write('')
	if line:
		st.tabs([' '])
	for _ in range(next_n):
		st.write('')

def ui_info():
	st.markdown(f"""
	# Flow Tutor
	### Empowering Developers with AI-Driven learning.
	version {__version__}
	
	Flow smart contracts analysis built with Flow blockchain.
	""")
	ui_spacer(1)
	st.write("Designed by [Abisoye Onanuga](https://abisoyeonanuga.github.io/website).", unsafe_allow_html=True)
	ui_spacer(1)
	st.markdown("""
		Welcome to Flow Tutor UI.
		A design system for Flow Tutor.
		""")
	ui_spacer(1)
	st.markdown('Source code on [Github](https://github.com/abisoyeonanuge/flow-tutor-ui).')

def ui_api_key():
	if ss['community_user']:
		st.write('## 1. Optional - enter your AI API key')
		t1,t2 = st.tabs(['community version','enter your own API key'])
		with t1:
			pct = ()
			st.write(f'Community tokens available: :{"green" if pct else "red"}[{int(pct)}%]')
			st.progress(pct/100)
			st.write('Refresh in: ' + ())
			st.write('You can sign up to AI and/or create your API key [here](https://platform.openai.com/account/api-keys)')
			ss['community_pct'] = pct
			ss['debug']['community_pct'] = pct
		with t2:
			st.text_input('AI API key', type='password', key='api_key', on_change=on_api_key_change, label_visibility="collapsed")
	else:
		st.write('## 1. Enter your AI API key')
		st.text_input('AI API key', type='password', key='api_key', on_change=on_api_key_change, label_visibility="collapsed")

def ui_pdf_file():
	st.write('## 2. Upload or select your PDF file')
	disabled = not ss.get('user') or (not ss.get('api_key') and not ss.get('community_pct',0))
	t1,t2 = st.tabs(['UPLOAD','SELECT'])
	with t1:
		st.file_uploader('pdf file', type='pdf', key='pdf_file', disabled=disabled, label_visibility="collapsed")
		b_save()
	with t2:
		filenames = ['']
		if ss.get('storage'):
			filenames += ss['storage'].list()
		def on_change():
			name = ss['selected_file']
			if name and ss.get('storage'):
				with ss['spin_select_file']:
					with st.spinner('loading index'):
						t0 = now()
						index = ss['storage'].get(name)
						ss['debug']['storage_get_time'] = now()-t0
				ss['filename'] = name # XXX
				ss['index'] = index

			else:
				#ss['index'] = {}
				pass
		st.selectbox('select file', filenames, on_change=on_change, key='selected_file', label_visibility="collapsed", disabled=disabled)
		b_delete()
		ss['spin_select_file'] = st.empty()


def b_ask():
	c1,c2,c3,c4,c5 = st.columns([2,1,1,2,2])
	if c2.button('👍', use_container_width=True, disabled=not ss.get('output')):
		ss['feedback'].send(+1, ss, details=ss['send_details'])
		ss['feedback_score'] = ss['feedback'].get_score()
	if c3.button('👎', use_container_width=True, disabled=not ss.get('output')):
		ss['feedback'].send(-1, ss, details=ss['send_details'])
		ss['feedback_score'] = ss['feedback'].get_score()
	score = ss.get('feedback_score',0)
	c5.write(f'feedback score: {score}')
	c4.checkbox('send details', True, key='send_details',
			help='allow question and the answer to be stored in the ask-my-pdf feedback database')
	#c1,c2,c3 = st.columns([1,3,1])
	#c2.radio('zzz',['👍',r','👍','👍','👍',...',r'👎'],horizontal=True,label_visibility="collapsed")
	#
	disabled = (not ss.get('api_key') and not ss.get('community_pct',0)) or not ss.get('index')
	if c1.button('get answer', disabled=disabled, type='primary', use_container_width=True):
		question = ss.get('question','')
		temperature = ss.get('temperature', 0.0)
		hyde = ss.get('use_hyde')
		hyde_prompt = ss.get('hyde_prompt')
		if ss.get('use_hyde_summary'):
			summary = ss['index']['summary']
			hyde_prompt += f" Context: {summary}\n\n"
		task = ss.get('task')
		max_frags = ss.get('max_frags',1)
		n_before = ss.get('n_frag_before',0)
		n_after  = ss.get('n_frag_after',0)
		index = ss.get('index',{})
		with st.spinner('preparing answer'):
			resp = (
				)
		usage = resp.get('usage',{})
		usage['cnt'] = 1
		ss['debug']['model.query.resp'] = resp
		ss['debug']['resp.usage'] = usage
		ss['debug']['model.vector_query_time'] = resp['vector_query_time']
		
		q = question.strip()
		a = resp['text'].strip()
		ss['answer'] = a
		output_add(q,a)
		st.experimental_rerun() # to enable the feedback buttons

def b_clear():
	if st.button('clear output'):
		ss['output'] = ''

def b_reindex():
	# TODO: disabled
	if st.button('reindex'):
		()

def b_reload():
	if st.button('reload prompts'):
		import importlib
		importlib.reload()

def b_save():
	db = ss.get('storage')
	index = ss.get('index')
	name = ss.get('filename')
	api_key = ss.get('api_key')
	disabled = not api_key or not db or not index or not name
	help = "The file will be stored for about 90 days. Available only when using your own API key."
	if st.button('save report on Flow Tutor', disabled=disabled, help=help):
		with st.spinner('saving to ask-my-pdf'):
			db.put(name, index)

def b_delete():
	db = ss.get('storage')
	name = ss.get('selected_file')
	# TODO: confirm delete
	if st.button('delete from ask-my-pdf', disabled=not db or not name):
		with st.spinner('deleting from ask-my-pdf'):
			db.delete(name)
		#st.experimental_rerun()

def output_add(q,a):
	if 'output' not in ss: ss['output'] = ''
	q = q.replace('$',r'\$')
	a = a.replace('$',r'\$')
	new = f'#### {q}\n{a}\n\n'
	ss['output'] = new + ss['output']

# LAYOUT

with st.sidebar:
	ui_info()
	ui_spacer(2)
	with st.expander('advanced'):
		b_clear()
		b_reload()

ui_api_key()
ui_pdf_file()
b_ask()
