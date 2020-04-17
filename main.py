#-*- coding:utf-8 -*-

import time
import os
import sys
from selenium import webdriver

#파일로드 함수
def Setup():
    global id, password, url, btested, studentId, name

    idFile = open(os.getcwd() + "\\setup\\id.txt",encoding="utf-8")
    id = idFile.read().replace("\n","").strip()
    idFile.close()

    passwordFile = open(os.getcwd() + "\\setup\\password.txt",encoding="utf-8")
    password = passwordFile.read().replace("\n","").strip()
    passwordFile.close()

    urlFile = open(os.getcwd() + "\\setup\\url.txt",encoding="utf-8")
    url = urlFile.read().replace("\n","").strip()
    urlFile.close()

    studentIdFile = open(os.getcwd() + "\\setup\\studentId.txt",encoding="utf-8")
    studentId = studentIdFile.read().replace("\n","").strip()
    studentIdFile.close()

    nameFile = open(os.getcwd() + "\\setup\\name.txt",encoding="utf-8")
    name = nameFile.read().replace("\n","").strip()
    nameFile.close()

    btestedFile = open(os.getcwd() + "\\programfiles\\btested.txt",encoding="utf-8")
    btested = bool(btestedFile.read().replace("\n","").strip())
    btestedFile.close()

    
    

#출석체크 함수
def DoAttendanceCheck():
    driver = webdriver.Chrome(os.getcwd() + "\\programfiles\\chromedriver.exe")
    driver.get('https://www.google.com')

    driver.implicitly_wait(10)
    driver.find_element_by_id('gb_70').click()

    driver.find_element_by_id('identifierId').send_keys(id)
    driver.find_element_by_id("identifierNext").click()

    driver.implicitly_wait(10)

    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_id("passwordNext").click()
    
    time.sleep(3)

    driver.get(url)

    driver.find_element_by_xpath('//*[@id="ow43"]/div[2]/div[1]/div[1]/div').click()
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div/div').click()
    driver.implicitly_wait(10)

    #미완성
    driver.switch_to.window(driver.window_handles[1])

    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/input').send_keys(studentId)  
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/input').send_keys(name)
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div/div[2]/div[3]/div/div[2]/div/div/label/div/div[1]/div[2]').click()
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div/div[3]/div[1]/div/div/span').click()

    driver.switch_to.window(driver.window_handles[0])

    driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[4]/div[2]/div/div[2]/aside/div[1]/div[2]/div[1]/div[1]/div[2]/textarea').send_keys("출석체크")
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[4]/div[2]/div/div[2]/aside/div[1]/div[2]/div[3]/div[2]/span').click()
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[12]/div/div[2]/div[3]/div[2]/span/span').click()
    #미완성
    

#로그작성 함수
def WriteLog(message):
    logFile = open(os.getcwd() + "\\programfiles\\log.txt","a",encoding="utf-8")
    logFile.write(message)
    logFile.close()




print("자동출석체크 - Developed by YJU")
print("개발자 연락처 : yju0808@naver.com - 버그, 오류 등등 발견시 제보해주세요\n\n")



#파일로드
Setup()

#테스트
if btested:
    print("테스트는 이미 진행했으니 생략합니다")
else:
    print("올바른 환경설정이 셋업되었는지 테스트합니다")
    time.sleep(1)

    #driver개체가 생성되는지 확인
    try:
        driver = webdriver.Chrome(os.getcwd() + "\\programfiles\\chromedriver")
    except Exception as e:
        print("크롬81버젼이 맞나요? 버젼을 확인해주세요")
        WriteLog("Test fail {},{}\n".format("chromedriver version error",time.strftime('%c', time.localtime(time.time()))))
        input("종료하시려면 아무키나 입력하세요  ")
        print("\n\n종료되었습니다")
        sys.exit()

    driver.get('https://www.google.com')

    driver.implicitly_wait(10)
    driver.find_element_by_id('gb_70').click()

    driver.find_element_by_id('identifierId').send_keys(id)
    driver.find_element_by_id("identifierNext").click()

    driver.implicitly_wait(10)
    
    #password입력창으로 넘어왔는지 확인
    try:
        driver.find_element_by_name("password").send_keys(password)
    except Exception as e:
        print("id가 잘못된 것 같군요 설정을 확인해 보세요")
        WriteLog("Test fail {},{}\n".format("not correct id",time.strftime('%c', time.localtime(time.time()))))
        input("종료하시려면 아무키나 입력하세요  ")
        print("\n\n종료되었습니다")
        driver.quit()
        sys.exit()

    driver.find_element_by_id("passwordNext").click()
    
    time.sleep(3)

    #로그인에 성공했는지 확인
    if not driver.current_url == "https://www.google.com/":
        print("password가 잘못된 것 같군요 설정을 확인해 보세요")
        WriteLog("Test fail {},{}\n".format("not correct password",time.strftime('%c', time.localtime(time.time()))))
        input("종료하시려면 아무키나 입력하세요  ")
        print("\n\n종료되었습니다")
        driver.quit()
        sys.exit()

    driver.get(url)

    #url이 구글 클래스룸으로 시작하는지 확인(엄밀히 말해서 완벽한 확인은 아님)
    if not driver.current_url.startswith("https://classroom.google.com/"):
        print(driver.current_url)
        print("url이 잘못된 것 같군요 설정을 확인해 보세요")
        WriteLog("Test fail {},{}\n".format("not correct url",time.strftime('%c', time.localtime(time.time()))))
        input("종료하시려면 아무키나 입력하세요  ")
        print("\n\n종료되었습니다")
        driver.quit()
        sys.exit()

    btestedFile = open(os.getcwd() + "\\programfiles\\btested.txt","w",encoding="utf-8")
    btestedFile.write("True")
    btestedFile.close()

    driver.quit()

    print("테스트가 성공적으로 종료되었습니다 :)\n\n")
    WriteLog("Test success {}\n".format(time.strftime('%c', time.localtime(time.time()))))



print("매일 아침 9시마다 출석체크를 진행합니다")

#매일 아침 9시마다 출석체크
while True:
    currentHour=time.strftime('%H', time.localtime(time.time()))
    currentAllTime = time.strftime('%c', time.localtime(time.time()))

    if currentHour == "09":
        print("9시네요! 출석체크를 진행합니다!")
        try:
            DoAttendanceCheck()
            print("출석체크를 완료했습니다 {}".format(currentAllTime))
            WriteLog("AttendanceCheck success {}\n".format(currentAllTime))

            time.sleep(86400)

        except Exception as e:
            print(e)
            print("에러가 발생했습니다 해당 메시지 발견시 즉시 개발자에게 문의주세요 일단 출석체크를 다시한번 시도하겠습니다")
            WriteLog("AttendanceCheck fail {}, {}\n".format(e,currentAllTime))
            
            #실패시 한번더 시도
            try:
                DoAttendanceCheck()
                print("다시한번 시도한 결과 성공했습니다 다만 첫번째 오류메시지를 반드시 제보해주세요 {}".format(currentAllTime))
                WriteLog("re AttendanceCheck success {}\n".format(currentAllTime))
                time.sleep(86400)

            except Exception as e:
                print(e)
                print("다시한번 시도했지만 실패하였습니다 개발자에게 반드시 문의넣어주세요")
                WriteLog("re AttendanceCheck fail {}, {}\n".format(e,currentAllTime))
                time.sleep(86400)








