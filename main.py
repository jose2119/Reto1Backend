import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from tkinter import *
from tkinter.ttk import Treeview

listaCambios= []
url = requests.get("https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx")


class Formulario:
    def __init__(self,window):
        self.wind = window
        self.wind.title('Cambios de Moneda')
        self.wind.geometry('700x600')
        self.wind.configure(bg='#49A')

        btnEntrada = Button(text='Importar',command=self.scrapping_tipocambio)
        btnEntrada.grid(row=0,column=1,columnspan=1,sticky=W+E)
            
        self.TrvCambios = Treeview(height=10,columns=('#1','#2'))
        self.TrvCambios.grid(row=1,column=0,columnspan=3,padx=10)
        self.TrvCambios.heading('#0',text='Moneda',anchor=CENTER)
        self.TrvCambios.heading('#1',text='compra',anchor=CENTER)
        self.TrvCambios.heading('#2',text='venta',anchor=CENTER)
        
        btnSalida=Button(text='Exportar',command=self.exportCambios)
        btnSalida.grid(row=2,column=1,columnspan=1,sticky=W+E)
    
    def scrapping_tipocambio(self):
        if(url.status_code == 200):
            print("pagina encontrada")
            html = BeautifulSoup(url.text,'html.parser')
            tabla = html.find_all('table',{'id':'ctl00_cphContent_rgTipoCambio_ctl00'})
            for i in range(7):
                fila = html.find('tr',{'id':'ctl00_cphContent_rgTipoCambio_ctl00__'+str(i)}) 
                moneda = fila.find('td',{'class':'APLI_fila3'})
                montos = fila.find_all('td',{'class':'APLI_fila2'})
                dicMoneda = {
                    'moneda': moneda.get_text(),
                    'compra': montos[0].get_text(),
                    'venta': montos[1].get_text()
                }
                listaCambios.append(dicMoneda)
                self.TrvCambios.insert('',END,text=moneda.get_text(),values=[montos[0].get_text(),montos[1].get_text()])
        
        else:
            print("error " + str(url.status_code))
    
    def exportCambios(self):
        TipoCambio=""
        for dictMoneda in listaCambios:
            for clave,valor in dictMoneda.items():
                TipoCambio+=valor
                if clave!='venta':
                    TipoCambio+=','
                else:
                    TipoCambio+='\n'
        fw=open('tiposDeCambio.csv','w')
        fw.write(TipoCambio)
        fw.close()
            

if __name__ == "__main__" :
    window = Tk()
    app = Formulario(window)
    window.mainloop()