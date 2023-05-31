![Logo](https://github.com/Jakensori/Backend/blob/main/KakaoTalk_Photo_2023-05-25-15-15-42.jpeg?raw=true)

# Pass-the-Meal


## 💻 Project Introduction

A project that means taking care of my meals and taking care of other people's meals with the food expenses users saved. Project name is derived from 'pass the hat' that means collecting money. 

**GOALS**

1. It solves **health and well-being problems** by encouraging **regular eating habit** by analyzing and showing users' meal records.
2. It helps **planned consumption** by encouraging consumption that fits user's own food budget.
3. It contributes to **solving the hunger problem** by allowing users to **donate** underprivileged children **as part of their budget savings.**


## 🕰 Develop Period

- 2023.01 ~ 2023.06


## 💡 Deployed Address

- Backend

[http://34.64.250.212:8000](http://34.64.250.212:8000/) (GCP) `server for demo`

[http://52.78.205.224:8000](http://52.78.205.224:8000/) (AWS) `http`

[https://pass-meal.site](https://pass-meal.site/) (AWS) `https`

- Smart Contract

0xB6Ebd7f29D5BbF9C3Dc6245450dAd49fEba2C25b


## 👩‍💻 Members

- Gahyun Lee (Backend, Server) [@gahyun02](https://github.com/gahyun02)
- Jiwoo Yang (Frontend) [@yang-jiu](https://github.com/yang-jiu)
- Jungmin Lee (Frontend) [@lmin402](https://github.com/lmin402)
- Eunjung Kwon (Frontend) [@enjung](https://github.com/enjung)


## 📒 Pages

⭐️ **Sign in / Sign up**

Enter information such as ID and password and press the 'Sign up' and 'Sign in' buttons at the bottom to access the main page.

⭐️ **Record Meal**

It is a page that manages daily food expenses, and you can record your meal.

⭐️ **Chart**

This page is composed of household account book and food cost analysis.

1. *Household account book* : When the daily settlement is completed, it shows how much food expenses have been saved, handed over, and put in the donation box. The following shows the amount of consumption and savings compared to the monthly budget.
2. *Food Cost Analysis* : Shows the type of meal corresponding to the selection year and month compared to last month's statistics according to the number and cost.

⭐️ **Donation**

This is a page where you can donate the amount you saved through ‘Settle for a day’. You can see ongoing campaigns you can donate to and the campaigns you have donated to. 
In order to increase accessibility to the campaigns currently in progress, we have placed about 4 campaigns at the bottom so that you can preview them.

⭐️ **Collection**

You can see the amount of MEAL points users have earned through donation payment and the level proportional to the number of donations. When enough MEAL points are accumulated, you can unlock various characters. Complete your own collection!

⭐️ **My page**

You can check your basic information, modify your monthly food budget, and view your donation details in the form of a receipt.


## 📌 Services

- **Payment for donation**

We support simple payment through Toss Payments service. After a user selects the campaign and amount to be donated and pays, amount of payment is converted into Ether at a 1:1 ratio and deposited into the user's e-wallet.

- **Smart Contract & BlockChain**

20 MEAL points are awarded to the user after the donation is delivered to the campaign fundraising safe implemented as a smart contract. MEAL point is managed by Loyalty point API of Luniverse Baas(Blockchain as a service). So, You can see when and how your points were spent, and you can check them at a glance at any time.

- **Recording Meals**

Check a meal time, method and write price, and note. Then press the save button. After using the daily food expenses, press the "one-day settlement" button at the bottom of the middle to save the donation amount. Donations are possible as much as the difference between the daily food budget and expenditure and the donations will be accumulated in the donation box.

- **Tracking Consumption**

You can track monthly consumption through accountbook and analysis charts.
Go manage your consumption patterns in detail !

- **Keeping in touch with beneficiaries**

If you click the *Letter* icon in the upper right corner of app bar, you can see the news of people who have been helped through the campaign you donated to. When the fundraising period of the campaign you donated is over, you can communicate with the beneficiaries through photos of daily necessities provided by donations, their photos, or handwritten letters.

- **Donating to a campaign**

 Once you have selected the campaign you would like to donate to, you will be taken to the payment page and the amount accumulated in the donation box will be donated.


## 🛠 Tech Stacks
> **Backend**
> 
|역할|종류|
|-|-|
|Framework|![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white)|
|Deploy|![Amazon EC2](https://img.shields.io/badge/Amazon_EC2-FF9900?style=for-the-badge&logo=AmazonEC2&logoColor=white) ![Google_Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=Google_Cloud&logoColor=white) |
|Database|![MySQL](https://img.shields.io/badge/MySQL-4479A1.svg?style=for-the-badge&logo=MySQL&logoColor=white)  ![RDS](https://img.shields.io/badge/Amazon_RDS-527FFF.svg?style=for-the-badge&logo=AmazonRDS&logoColor=white) |
|Programming Language|![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white) ![Solidity](https://img.shields.io/badge/Solidity-363636?style=for-the-badge&logo=Solidity&logoColor=white) ![html](https://img.shields.io/badge/html-E34F26?style=for-the-badge&logo=html5&logoColor=white) |
|Environment|![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Visual_Studio_Code](https://img.shields.io/badge/Visual_Studio_Code-007ACC?style=for-the-badge&logo=Visual_Studio_Code&logoColor=white) ![Remix](https://img.shields.io/badge/Remix-000000?style=for-the-badge&logo=Remix&logoColor=white) |
|Communication|![Google Meet](https://img.shields.io/badge/Google_Meet-00897B?style=for-the-badge&logo=Google_Meet&logoColor=white) ![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white) ![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=Discord&logoColor=white)|
<br />

> **Frontend**
> 
|역할|종류|
|-|-|
|Framework|![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=Flutter&logoColor=white)|
|Programming Language|![Dart](https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=Dart&logoColor=white)|
|Environment|![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Visual_Studio_Code](https://img.shields.io/badge/Visual_Studio_Code-007ACC?style=for-the-badge&logo=Visual_Studio_Code&logoColor=white) ![Android_Studio](https://img.shields.io/badge/Android_Studio-3DDC84?style=for-the-badge&logo=Android_Studio&logoColor=white) |
|Communication|![Google Meet](https://img.shields.io/badge/Google_Meet-00897B?style=for-the-badge&logo=Google_Meet&logoColor=white) ![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white) ![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=Discord&logoColor=white)|
## 🔍 Action Guide

### Requirements

> **Backend**
> 

For building and running the application you need:

- Python 3.9.2

```bash
git clone https://github.com/Jakensori/Backend.git
pip install -r requirements.txt
cd Backend/naegginiggi

python3 manage.py runserver
```


## 🔗 Architecture

- Structure of directories
```Plain Text
├── README.md
├── .gitignore
├── db.sqlite3
├── donation_smartcontract.sol    : file of smartcontract
├── dump.rdb
├── manage.py
├── requirements.txt              : installed packages
├── artifacts
	├── test.json
	├── test_metadata.json
└── campaign
	├── migrations
	└── templates/chat
			├── chat_room.html
			└── index.html
	├── __init__.py
	├── admin.py
	├── apps.py
	├── consumers.py
	├── models.py
	├── routing.py
	├── serializers.py
	├── tests.py
	├── urls.py
	└── views.py
└── donation_point
	├── migrations
	└── templates/chat
			├── requestPayment.html     : payment webview 
			└── success.html
	├── .views.py.swp
	├── __init__.py
	├── admin.py
	├── apps.py
	├── models.py
	├── routing.py
	├── serializers.py
	├── tests.py
	├── urls.py
	└── views.py
└── naegginiggi
	├── __init__.py
	├── asgi.py
	├── result.json                  : donation campaign crawling data
	├── search_apitest.py            : crawling 'happybean' site
	├── settings.py
	├── urls.py
	└── wsgi.py
└── user
	├── migrations
	├── __init__.py
	├── admin.py
	├── apps.py
	├── models.py
	├── serializers.py
	├── tests.py
	├── urls.py
	└── views.py
└── user_custom
	├── migrations
	├── __init__.py
	├── admin.py
	├── apps.py
	├── models.py
	├── serializers.py
	├── tests.py
	├── urls.py
	└── views.py
└── user_record
	├── migrations
	├── .views.py.swp
	├── __init__.py
	├── admin.py
	├── apps.py
	├── models.py
	├── serializers.py
	├── tests.py
	├── urls.py
	└── views.py
```
