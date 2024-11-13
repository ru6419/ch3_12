from django.shortcuts import redirect, render
from django.http import HttpResponse
from myapp.models import * 
from django.forms.models import model_to_dict

# 查詢資料
def search_list(request):
    if 'cName' in request.GET:
        cName = request.GET["cName"]
        print(cName)
        # resultList = students.objects.filter(cName=cName) #select where   ## 網址輸入範例(單一)  http://192.168.59.17:8080/search_list/?cName=林雨媗
        resultList = students.objects.filter(cName__contains=cName) #select where like %林%(關鍵字)  ## 網址輸入範例  http://192.168.59.17:8080/search_list/?cName=%E6%9E%97

    else:
        resultList = students.objects.all().order_by("-cID")

    # for data in resultList:
    #     print(model_to_dict(data))
    # return HttpResponse("hello..")

    errormessage =""
    if not resultList:
        errormessage="無此資料"
    return render(request,"search_list.html", locals())

def search_name (request):
    # return HttpResponse ("hello.....")
    return render(request,"search_name.html", locals())

# 顯示(共)有幾筆資料
from django.db.models import Q
def index (request):
    # 從前端表單提交輸入內容，網址帶有site_serach參數的值
    if 'site_serach' in request.GET:   
        site_serach = request.GET["site_serach"] # 取單一關鍵字
        site_serach = site_serach.strip() #去前後去空白
        keywords = site_serach.split() #字串切割
        # print(keywords)
        # print(site_serach)

        # 同時取多個關鍵字_中間要用空格隔開。
        q_objects = Q()
        for keyword in keywords:
            q_objects.add( Q(cID__contains = keyword),Q.OR)
            q_objects.add( Q(cName__contains = keyword),Q.OR)
            q_objects.add( Q(cBirthday__contains = keyword),Q.OR)
            q_objects.add( Q(cEmail__contains = keyword),Q.OR)
            q_objects.add( Q(cPhone__contains = keyword),Q.OR)
            q_objects.add( Q(cAddr__contains = keyword),Q.OR)

        # resultList = students.objects.filter(
        #     Q(cID__contains = site_serach)|
        #     Q(cName__contains = site_serach)|
        #     Q(cBirthday__contains = site_serach)|
        #     Q(cEmail__contains = site_serach)|
        #     Q(cPhone__contains = site_serach)|
        #     Q(cAddr__contains = site_serach)
        # )
        resultList = students.objects.filter(q_objects)
    else:
        resultList = students.objects.all().order_by("cID") # 從資料庫取得students表格的所有資料。
    data_count = len(resultList) # 計算排序後的學生有多少筆。
    print(data_count)
    # for data in resultList:
    #     print(model_to_dict(data))
    # return HttpResponse ("hello.....")
    return render(request,"index.html", locals())

def post (request):
    # 傳入資料，按照前端資料填入[]內。
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        # print(f"{cName}:{cSex}:{cBirthday}:{cEmail}:{cPhone}:{cAddr}") #顯示在終端機，檢查完註解。
        add = students(cName=cName,cSex=cSex,cBirthday=cBirthday,
                       cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        
        add.save() # 加入save 儲存資料，回首頁新增一筆資料。
        return HttpResponse("已送出資料..")
    else:
        return render(request,"post.html", locals())
    
    
# 輸入id 接受其資料並修改。 
# 方法 1.[透過網址取得當筆資料的id，會在網址上顯示id ]→ (示範使用網址取得資料)
# 方法 2.[使用 GET 取得當筆資料]
def edit (request, id=None):  # 把資料放入指定的變數，顯示這筆資料內容 (名稱、性別..需要什麼就放入)。
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        # print(f"{cName}:{cSex}:{cBirthday}:{cEmail}:{cPhone}:{cAddr}") #顯示在終端機，檢查完註解。
        #把取得id的物件。 
        update = students.objects.get(cID=id)
        update.cName = cName
        update.cSex = cSex
        update.cBirthday = cBirthday
        update.cEmail = cEmail
        update.cPhone = cPhone
        update.cAddr = cAddr
        update.save()
        # return HttpResponse("已送出資料..")
        return redirect('/index/')
    
    else:
        # print(f"id={id}")
        datas = students.objects.get(cID=id) #取某一筆資料的id。

        # print(model_to_dict(datas))
        # 它將實例 (datas) 轉換為字典格式並輸出。舉例→ {'cID': 9, 'cName': '林心儀'}
        print(model_to_dict(datas)) #轉型
        return render(request, "edit.html" , locals())

## [快捷鍵_排列位移] 首先反白文字：1.按下 Tab鍵 右縮 ； 2.按下 Shift + Tab鍵 往左縮。

## [ redirect ] 將用戶從當前頁面_重定向到另一個 URL 的快捷方法。
## [ redirect ] 用途：當你希望用戶在完成某個操作（如提交表單、修改資料）後，跳轉到一個不同的頁面。
## 行為：瀏覽器會接收到一個新的請求，並向新的 URL 發送請求，這通常是頁面跳轉的一種方式。

## [ render ] 當你需要將資料顯示給用戶，並生成一個 HTML 頁面時，會使用 render。
## [ render ] 用途：用來將資料與模板合併，生成一個 HTML 頁面，並將該頁面返回給用戶。
## 行為：不會進行頁面跳轉，而是渲染模板並將結果返回給用戶。


# 刪除單筆資料
def delete (request, id=None): 
    print(id)
    if request.method == "POST":
        delete = students.objects.get(cID=id)
        delete.delete()
        # return HttpResponse("已送出資料..")
        return redirect('/index/')  # 若按下刪除，則回傳'/index/'樣板(顯示每筆資料)。
    else:
        datas = students.objects.get(cID=id) #取某一筆資料的id。
        print(model_to_dict(datas))
    return render(request, "delete.html" , locals()) # 沒有刪除則回傳刪除前的資料。

# 在 "delete.html" 樣板 句尾後面 是"POST"→ <form action="/delete/{{datas.cID}}/" method="POST">
