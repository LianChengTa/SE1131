簡易編輯方法：
--------------------------------------------------------------------------------------------------------------------------
![{830C6684-0C3A-4CD4-90B5-9D464BCD9BCE}](https://github.com/user-attachments/assets/858c9614-758f-4b9f-a116-3326e806f4ac)

以上六項是關鍵

關於static：
--------------------------------------------------------------------------------------------------------------------------
![{3C0E3FB1-0E89-49CD-AA07-B352367E825C}](https://github.com/user-attachments/assets/d9ff3960-8e06-4a18-8a96-3fc8644a694e)

這是用來放一些.css或各種icon,圖片的地方

關於templates：
--------------------------------------------------------------------------------------------------------------------------
![{E143B336-1FA2-4150-9FB3-6EFC58D52AAA}](https://github.com/user-attachments/assets/ed00b591-3a9b-4c49-8a9a-39a2ba99eca5)

這裏是用來放置所有.html的地方

關於html的撰寫方式：
--------------------------------------------------------------------------------------------------------------------------
由於所有的東西都放到static裏面去了。
所以所有的路徑都要做更改，例如原本是../images/image.png，現在就要改成{% static 'image.png' %}

也就是{% static '圖片在static文件中的路徑' %}

![image](https://github.com/user-attachments/assets/4f5392b4-4147-4743-b466-3cc5d73edbd7)

另外，url的部分也是同樣的概念，改成{% url '指定路徑' %}
指定路徑是哪裏？
要看urls.py裏面怎麽寫

![{50DC4E77-991E-47DC-8517-DFEA2AA75868}](https://github.com/user-attachments/assets/d9a31150-bbe5-4248-819f-690f26a26570)

可以看到裏面的name，是什麽，指定路徑就寫什麽

例：

![image](https://github.com/user-attachments/assets/51cc24a0-ea83-4f6c-b86c-e11677720c54)

register對應到上面urls.py的register path。


關於urls.py：
--------------------------------------------------------------------------------------------------------------------------
這裏是用來寫所有的路徑（或者説網址）的地方，可以指定名稱，跟用來做什麽事情（透過views.py）

![image](https://github.com/user-attachments/assets/7dd34430-d762-4aca-bd41-2c9c1e8efbc2)

前面指定路徑，後面指定名稱，中間紅綫部分是指定做什麽事情的地方。

關於views.py
--------------------------------------------------------------------------------------------------------------------------
這裏是寫主要function的地方！！！！！！！！！！
很重要

![{F9D4EE2C-82CB-4E86-9E40-D4E7FDD14AA7}](https://github.com/user-attachments/assets/2caf329b-706f-484d-b1df-f79ead0e7ee3)

以上為一個小例子：可以看urls.py中的detail指到這個function，所以這個function會被執行，然後render一個.html文件回去，顯示在用戶的瀏覽器上

以下爲實際流程示意圖：


![image](https://github.com/user-attachments/assets/ddeff031-41d2-47dc-806f-50250c7571a6)

對應到

![{9942E3EE-A59D-484E-966C-DF9DBCF34D6D}](https://github.com/user-attachments/assets/c524e785-5f80-4149-b902-04d5e07e0255)

![image](https://github.com/user-attachments/assets/7170ef0c-dea5-47c2-89f4-fc7ffdd121b2)

![{C0D18060-8DD3-42BA-B92D-FD71EFC31EC1}](https://github.com/user-attachments/assets/03a47595-421a-4682-a28b-f7b0d1470426)

得到：

![{4258EA94-CA69-45D9-BB80-7556509F13F8}](https://github.com/user-attachments/assets/57dce0da-73f9-43ab-9836-1e7c12c859b0)

以上就是views.py的用處展示


關於forms.py：
--------------------------------------------------------------------------------------------------------------------------
這裏是編輯表單用的地方，例如登入表單，注冊表單

![{A04EEA57-D684-4F92-9BDD-5BAC25FDE9AD}](https://github.com/user-attachments/assets/9da0e5ef-2328-4b33-a3e9-ee2b4c531193)

詳情可以上網查查看，蠻多東西可以設定的，利用好的話.html甚至可以很簡單，例如：

![{1B204523-FEBC-4E95-94BA-7855AE189663}](https://github.com/user-attachments/assets/baba201d-0524-4564-9476-cda56400a996)

它會自動把表單中所設定的所有東西以html的語法添加進.html中，非常方便。

關於models.py：
--------------------------------------------------------------------------------------------------------------------------
這裏是設定資料庫裏面所有table長什麽樣的地方

以下為示意圖：

![{497C6573-22CE-4D9A-B91D-1A7CCA837BD7}](https://github.com/user-attachments/assets/dc4e5956-b073-41f9-bc95-ad6f7eea64dc)

圖中設定了一個user_account的table，繼承了AbstactUser模型，自行添加了一項studentid（可以自己設定各個column的attribute）

![image](https://github.com/user-attachments/assets/b36e4789-6838-448a-b3fa-cadee28b9e92)

所以最後的資料庫會長這樣，有個自己創建的user_account的table（因爲在django中它是under一個叫webpage的app，所以系統命名為webpage_user_account，實際使用可以忽略名稱問題...應該），裏面有從AbstactUser繼承的各種column，還有自己添加的studentid






