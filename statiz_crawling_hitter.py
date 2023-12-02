from tqdm import tqdm
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd 

def get_dataframe(driver, team_xpath, year):
    team = driver.find_element(By.XPATH, team_xpath+"button").text
    try:
        df = pd.read_html(driver.page_source)[1]
        print(f'#######{year} {team}#######')

        # 멀티 인덱스 제거
        df.columns = df.columns.droplevel()

        # 필요없는 칼럼 제거 WAR*(중복), 순
        filter_columns = ~df.columns.duplicated()
        filter_columns[0] = False
        df = df.loc[:, filter_columns]

        # 필요없는 열 제거
        df = df[df['이름'] != '이름']

        # 타입 변환 및 NULL값 제거
        float_columns = ['WAR*', '타율', '출루', '장타', 'OPS', 'wOBA', 'wRC+', 'WPA'] 
        int_columns = ['G', '타석', '타수', '득점', '안타', '2타', '3타', '홈런', '루타', '타점', '도루', '도실', '볼넷', '사구', '고4', '삼진', '병살', '희타', '희비']
        df[float_columns+int_columns] = df[float_columns+int_columns].apply(pd.to_numeric, errors='coerce')
        df[int_columns] = df[int_columns].astype('int')

        # 소속팀 및 시즌 정보 추가
        df.insert(0, '소속팀', team)
        df.insert(0, '시즌', year)
        df['시즌'] = df['시즌'].astype('int')

        return df

    except:
        return pd.DataFrame()

if __name__ == '__main__':
    df = pd.DataFrame()

    # 스탯티즈 사이트 접속
    url = 'http://www.statiz.co.kr/stat.php'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    year_xpath = '/html/body/div[1]/div[1]/div/section[2]/div/div[2]/div[1]/div/div[1]/div/'
    team_xpath = '/html/body/div[1]/div[1]/div/section[2]/div/div[2]/div[1]/div/div[3]/'
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/section[2]/div/div[2]/div[1]/div/div[9]/button'))).send_keys(Keys.ENTER)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/section[2]/div/div[2]/div[2]/div[2]/div[5]/form/select'))).send_keys("100")
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/section[2]/div/div[2]/div[2]/div[2]/div[5]/form/select/option[5]'))).click()
    except:
        pass


    # 연도 선택 2 ~ 44
    for idx1 in tqdm(range(2, 44)):
        year = idx1+1980
        retry = 0
        max_retries = 3
        while retry < max_retries:
            try:
                next_df = pd.DataFrame()
                wait.until(EC.presence_of_element_located((By.XPATH, year_xpath+"button"))).send_keys(Keys.ENTER)
                wait.until(EC.presence_of_element_located((By.XPATH,year_xpath+"ul/div/button"+f"[{idx1}]"))).send_keys(Keys.ENTER)
                # 팀 선택 1 ~ 13
                for idx2 in range(1, 13):
                    wait.until(EC.presence_of_element_located((By.XPATH, team_xpath+"button"))).send_keys(Keys.ENTER)
                    wait.until(EC.presence_of_element_located((By.XPATH, team_xpath+"ul/div[3]/button"+f"[{idx2}]"))).send_keys(Keys.ENTER)
                    next_df = pd.concat([next_df, get_dataframe(driver, team_xpath, year)])
                df = pd.concat([df, next_df])
                break
                
            except:
                # 사이트 재접속
                url = 'http://www.statiz.co.kr/stat.php?sn=100'
                driver = webdriver.Chrome()
                driver.get(url)
                retry += 1

                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/section[2]/div/div[2]/div[1]/div/div[9]/button'))).send_keys(Keys.ENTER)
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/section[2]/div/div[2]/div[2]/div[2]/div[5]/form/select'))).send_keys("100")
                    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/section[2]/div/div[2]/div[2]/div[2]/div[5]/form/select/option[5]'))).click()
                except:
                    pass
                
    df.to_csv("hitter_record_1982_to_2023(ver.2).csv",index=False)