import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_mail(
    sender,
    password,
    recipient,
    title,
    content,
    mail_host="smtp.163.com",
    port=25,
    file=None,
):
    """
    发送邮件函数，默认使用163smtp
    :param sender: 邮箱账号 xx@163.com
    :param password: 邮箱密码
    :param recipient: 邮箱接收人地址，多个账号以逗号隔开
    :param title: 邮件标题
    :param content: 邮件内容
    :param mail_host: 邮箱服务器
    :param port: 端口号
    :return:
    """
    if file:
        msg = MIMEMultipart()
        # 构建正文
        part_text = MIMEText(content)
        msg.attach(part_text)  # 把正文加到邮件体里面去
        # 构建邮件附件
        part_attach = MIMEApplication(open(file, "rb").read())  # 打开附件
        part_attach.add_header(
            "Content-Disposition", "attachment", filename="capture.mp4"
        )  # 为附件命名
        msg.attach(part_attach)  # 添加附件
    else:
        msg = MIMEText(content)  # 邮件内容
    msg["Subject"] = title  # 邮件主题
    msg["From"] = sender  # 发送者账号
    msg["To"] = recipient  # 接收者账号列表
    smtp = smtplib.SMTP(mail_host, port=port)
    smtp.login(sender, password)  # 登录
    smtp.sendmail(sender, recipient, msg.as_string())
    smtp.quit()
