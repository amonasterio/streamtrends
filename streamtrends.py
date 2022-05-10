import streamlit as st, pandas as pd, time, sys,datetime           
from pytrends.request import TrendReq
from requests.packages.urllib3.util.retry import ResponseError

def dateToStr(fecha):
    return fecha.strftime("%Y-%m-%d")

st.title("Consulta masiva a Google Trends")
st.text("Devuelve el interés a lo largo del tiempo para las consultas que requiramos")
start_date, end_date = st.date_input("Seleccione rango de fechas", [datetime.date(2022,1,1), datetime.date.today()])
geolocalizacion=st.text_input("Geolocalización (Código de país con dos caracteres: ES, GB, DE, IT...", value='ES')
f_entrada=st.file_uploader('CSV con términios a estudiar', type='csv')
if start_date is not None and end_date is not None:
    if f_entrada is not None:
        crawldf = pd.read_csv(f_entrada,header=None)
        nombres= crawldf[0].tolist()
        st.text(nombres)
        pytrends = TrendReq(hl='es-ES', tz=60)
        dfFinal= pd.DataFrame()
        cont=0
        for row in nombres:
            kw_list = [row] 
            # build the payload
            try:
                pytrends.build_payload(kw_list, timeframe=dateToStr(start_date)+' '+dateToStr(end_date), geo=geolocalizacion)
                # store interest over time information in df
                df = pytrends.interest_over_time()
                if not df.empty:
                    df=df.drop(['isPartial'],axis=1) #Eliminamos la columna 'isPartial'
                    if cont == 0: 
                        dfFinal=df
                    else:  
                        lista=df[df.columns.values[0]].values
                        dfFinal[df.columns.values[0]]=lista
                    time.sleep(1)
                cont=cont+1
            except ResponseError as e:
                st.error("Response error: "+e.strerror)
        csv=dfFinal.to_csv().encode('utf-8')
        st.download_button(
        label="Descargar como CSV",
        data=csv,
        file_name='salida.csv',
        mime='text/csv',
        )
        st.line_chart(dfFinal)