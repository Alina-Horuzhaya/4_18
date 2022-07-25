import cgi
import html
import qrcode


## Собираем строку данных для формирования qr-code.
#  @param values_from_form: Dictionary cо значениями с формы.
#  @return: filename (str) - название файла
def generate_qr_and_save_img(values_from_form: dict = None) -> str:
    if values_from_form is None:
        values_from_form = {}
    data = "BEGIN:VCARD\n" + "VERSION:3.0\n" + "FN:" + str(values_from_form["fio"]) +\
           '\nTEL;TYPE=Сотовый телефон:' + str(values_from_form["cell"]) +\
           '\nEMAIL;TYPE=Электронная почта:' + str(values_from_form["email"]) +\
           '\nX-SOCIALPROFILE;X-USER=@' + str(values_from_form["social"]) + ";TYPE=Telegram:https://t.me/" + str(values_from_form["social"]) +\
           "\nURL;TYPE=Ссылка на профиль GitHab:" + "github.com/" + str(values_from_form["git"]) +\
           "\nNOTE:Языки программирования: " + str(values_from_form["note_1"]) +\
           " | Крупные проекты: " + str(values_from_form["note_2"]) + "\nEND:VCARD"

    filename = "qr_it_" + str(values_from_form["fio"]) + ".png"
    # создаем код
    img = qrcode.make(data)
    # сохраняем в файл на сервере
    img.save(filename)
    return filename


## Экранирование спецсимволов-html.
#  @param values_from_form: Dictionary cо значениями с формы.
#  @return: filename (str) - название файла
def escaping_special_chars(values_from_form: dict = None) -> str:
    if values_from_form is None:
        values_from_form = {}
    for key, value in values_from_form.items():
        values_from_form[key] = html.escape(value)
    return generate_qr_and_save_img(values_from_form)


## Обработчик формы создания стандартной визитки. получение данных из формы create_it.html
#  @return: filename (str) - название файла
def process_form_and_generate_qr() -> str:
    form = cgi.FieldStorage()
    values_dict = {"fio": form.getfirst("FIO"), "cell": form.getfirst("CELL"), "email": form.getfirst("EMAIL"),
                   "social": form.getfirst("SOCIAL", "-"), "git": form.getfirst("GIT", "-"),
                   "note_1": form.getfirst("NOTE_1", "-"), "note_2": form.getfirst("NOTE_2", "-")}
    return escaping_special_chars(values_from_form=values_dict)


filename = process_form_and_generate_qr()

# формирование итоговой страницы
print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Создание визитки IT</title>
            <style>
            
            * {
	            -webkit-box-sizing: border-box;
	            -moz-box-sizing: border-box;
	            box-sizing: border-box;
	        }
            
            A {
                text-decoration: none;
                color: black;
            }

            A:hover {
                text-decoration: none;
                color: black;
            }
        
            body {
                position: relative;
                font-family: 'Noto Sans', sans-serif;
                line-height: 1.4;
                min-width: 320px;
                min-height:812px;
                overflow-x: hidden;
                height: auto;
                background: linear-gradient(45deg, #edf1cf, #58b6b9);
            }
            
            button {
                margin-top: 40px;
                display: inline-block;
                padding: 10px 30px;
                font-size: 12px;
                border: none;
                background-color: rgba(	255, 160, 122, 0.5);
                font-color: black;
                text-transform: uppercase;
                border-radius: 8px;
                font-weight: 700;
                background-color: rgba(96, 210, 214, 0.3);
                box-shadow: 0px 5px 15px rgba(78, 165, 134, 0.6);
            }
            
            button:hover {
                box-shadow: 0px 5px 15px rgba(78, 165, 134, 0.6);
                transform: scale(1.05);
            }
            
            h2 {
                margin-top: 30px;
                font-size: 30px;
            }
            
            img {
                max-width: 30%;
                border: thick double #58b6b9;
            }

            </style>
        </head>
        <body align=\"center\">""")

# показываем код на форме
print("<br> <br> <h2>Ваша QR-визитка готова! Кликните по ней для сохранения </h2>")
# внутри ссылки, чтобы можно было сохранить, нажав на сам код
print("<a href=\"../" + str(filename) + "\" download>")
print("<img id=\"qrc\" src=\"../" + str(filename) + "\"/>")
print("</a>")
print("<br> <button><a href=\create_it.html>")
print("Назад </button></a>")

print("""</body>
        </html>""")
