import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import nltk.stem.porter as port

def main():
	stopwords=['a', 'about', 'after', 'against', 'all', 'also', 'an', 'and', 'any', 'apr', 'april', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'between', 'blah', 'both', 'but', 'by', 'can', 'co', 'could', 'did', 'down', 'due', 'during', 'each', 'end', 'expected', 'feb', 'february', 'first', 'five', 'for', 'four', 'from', 'general', 'had', 'has', 'have', 'he', 'here', 'his', 'is', 'if', 'in', 'includes', 'into', 'is', 'it', 'its', 'jan', 'january', 'july', 'june', 'just', 'last', 'made', 'make', 'mar', 'march', 'may', 'might', 'more', 'most', 'must', 'nearly', 'new', 'next', 'no', 'not', 'now', 'of', 'on', 'one', 'only', 'or', 'other', 'our', 'out', 'over', 'per', 'quite', 'reuter', 's', 'said', 'same', 'says', 'set', 'she', 'should', 'since', 'six', 'so', 'some', 'such', 'th', 'than', 'that', 'the', 'their', 'there', 'these', 'they', 'this', 'those', 'three', 'through', 'thus', 'to', 'today', 'told', 'two', 'u', 'under', 'up', 'using', 'very', 'vs', 'was', 'we', 'well', 'were', 'what', 'when', 'which', 'while', 'who', 'will', 'with', 'world', 'would', 'year', "ain't", "can't", "wouldn't", "i'll", "couldn't", "it'll", 'ill', "u're", 'i', 'then', 'p', 'do','etc']   #list of stopwords
	stem=port.PorterStemmer()
	cnt=0
	flag1=False
	flag2=False
	flag3=False
	flag4=False
	flag5=False
	flg=True
	categ=[]
	vocab=[]
	f=open('C:\\Users\\dell\\Desktop\\result.csv','w+')
	with open('C:\\Users\\dell\\Downloads\\Train\\Train.csv') as fileobject:
		for line in fileobject:
			if cnt<0:
				cnt+=1
			else:
				strn=line.split(",")
				if re.search("^\"[0-9]+",strn[0]):  #first field consisting of ID
					t=strn
					if len(strn)<3:
						flag3=True
					if flag3==False:
						r=strn[2]
						for i in range(2,len(strn)-1):
							r+=" " + strn[i+1]
						flag1=True
					else:
						z=strn[1]
						for i in range(1,len(strn)-1):
							z+=" " + strn[i+1]
						flag4=True
				if strn[0]=='"':  #last field consisting of tags 
					r+=strn[0]
					if flag3==True:
						t[1]=z
					t=t[:2]
					t.append(r)
					s=t
					s.append(strn[1])
					if (cnt<65000):

						categ += processtext(s[3])

					else:
						if flg==True:  #vocabulary of tags
							category=list(set(categ))
							NWORDS=train(category)
							for i in range(len(category)):
								category[i]=stem.stem(category[i]) #stem the words using PortStemmer
							category=[w for w in category if w not in stopwords]
							category=list(set(category))
							acc1=0.0
							j=0
							flg=False

						vocab=processtext(s[1] + " " + s[2])   # vocabulary of title and body for each problem
						vocabulary=list(set(vocab))
						NWORDS=train(vocabulary)
						for i in range(len(vocabulary)):
							vocabulary[i]=stem.stem(vocabulary[i]) 
						vocabulary=[w for w in vocabulary if w not in stopwords]
						vocabulary=list(set(vocabulary))
						predtag=list(set(vocabulary).intersection(set(category)))  #predict tags based on match between vocab of question and vocab of tags
						actualtag=processtext(s[3]) #actual tags
						for i in range(len(actualtag)):
							actualtag[i]=stem.stem(actualtag[i])
						actualtag=list(set(actualtag))
						acc=len(list(set(predtag).intersection(set(actualtag))))/float(len(actualtag)) #determine accuracy based on no of tags predicted matching the actual ones
						acc1 += acc
						f.write(s[0] + ',' + ' '.join(predtag) + '\n') #write the problem ID,predicted tags in CSV file.
						

					cnt+=1
					if cnt==100000:   #considered 100000 records with 65000 as training and rest as testing
						break

					flag2=False
					flag1=False
					flag3=False

				if flag2==True:
					for i in strn:
						r+= " " + i
				if flag5==True:
					if strn[len(strn)-1][0]=='"':
						for i in range(len(strn)-1):
							z+= " " + strn[i]
						r += " " + strn[len(strn)-1]
						flag5=False
						flag4=False
						flag2=True

					else:
						for i in strn:
							z+= " " + i
				if flag1==True:
					flag2=True
				if flag4==True:
					flag5=True


def processtext(raw): #tokenize the raw text
	tokens=re.findall("[A-Za-z#]+|[0-9]+(?:\.[0-9]+)*",raw)
	words=[w.lower() for w in tokens]
	vocab=sorted(set(words))
	return vocab
def converttoxml(s):
	idnum=re.split('"',s[0])
	title=re.split('"',s[1])
	body=re.findall('<p>(.*?)</p>',s[2],re.DOTALL)
	textstring=''
	stry=''
	for i in body:
		textstring+=i
	temp=re.split('"',s[3])
	tags=re.split(" ",temp[1])
	XML='<DOC>\n<ID>' + idnum[1] + '<\\ID>\n<TEXT>\n<TITLE>' + title[1] + '<\\TITLE>\n<BODY>' + textstring + '<\\BODY>\n<TOPICS>\n'
	for i in tags:
		stry+='<TOPIC>' + i + '<\\TOPIC>\n'
	XML+=stry
	XML+='<\\TOPICS>\n<\\TEXT>\n<\\DOC>\n\n'
	f.write(XML)


