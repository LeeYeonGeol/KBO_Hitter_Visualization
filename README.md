# KBO_Hitter_Visualization

## 프로젝트 소개
- 1982년부터 2023년까지 KBO 타자들의 주요 지표(타율, 출루율, 홈런, 안타) 등의 변화를 한눈에 알아볼 수 있습니다.
- 연도를 선택하면, 해당하는 연도의 팀 순위, 지표 변화가 나타납니다.
- 팀 혹은 선수를 클릭하면 그래프가 인터랙티브하게 변합니다.

## 기간
- 2023.11.23 ~ 2023.12.02

## Dependencies
```
pandas==2.0.1
selenium==4.15.2
tqdm==4.65.0
```

## 결과

- [대시보드 링크](https://public.tableau.com/app/profile/.76426565/viz/KBOHitterDashboard/KBOHitterDashboard)
- [블로그 링크](https://lottegiantsv3.tistory.com/212)

![image](https://github.com/LeeYeonGeol/leagueoflegends_metric_modeling/assets/48538655/2878ebef-81fa-4fbf-83d0-fa615651883f)
- 우측 상단 Year 파라미터를 통해 원하는 연도를 선택할 수 있다.
- 가운데에는 해당 연도의 팀 순위가 나온다.
- 좌, 우측에는 관련 그래프가 나온다.

![image](https://github.com/LeeYeonGeol/leagueoflegends_metric_modeling/assets/48538655/daddd407-67e8-430b-b433-abaef1fa7099)
- 팀을 선택하면 좌, 우측 그래프가 인터랙티브하게 변경된다.

![image](https://github.com/LeeYeonGeol/leagueoflegends_metric_modeling/assets/48538655/4cbcda57-1c9c-46ae-ac1a-2da1ee716af4)
- 선수를 선택하면, 좌측 그래프가 변화한다.
