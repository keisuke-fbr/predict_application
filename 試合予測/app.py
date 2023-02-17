import os
from flask import (
    Flask, 
    request, 
    render_template)

from predict import predict,getdata,makedata

UPLOAD_FOLDER='./static/dog_image'

app = Flask(__name__,static_folder="./images")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload_user_files():
    if request.method == 'POST':

        pwhen = (request.form["input_data0"])
        phome = (request.form["input_data1"])
        phomew = (request.form["input_data1"])
        paway = (request.form["input_data2"])
        pawayw = (request.form["input_data2"])
        pweather = (request.form["input_data3"])
        phumid = (request.form["input_data4"])
        ptemp = float(request.form["input_data5"])

        def isint(s):  # 整数値を表しているかどうかを判定
            try:
                int(s, 10)  # 文字列を実際にint関数で変換してみる
            except ValueError:
                return "error"  
            else:
                return int(s,10)  # 変換できたのでTrueを返す

        def isfloat(s):  # 浮動小数点数値を表しているかどうかを判定
            try:
                float(s)  # 文字列を実際にfloat関数で変換してみる
            except ValueError:
                return "error"
            else:
                return float(s)  # 変換できたのでTrueを返す

        pwhen = isint(pwhen)

        if pwhen != "error":
            #pwhenの整形
            if pwhen <= 10:

                pwhen = 0

            elif pwhen <=25:

                pwhen = 1

            elif pwhen <=38:

                pwhen =2 

            else:
                pwhen = "error"

        #phome,pawayの整形

        team_data = {"川崎F":0.8097,"FC東京":0.1516,"G大阪":0.1568,"鹿島":0.4412,"京都":-0.2353,"浦和":0.2613,"広島":0.4220,"鳥栖":-0.1073,"清水":-0.4029,"札幌":-0.3376,"横浜FM":0.4920,"C大阪":0.2067,"福岡":-0.4444,"磐田":-0.2618,"湘南":-0.4549,"柏":0.1183,"名古屋":-0.021,"神戸":-0.018,"横浜FC":-1.0417,"大分":-.05714,"徳島":-1.234,"仙台":-0.2566,"松本":-0.6324,"長崎":-0.5882,"新潟":-0.3618,"大宮":-0.3636,"甲府":-0.4353,"山形":-0.3618}
        
        if phome in team_data:
            phome = team_data[phome]
        else:
            phome = "error"


        if paway in team_data:
            paway = team_data[paway]
        else:
            paway = "error"
        
        

        #pweatherの整形
        weather_data = {"晴":0,"曇":1,"雨":2,"室内":3}
        if pweather in weather_data:
            pweather = weather_data[pweather]
        else:
            pweather = "error"

        #phumidの整形
        phumid = isint(phumid)

        #ptempの整形
        ptemp = isfloat(ptemp)


        
        judge1 = ["節","ホームチーム","アウェイチーム","天気","湿度","気温"]
        judge2 = [pwhen,phome,paway,pweather,phumid,ptemp]
        judge = []
        num = 0

        for i in judge2:
            if i == "error":
                judge.append(judge1[num])

            num += 1    

        if len(judge)==0:


            pdata = [[pwhen,phome,paway,pweather,phumid,ptemp]]

        

            result = predict(pdata)

            if result ==0:
                ans = phomew + "の勝ち"
                url = "../images/" + phomew + ".jfif"

            elif result==1:
                ans = pawayw + "の勝ち"
                url = "../images/" + pawayw + ".jfif"

            else :
                ans = "引き分け"
                url = "none"

        
            return render_template('result.html', ans = ans, url = url)

        else:
            return render_template('error.html',judge = judge)    

    

if __name__ == "__main__":
    app.run(debug=True)
