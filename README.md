# hand recognition game
2022 Summer MadCamp Week4

## Project name
몰?루 게임

## Teammates
KAIST 전산학부 방준형

POSTECH 컴퓨터공학과 박정은

## Description
gesture 인식을 적용한 크레이지 아케이드 게임

방향키 : 손가락 방향

물풍선 : 보자기

바늘 : 주먹


## Implementation Method
pygame 라이브러리를 사용하여 game ui 및 알고리즘 구현

손 인식은 openCV (openPose)로 구현

socket으로 양방향 통신 구현

## Usage
### tab1 – login page                   

|로그인 화면|회원가입 화면|방 생성 화면|
|---|---|---|
|![image](https://user-images.githubusercontent.com/91946706/181479253-ea2149b4-6c36-4477-8750-5d49e21573c1.png)|![image](https://user-images.githubusercontent.com/91946706/181479385-bd755dbb-ddcb-44a3-bf4c-68ff415a334c.png)|![image](https://user-images.githubusercontent.com/91946706/181479498-2bc1455a-a6c5-4d21-a171-e32cf3740251.png)|

### tab2.1 – 대기실 page                 

|대기실(1명)|대기실(2명)|
|---|---|
|![image](https://user-images.githubusercontent.com/91946706/181479591-409edc5e-e269-4845-a3f6-73e8464cb6e6.png)|![image](https://user-images.githubusercontent.com/91946706/181479674-b40e90dd-c3da-4cb1-9f32-05111672c8c6.png)|

### tab2.2 – game page                 

|게임 시작화면|웹캠|게임 진행화면|배찌 사망|
|---|---|---|---|
|![image](https://user-images.githubusercontent.com/91946706/181479806-b3b7e45d-6c9f-4646-9fde-c9d35b8a6831.png)|![image](https://user-images.githubusercontent.com/91946706/181482255-22efb129-a782-4c9c-a950-c537ab28ebbd.png)|![image](https://user-images.githubusercontent.com/91946706/181483197-0a40df22-50b2-4ac3-a3a7-a191fd1a9497.png)|![image](https://user-images.githubusercontent.com/91946706/181479857-22c61609-cfe9-45af-af76-d7c7aedf76dd.png)|

### 일화
웹캠이 방준형 얼굴을 "보자기"로 인식해서 물풍선을 쐈다. (ㅈㄴ웃기다)
