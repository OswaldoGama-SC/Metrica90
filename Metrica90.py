import streamlit as st
import pandas as pd
from datetime import datetime
import time

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

st.set_page_config(page_title="Métrica 90 PRO", layout="centered")

# -----------------------------
# SESSION STATE
# -----------------------------
if "registro" not in st.session_state:
    st.session_state.registro = []

if "plantilla" not in st.session_state:
    st.session_state.plantilla = []

if "jugador_activo" not in st.session_state:
    st.session_state.jugador_activo = None

if "inicio_partido" not in st.session_state:
    st.session_state.inicio_partido = None

if "tiempo_acumulado" not in st.session_state:
    st.session_state.tiempo_acumulado = 0

if "notas" not in st.session_state:
    st.session_state.notas = ""

# -----------------------------
# FUNCIONES
# -----------------------------
def obtener_tiempo():
    if st.session_state.inicio_partido:
        delta = datetime.now() - st.session_state.inicio_partido
        total = st.session_state.tiempo_acumulado + delta.total_seconds()
    else:
        total = st.session_state.tiempo_acumulado

    minutos = int(total // 60)
    segundos = int(total % 60)
    return minutos, segundos

def obtener_minuto():
    m, _ = obtener_tiempo()
    return m

def registrar_evento(jugador, accion, resultado):
    if jugador is None:
        st.warning("Selecciona un jugador")
        return

    evento = {
        "hora": datetime.now().strftime("%H:%M:%S"),
        "minuto": obtener_minuto(),
        "jugador": jugador,
        "accion": accion,
        "resultado": resultado
    }
    st.session_state.registro.append(evento)

# -----------------------------
# HEADER
# -----------------------------
st.title("⚽ MÉTRICA 90 PRO")

# -----------------------------
# DATOS PARTIDO
# -----------------------------
st.subheader("📋 Datos del partido")

col1, col2, col3, col4 = st.columns(4)

with col1:
    equipo = st.text_input("Equipo")

with col2:
    rival = st.text_input("Rival")

with col3:
    marcador = st.text_input("Marcador")

with col4:
    fecha_partido = st.date_input("Fecha")

# -----------------------------
# RELOJ
# -----------------------------
st.subheader("⏱️ Partido")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ Iniciar"):
        st.session_state.inicio_partido = datetime.now()
        st.session_state.tiempo_acumulado = 0

with col2:
    if st.button("⏸️ Pausar"):
        if st.session_state.inicio_partido:
            delta = datetime.now() - st.session_state.inicio_partido
            st.session_state.tiempo_acumulado += delta.total_seconds()
            st.session_state.inicio_partido = None

with col3:
    if st.button("🔄 Reanudar"):
        st.session_state.inicio_partido = datetime.now()

placeholder = st.empty()

while st.session_state.inicio_partido:
    m, s = obtener_tiempo()
    placeholder.markdown(f"### ⏱️ {m:02d}:{s:02d}")
    time.sleep(1)

m, s = obtener_tiempo()
placeholder.markdown(f"### ⏱️ {m:02d}:{s:02d}")

# -----------------------------
# PLANTILLA
# -----------------------------
st.subheader("📋 Plantilla")

nuevo = st.text_input("Jugador")

if st.button("➕ Añadir jugador"):
    if nuevo and nuevo not in st.session_state.plantilla:
        st.session_state.plantilla.append(nuevo)

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3 = st.tabs(["⚡ Registro", "📊 Eventos", "📈 Estadísticas"])

# -----------------------------
# TAB 1 - REGISTRO (CON TODOS TUS BOTONES)
# -----------------------------
with tab1:

    st.subheader("👥 Jugadores")

    cols = st.columns(4)

    for i, j in enumerate(st.session_state.plantilla):
        label = f"🟢 {j}" if j == st.session_state.jugador_activo else j
        if cols[i % 4].button(label):
            st.session_state.jugador_activo = j

    st.info(f"Jugador activo: {st.session_state.jugador_activo}")

    st.markdown("### ⚡ Acciones")

    # PASES
    st.markdown("#### 🟡 Pases")
    c1, c2, c3 = st.columns(3)

    if c1.button("Pase ✔️"):
        registrar_evento(st.session_state.jugador_activo, "Pase", "Exitoso")

    if c2.button("Pase ❌"):
        registrar_evento(st.session_state.jugador_activo, "Pase", "Fallado")

    if c3.button("Asistencia 🅰️"):
        registrar_evento(st.session_state.jugador_activo, "Asistencia", "Exitoso")

    # TIROS
    st.markdown("#### 🔴 Tiros")
    c1, c2, c3 = st.columns(3)

    if c1.button("Gol ⚽"):
        registrar_evento(st.session_state.jugador_activo, "Tiro", "Gol")

    if c2.button("Al arco 🎯"):
        registrar_evento(st.session_state.jugador_activo, "Tiro", "Al Arco")

    if c3.button("Desviado"):
        registrar_evento(st.session_state.jugador_activo, "Tiro", "Desviado")

    # DUELOS
    st.markdown("#### ⚔️ Duelos")
    c1, c2 = st.columns(2)

    if c1.button("1vs1 Of ✔️"):
        registrar_evento(st.session_state.jugador_activo, "1vs1 ofensivo", "Exitoso")

    if c2.button("1vs1 Of ❌"):
        registrar_evento(st.session_state.jugador_activo, "1vs1 ofensivo", "Fallado")

    if c1.button("1vs1 Def ✔️"):
        registrar_evento(st.session_state.jugador_activo, "1vs1 defensivo", "Exitoso")

    if c2.button("1vs1 Def ❌"):
        registrar_evento(st.session_state.jugador_activo, "1vs1 defensivo", "Fallado")

    # DEFENSA
    st.markdown("#### 🛡 Defensa")
    c1, c2, c3 = st.columns(3)

    if c1.button("Recuperación"):
        registrar_evento(st.session_state.jugador_activo, "Recuperación", "Exitoso")

    if c2.button("Intercepción"):
        registrar_evento(st.session_state.jugador_activo, "Intercepción", "Exitoso")

    if c3.button("Pérdida"):
        registrar_evento(st.session_state.jugador_activo, "Pérdida", "Fallado")

    # OTROS
    st.markdown("#### 📌 Otros")
    c1, c2, c3 = st.columns(3)

    if c1.button("Centro"):
        registrar_evento(st.session_state.jugador_activo, "Centro", "Exitoso")

    if c2.button("Falta cometida"):
        registrar_evento(st.session_state.jugador_activo, "Falta", "Cometida")

    if c3.button("Falta recibida"):
        registrar_evento(st.session_state.jugador_activo, "Falta", "Recibida")

    if c1.button("Amarilla"):
        registrar_evento(st.session_state.jugador_activo, "Tarjeta Amarilla", "-")

    if c2.button("Roja"):
        registrar_evento(st.session_state.jugador_activo, "Tarjeta roja", "-")

# -----------------------------
# DATAFRAME
# -----------------------------
df = pd.DataFrame(st.session_state.registro)

# -----------------------------
# TAB 2
# -----------------------------
with tab2:
    st.dataframe(df, use_container_width=True)

# -----------------------------
# TAB 3 + PDF PRO
# -----------------------------
with tab3:

    if not df.empty:

        jugador_sel = st.selectbox("Selecciona jugador", df["jugador"].unique())
        df_j = df[df["jugador"] == jugador_sel]

        # MÉTRICAS INDIVIDUALES
        pases_ok = len(df_j[(df_j["accion"]=="Pase") & (df_j["resultado"]=="Exitoso")])
        pases_tot = len(df_j[df_j["accion"]=="Pase"])
        ef_pases = (pases_ok/pases_tot*100) if pases_tot>0 else 0

        tiros_arco = len(df_j[df_j["resultado"]=="Al Arco"])
        tiros_desviados = len(df_j[df_j["resultado"]=="Desviado"])

        duelos_of = len(df_j[df_j["accion"]=="1vs1 ofensivo"])
        duelos_of_gan = len(df_j[(df_j["accion"]=="1vs1 ofensivo") & (df_j["resultado"]=="Exitoso")])
        ef_duelos_of = (duelos_of_gan/duelos_of*100) if duelos_of>0 else 0

        duelos_def = len(df_j[df_j["accion"]=="1vs1 defensivo"])
        duelos_def_gan = len(df_j[(df_j["accion"]=="1vs1 defensivo") & (df_j["resultado"]=="Exitoso")])
        ef_duelos_def = (duelos_def_gan/duelos_def*100) if duelos_def>0 else 0

        recuperaciones = len(df_j[df_j["accion"]=="Recuperación"])
        perdidas = len(df_j[df_j["accion"]=="Pérdida"])

        st.subheader("📊 Rendimiento individual")

        col1, col2, col3 = st.columns(3)

        col1.metric("% Pases", round(ef_pases,1))
        col1.metric("Tiros al arco", tiros_arco)

        col2.metric("Tiros desviados", tiros_desviados)
        col2.metric("% Duelos Of", round(ef_duelos_of,1))

        col3.metric("% Duelos Def", round(ef_duelos_def,1))
        col3.metric("Recuperaciones", recuperaciones)

        st.metric("Pérdidas", perdidas)

        st.session_state.notas = st.text_area("Observaciones")


        # -----------------------------
        # PDF FULL PRO
        # -----------------------------
        def generar_pdf():
            doc = SimpleDocTemplate("reporte.pdf", pagesize=letter)
            styles = getSampleStyleSheet()
            contenido = []

            estilo = styles["Title"]
            estilo.alignment = 1

            contenido.append(Paragraph(f"Reporte de rendimiento individual vs {rival}", estilo))
            contenido.append(Spacer(1, 15))

            contenido.append(Paragraph(f"Equipo: {equipo}", styles["Normal"]))
            contenido.append(Paragraph(f"Fecha: {fecha_partido}", styles["Normal"]))
            contenido.append(Spacer(1, 20))

            # RESUMEN EQUIPO TABLA
            contenido.append(Paragraph("Resumen del equipo", styles["Heading2"]))

            resumen_equipo = [
                ["Métrica","Valor"],
                ["% Pases", round((len(df[(df["accion"]=="Pase") & (df["resultado"]=="Exitoso")]) / len(df[df["accion"]=="Pase"]) *100) if len(df[df["accion"]=="Pase"])>0 else 0,1)],
                ["Tiros al arco", len(df[df["resultado"]=="Al Arco"])],
                ["Tiros desviados", len(df[df["resultado"]=="Desviado"])],
                ["% Duelos Of Ganados", round((len(df[(df["accion"]=="1vs1 ofensivo") & (df["resultado"]=="Exitoso")]) / len(df[df["accion"]=="1vs1 ofensivo"]) *100) if len(df[df["accion"]=="1vs1 ofensivo"])>0 else 0,1)],
                ["% Duelos Def Ganados", round((len(df[(df["accion"]=="1vs1 defensivo") & (df["resultado"]=="Exitoso")]) / len(df[df["accion"]=="1vs1 defensivo"]) *100) if len(df[df["accion"]=="1vs1 defensivo"])>0 else 0,1)],
                ["Recuperaciones", len(df[df["accion"]=="Recuperación"])],
                ["Pérdidas", len(df[df["accion"]=="Pérdida"])]
            ]

            contenido.append(Table(resumen_equipo))
            contenido.append(Spacer(1,20))

            # STATS POR JUGADOR
            stats = []
            for j in df["jugador"].unique():
                d = df[df["jugador"]==j]

                pases_ok = len(d[(d["accion"]=="Pase") & (d["resultado"]=="Exitoso")])
                pases_tot = len(d[d["accion"]=="Pase"])
                ef_pases = (pases_ok / pases_tot *100) if pases_tot>0 else 0

                # TIROS
                tiros_arco = len(d[d["resultado"]=="Al Arco"])
                tiros_desv = len(d[d["resultado"]=="Desviado"])

                # DUELOS OFENSIVOS
                duelos_of_gan = len(d[(d["accion"]=="1vs1 ofensivo") & (d["resultado"]=="Exitoso")])
                duelos_of_per = len(d[(d["accion"]=="1vs1 ofensivo") & (d["resultado"]=="Fallado")])
                duelos_of_tot = duelos_of_gan + duelos_of_per
                ef_duelos_of = (duelos_of_gan / duelos_of_tot *100) if duelos_of_tot>0 else 0

                # DUELOS DEFENSIVOS
                duelos_def_gan = len(d[(d["accion"]=="1vs1 defensivo") & (d["resultado"]=="Exitoso")])
                duelos_def_per = len(d[(d["accion"]=="1vs1 defensivo") & (d["resultado"]=="Fallado")])
                duelos_def_tot = duelos_def_gan + duelos_def_per
                ef_duelos_def = (duelos_def_gan / duelos_def_tot *100) if duelos_def_tot>0 else 0

                # OTROS
                recuperaciones = len(d[d["accion"]=="Recuperación"])
                perdidas = len(d[d["accion"]=="Pérdida"])

                stats.append([
                    j,
                    round(ef_pases,1),
                    tiros_arco,
                    tiros_desv,
                    duelos_of_gan,
                    duelos_of_per,
                    round(ef_duelos_of,1),
                    duelos_def_gan,
                    duelos_def_per,
                    round(ef_duelos_def,1),
                    recuperaciones,
                    perdidas
                ])

            headers = ["Jugador", "% Pases", "Tiros Arco", "Tiros Desv", "Duelos Of Gan", "Duelos Of Perd", "% Duelos Of", "Duelos Def Gan", "Duelos Def Perd", "% Duelos Def", "Recup", "Pérdidas"]

            contenido.append(Paragraph("Tabla completa del equipo", styles["Heading2"]))
            contenido.append(Table([headers] + stats))

            contenido.append(Spacer(1,20))

            contenido.append(Paragraph("Observaciones", styles["Heading2"]))
            contenido.append(Paragraph(st.session_state.notas or "Sin observaciones", styles["Normal"]))

            contenido.append(Spacer(1,20))
            contenido.append(Paragraph(f"Marcador final: {marcador}", styles["Normal"]))

            contenido.append(Spacer(1,30))
            contenido.append(Paragraph("Reporte generado por Metrica90", styles["Normal"]))

            doc.build(contenido)

        if st.button("📄 Generar PDF PRO"):
            generar_pdf()
            with open("reporte.pdf","rb") as f:
                st.download_button("⬇️ Descargar PDF",f,"reporte.pdf")

    else:
        st.info("No hay datos aún")

# -----------------------------
# RESET
# -----------------------------
if st.button("🗑️ Reiniciar todo"):
    st.session_state.registro = []
    st.session_state.plantilla = []
    st.session_state.jugador_activo = None
    st.session_state.inicio_partido = None
    st.session_state.tiempo_acumulado = 0