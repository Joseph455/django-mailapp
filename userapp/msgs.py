
def confirm_email_message(id_signature, email_signature, link):
    html_message = ("""
            <h2>M-Sender</h2>
            <p> This link will expire in five minutes <a href=\"http://""" + link +  "/" + id_signature + "/" + email_signature + "\"" + ">click to confirm your email</a></p>" +
            """<p> if you did not make this request please ignore</p>""")
    text_message = " Use This link to confirm your email http://%s" %link + "/" + id_signature + "/" + email_signature + ' link will expires in five minutes'
    return html_message, text_message


