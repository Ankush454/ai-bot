# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import requests
import json

# TODO: replace with your own app_id and app_key

# TODO: replace with your own app_id and app_key
app_id = 'f9276b3b'
app_key = '2dc1726dc25ade86558c12bf0249444f'

language = 'en'

def dictionary(word_id):
	url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
	# meaning = [l for d in r.json()["results"] for i in d["lexicalEntries"] for j in i["entries"] for k in j["senses"] for l in k["definitions"]]
	meaning = []
	try:
		text = [k for d in r.json()["results"] for i in d["lexicalEntries"] for j in i["entries"] for k in j["senses"]]
		try:
			for i in text:
				meaning.append(''.join(i["definitions"]))
		except:
			pass
	except:
		meaning = ["Sorry this {} can't be found".format(word_id)]
	
	return [r.status_code, meaning]
	# return [r.status_code, json_data]
	# print("code {}\n".format(r.status_code))
	# print("text \n" + r.text)
# print("json \n" + json.dumps(r.json()))

# dictionary('set')