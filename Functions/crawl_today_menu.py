from urllib.request import urlopen
from bs4 import BeautifulSoup

def today_menu(arg1:str, arg2:str, arg3:str) -> str:
    '''
    Args:
        arg1: {breakfast, launch, dinner}\n
        arg2: {staff, student}\n
        arg3: {2: 2학생회관, 3: 3학생회관, 4: 4학생회관}

    Return:
        'invalid input' or menu!
    '''

    #checking args
    check_arg1 = ['breakfast', 'launch', 'dinner']
    check_arg2 = ['staff', 'student']
    check_arg3 = ['2', '3', '4']
    if (arg1 not in check_arg1) or (arg2 not in check_arg2) or (arg3 not in check_arg3):
        return 'invalid input'
    

    #===========================crawling start======================================

    response = urlopen("https://mobileadmin.cnu.ac.kr/food/index.jsp")
    soup = BeautifulSoup(response, "html.parser")

    elements1 = soup.select('tbody > tr > td')

    menu_table = {
        'breakfast': {'staff': {'2': elements1[3].text, '3': elements1[4].text, '4': elements1[5].text},
                    'student': {'2': elements1[8].text, '3': elements1[9].text, '4': elements1[10].text}},

        'launch': {'staff': {'2': elements1[14].text, '3': elements1[15].text, 4: elements1[16].text},
                    'student': {'2': elements1[19].text, '3': elements1[20].text, 4: elements1[21].text}},

        'dinner': {'staff': {'2': elements1[25].text, '3': elements1[26].text, '4': elements1[27].text},
                    'student': {'2': elements1[30].text, '3': elements1[31].text, '4': elements1[32].text}}
    }

    return menu_table[arg1][arg2][arg3].strip()