import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.image import MIMEImage

# из библы фласк импортим нужные нам функции
from flask import Flask, render_template, send_from_directory, request, Response
# после мы создаем объект нашего приложения
app = Flask(__name__)

# такая запись является перегрузкой функции (когда мы функции добавляем еще какие-то свойства)
# здесь мы добавили прослушивание URL адреса /index_2
# и сказали что разрешено к нему обращаться только методами GET и POST
@app.route("/index_2", methods=["GET", "POST"])
def my_func():
    return "Text  fsf sf adsg sdg"

def get_():
    return {'u': 'homeituniversity@gmail.com', 'p': '123'}

def send_email(mail_to, subject, text, files=None, need_attach_to_body=False):
    try:

        assert isinstance(mail_to, list)
        smtp_user = get_()['u']
        smtp_pwd = get_()['p']


        # первым делом вы должны создать пустой объект письма
        msg = MIMEMultipart()

        # затем добавить в него кому от кого дату и тему письма
        msg['From'] = smtp_user
        msg['To'] = COMMASPACE.join(mail_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        # ЗАТЕМ если  вас есть файлы
        if files is not None:

            for i, f in enumerate(files) or enumerate([]):


                # для того чтобы вложить файл как аттач вам нужно открыть его на чтение байтов rb
                with open(f, "rb") as fil:
                    # затем прочитать его в новый объект MIMIApplication
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(f) # это имя файла которое будет видеть пользователь получивший письмо
                    )

                # после того как файл прочитали, нужно добавить в созданный объект заголовок с указанием того,  то мы приложили к письму файл как аттач
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                #затем кладем этот объект в тело письма при помощи метода аттач
                msg.attach(part)

                # ессли мы хотим вложить в письмо картинку как картинку (а не аттач)
                if need_attach_to_body and (f.lower().__contains__('.png') \
                                            or f.lower().__contains__('.jpg') \
                                            or f.lower().__contains__('.jpeg') \
                                            or f.lower().__contains__('.gif') \
                                            or f.lower().__contains__('.tif')):
                    # то мы открываем ее на чтение байтов rb
                    fp = open(f, 'rb')
                    # создаем объект MIMEImage и передаем в него данные из файла
                    msgImage = MIMEImage(fp.read())
                    fp.close()

                    # после прочтения обязательно ддобавляем заголовок, в который помещаем имя нашего файла(в лбьом формате, оно нужно чисто только для вас)
                    msgImage.add_header('Content-ID', '<image{}>'.format(i))

                    # после добавления этого объекта в тело письма
                    msg.attach(msgImage)

                    # обязательно в тексте письма должен быть добавлен тег img в котором будет происходить отрисовка картинки,
                    # а источником нужно указать  cid:ваше имя что вы дали файлу ступенькой выше
                    text += '<br><img src="cid:image{}">'.format(i)
        # добавляем в сообщение текст сообщения
        msg.attach(MIMEText(text, 'html'))

        # если нужно отправлять письма внутри банка то раскомментируйте следующие строки
        # smtp = smtplib.SMTP("outlook.homecredit.ru", 587)
        # smtp.ehlo()
        # smtp.starttls()

        # а эту закомментируйте
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        smtp.ehlo()
        smtp.login(smtp_user, smtp_pwd)

        smtp.sendmail(smtp_user, mail_to, msg.as_string())

        smtp.close()
        return True
    except Exception as e:
        print(e)
        return False



@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/index_hard", methods=["GET", "POST"])
def index_hard():
    return render_template("index_hard.html", lastname="Иванов", firstname="Иван")

@app.route("/download_file", methods=["GET", "POST"])
def download_file():
    return send_from_directory(directory="files", filename="1.png", as_attachment=False)

@app.route("/parse_form", methods=["GET", "POST"])
def parse_form():
    if request.method == "GET":
        return render_template("forms.html")
    else:
        lastname = request.form.get('lastname', "Empty")
        firstname = request.form.get('firstname', "Empty")
        return f"<div>Привет {lastname} {firstname}</div>"

@app.route("/viber_proxy", methods=["POST"])
def viber_proxy(self):

    self.logger.info("remote_addr " + str(request.remote_addr))
    if str(request.remote_addr) == "10.6.142.155" and hmac.new(
            bytes(self.config['Messenger']['token_prod'].encode('ascii')), msg=request.get_data(),
            digestmod=hashlib.sha256).hexdigest() == request.headers.get('X-Viber-Content-Signature'):
        jsreq = request.get_json(force=True, silent=True)
        try:
            if jsreq['event'] == 'message' and self.psql.viber_message_is_in_db(
                    message_id=jsreq['message_token']) == False:
                self.psql.viber_reciever(jsreq, jsreq['sender']['id'], jsreq['message_token'])
        except Exception as e:
            self.logger.exception("Exception " + str(e))
        try:
            deliverid = {
                "event": "delivered",
                "timestamp": str(jsreq['timestamp']),
                "message_token": str(jsreq['message_token']),
                "user_id": str(jsreq['sender']['id'])
            }
            deliverid = str(deliverid).encode("UTF-8")
        except:
            deliverid = Response(status=200)
        return deliverid
    else:
        return Response(status=403)

@app.route('/snd')
def snd():
    send_email(
        mail_to=['xxshramxx@yandex.ru'],
        subject="Test mail with image",
        text='This is test mail',
        files=[r"C:\Users\VCherkozyanov\PycharmProjects\FlaskExample\files\1.png"],
        need_attach_to_body=True)

    return Response(status=200)


# если мы хотим перерисовать страницу ошибки со стандартной нам нужно использовать следующие конструкции
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")



if __name__ == '__main__':
    # обязательно запускаем наше приложение
    # host=0.0.0.0 значит что мы можем обратиться к нашему веб серверу через имя сервера, localhost, ip address
    # порт это указание по какому порту доступен будет веб ссервер
    # если указать не 80 порт то url  в браузере будет выглядеть так
    # например если port=3333 то http://localhost:3333/
    app.run(host="0.0.0.0", port=80, debug=True)