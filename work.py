import urllib
import urllib.request
import re

url = 'https://tos.fandom.com'
home_page = '/zh/wiki/%E7%A5%9E%E9%AD%94%E4%B9%8B%E5%A1%94_%E7%B9%81%E4%B8%AD%E7%B6%AD%E5%9F%BA?variant=zh-tw'
content = urllib.request.urlopen(url + home_page)
html_str = content.read().decode('utf-8')

def color(string):
    if string == '水':
        return '\uD83D\uDCA7'
    elif string == '木':
        return '\uD83C\uDF32'
    elif string == '光':
        return '\uD83C\uDF15'
    elif string == '暗':
        return '\uD83C\uDF11'
    else:
        return '\uD83D\uDD25'

# return [[names, names, ...], [url, url, ...]]
def home_info(pattern):
    url_name = []
    url_url = []
    pattern = '<a[^<]*</a> </span> ※'+pattern
    result = re.findall(pattern, html_str)
    if result == []:
        return [['no data'],['no data']]
    for term in result:
        #print(term)
        url_name.append(re.findall('title=\"[^\"]*',term)[0][7::])
        url_url.append(re.findall('href=\"[^\"]*',term)[0][6::])
    for i in range(len(url_url)):
        ## build a complete url
        url_url[i] = url + url_url[i]
    return [url_name, url_url]

'''result = home_info('地獄級')
for i in range(len(result[0])):
    print(result[0][i])
    print(result[1][i])'''

def find_color(href):
    content = urllib.request.urlopen(url + href[6::])
    html_str = content.read().decode('utf-8')
    result = re.findall('屬性\n</th><td colspan="3" style="font-size:1.5em"><b>[\\s]*[\\S]', html_str)
    return result[0][len(result[0])-1]
# input: stage url
# return: ['1.\nattack: 2000\n ... skill:...\n\n "another monster"', 
# '2.\nattack: 2001\n ... skill', ...]
def stage_info(sub_url):
    content = urllib.request.urlopen(sub_url)
    html_str = content.read().decode('utf-8')
    pattern = '<td class=\"stage\">[^\n]*|name=\"Race[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n'
    blocks = re.findall(pattern, html_str)
    result = []
    stage_counter = 1
    ## an enemy a block
    for block in blocks:
        if block[0:18] == '<td class="stage">':
            result.append(str(stage_counter)+'.')
            stage_counter += 1
            if not(block[len(block)-1:len(block)].isdigit()):
                if re.findall('血',block) != []:
                    result[len(result)-1] += '雙血'
            result[len(result)-1] += '\n'
        else:
            line = re.findall('[^\n]*\n',block)
            tmp_text = re.findall('href=\"[^"]*',line[0])
            result[len(result)-1] += '\t'+color(find_color(tmp_text[0]))+' '
            result[len(result)-1] += line[0][10:12] + '\n'

            tmp_text = re.findall('[0-9]+',line[2])
            result[len(result)-1] += '攻擊 ' + tmp_text[0] + '\n'

            tmp_text = re.findall('[0-9]+',line[3])
            result[len(result)-1] += 'CD '
            if len(tmp_text) == 2:
                result[len(result)-1] += tmp_text[0]+'('+tmp_text[1]+')\n'
            else:
                result[len(result)-1] += tmp_text[0] + '\n'

            tmp_text = re.findall('>[0-9]+<',line[4])
            if tmp_text != []:
                result[len(result)-1] += 'HP ' + tmp_text[0][1:-1]+'\n'
            else:
                tmp_text = re.findall('[0-9]+',line[4])
                result[len(result)-1] += 'HP ' + tmp_text[0]+'\n'

            tmp_text = re.findall('[0-9]+',line[5])
            result[len(result)-1] += '防禦 ' + tmp_text[0] + '\n'

            tmp_text = re.findall('title=\"敵人技能[^\"]*\"><span[^>]*>[^<]*<', line[8])
            skill_text = re.findall('>[^<]*<', tmp_text[0])
            for skill in skill_text:    ## short skill description
                if skill[1:-1] != '':
                    result[len(result)-1] += skill[1:-1] + '\n'
            ## find long skill description
            skill_text = re.findall('title=\"[^\"]*', tmp_text[0][3::])
            result[len(result)-1] += skill_text[0][7:] + '\n\n'
    # return a list
    return result


class StateMachine():
    url_to_choose = []
    hell_to_choose = []
    def __init__(self):
        self.state = "start"
    def get_text(self, in_text):
        if self.state == 'start':
            self.state = 'web'
            return ['選擇服務:\n地獄級\nOthers']
        elif self.state == 'web':
            tmp = self.web_state(in_text)
            if tmp[0] == 'no data':
                state = 'start'
                return ['Error: no data about 地獄級']
            # combine list to a string
            result = ''
            for term in tmp:
                result += term + '\n'
            #stage_info(self.url_to_choose[0])
            return [result.strip()]
        elif self.state == 'hell':
            tmp = self.hell_state(in_text)
            result = ""
            for term in tmp:
                result += term + '\n'
            return [result.strip()]
        elif self.state == 'info':
            return [self.info_state(in_text)]
        else:
            return ['How did you get this state!?']

    def web_state(self, in_text):
        if in_text == '地獄級' or in_text == '1':
            self.state = 'hell'
            # find all hell in home page
            result = home_info('地獄級')
            # store the url in ordered list
            self.url_to_choose = result[1]
            self.hell_to_choose = result[0]
            real_result = '選擇關卡:\n'
            for i in range(len(result[0])):
                real_result += str(i+1) + '. ' + result[0][i] + '\n'
            return [real_result]
        elif in_text.lower()=='others':
            return ['Others 暫缺']
        else:
            return ['Input "1" or "地獄級" to get more information']
    def hell_state(self, in_text):
        self.state = 'info'
        if in_text.isdigit():
            in_text = int(in_text)
        if type(in_text) == type(1):
            return stage_info(self.url_to_choose[in_text-1])
        elif type(in_text) == type(''):
            for i in range(len(self.hell_to_choose)):
                if in_text == self.hell_to_choose[i]:
                    return stage_info(self.url_to_choose[i])
                if len(in_text)>1 and len(in_text)<len(self.hell_to_choose[i]):
                    if in_text == self.hell_to_choose[i][0:len(in_text)]:
                        return stage_info(self.url_to_choose[i])
        self.state = 'hell'
        return ['No such stage. Please try again.']
    def info_state(self, in_text):
        if in_text.lower() == 'back':
            self.state = 'hell'
            result = '選擇關卡:\n'
            for i in range(len(self.hell_to_choose)):
                result += str(i+1)+'. '+self.hell_to_choose[i] + '\n'
            return result.strip()
        elif in_text.lower() == 'home':
            self.state = 'web'
            return '選擇服務:\n地獄級\nOther Options'
        ## else
        return self.info_state('home')

#current_state = StateMachine()
#print(current_state.get_text('1'))
#current_state.get_text('1')
def main(text):
    if text == 'hello':
        return 'world'
    elif text == 'Hello':
        return 'World \uD83D\uDD25'
    else:
        return text
