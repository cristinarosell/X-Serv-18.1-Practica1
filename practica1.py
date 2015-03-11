#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Acortador de urls
"""

import webapp


class AcortadorApp (webapp.webApp):

    # Declare and initialize content
    diccUrls_reales = {}
    diccUrls_cortas = {}
    url_corta = -1

    def parse(self, request):
        metodo = request.split(' ', 2)[0]
        recurso = request.split(' ', 2)[1]

        if metodo == "POST":
            cuerpo = request.split('\r\n\r\n', 1)[1].split('=')[1]
            cuerpo = cuerpo.replace('+', '')
        elif metodo == "GET":
            cuerpo = ""
        return (metodo, recurso, cuerpo)

    def process(self, resourceName):

        (metodo, recurso, cuerpo) = resourceName

        formulario = '<form action="" method="POST">'
        formulario += 'Introducir url : <input type="text" name="valor">'
        formulario += '<input type="submit" value="Enviar">'
        formulario += '</form>'

        if metodo == "POST":
            #el cuerpo del POST es la url
            if cuerpo == "":
                httpCode = "404 Not Found"
                htmlBody = ("<html><body>Error</body></html>")
                return (httpCode, htmlBody)

            else:
                if cuerpo.find("http") == -1:
                    cuerpo = "http://" + cuerpo
                else:
                    cuerpo = cuerpo.replace('%3A%2F%2F', '://')

            if cuerpo in self.diccUrls_reales:
                self.url_corta = self.diccUrls_reales[cuerpo]
            else:
                self.url_corta = self.url_corta + 1
                self.diccUrls_reales[cuerpo] = self.url_corta
                self.diccUrls_cortas[self.url_corta] = cuerpo

            httpCode = "200 OK"
            url_l = "<a href ='" + cuerpo + "'> Url larga: " + cuerpo + "</a>"
            url_c = ("<a href ='http://localhost:1234/" + str(self.url_corta) +
                     "'> Url corta : " + str(self.url_corta) + "</a>")
            htmlBody = ("<html><body> URLS: </br>" + url_l + "</br>" +
                        url_c + "</br>" + "</body></html>")
        else:
            if recurso == "/":
                httpCode = "200 OK"
                htmlBody = ("<html><body>" + str(self.diccUrls_reales) +
                            formulario + "</body></html>")
            else:
                recurso = int(recurso.split('/')[1])
                if recurso in self.diccUrls_cortas:
                    httpCode = ("300 Multiple Choices\nLocation: " +
                                self.diccUrls_cortas[recurso])
                    htmlBody = "<html><body>Redirigiendo</body></html>"
                else:
                    httpCode = "404 Not Found"
                    htmlBody = ("<html><body> Error:Recurso no disponible" +
                                "</body></html>")

        return (httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = AcortadorApp("localhost", 1234)
