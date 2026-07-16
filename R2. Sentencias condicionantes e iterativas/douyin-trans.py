import streamlit as st
import yt_dlp
import os
import re
import tempfile
from moviepy import VideoFileClip
import whisper
from deep_translator import GoogleTranslator
import time

# ============================================================
# CONFIGURACIÓN INICIAL DE STREAMLIT
# ============================================================
st.set_page_config(page_title="🎬 Douyin Translator", layout="wide")
st.title("🎬 Traductor de Videos de Douyin")
st.markdown("Sube la URL de un video de Douyin , extrae el audio, transcríbelo y tradúcelo al inglés.")

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def validar_url_douyin(url):
    """Valida que la URL sea de Douyin/TikTok"""
    # [Condicional 1: if]
    if url is None or url.strip() == "":
        return False, "La URL está vacía."
    
    # [Condicional 2: elif]
    elif "douyin.com" in url or "tiktok.com" in url or "iesdouyin.com" in url:
        return True, "URL válida de Douyin/TikTok."
    
    # [Condicional 3: elif]
    elif url.startswith("http://") or url.startswith("https://"):
        return True, "URL genérica aceptada (se intentará descargar)."
    
    # [Condicional 4: else]
    else:
        return False, "URL no válida. Debe ser de Douyin o TikTok."


def descargar_video_douyin(url, output_path):
    """Descarga el video usando yt-dlp"""
    # [Condicional 5: if] Validación previa
    if not url:
        return None, "URL no proporcionada."
    
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'rm_cachedir': True,
        'extractor_args': {
        'youtube': {
            'player_client': ['android', 'ios']
        }
    },
    
    }
    
    try:
        # [Iterativa 1: for-in] Reintentos de descarga
        for intento in range(3):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    # [Condicional 6: if]
                    if info is None:
                        return None, "No se pudo extraer información del video."
                    
                    # [Condicional 7: if]
                    if 'title' not in info:
                        info['title'] = 'video_sin_titulo'
                    
                    return info, "Descarga exitosa."
            except Exception as e:
                # [Condicional 8: elif]
                if intento < 2:
                    time.sleep(1)
                    continue
                # [Condicional 9: else]
                else:
                    return None, f"Error tras 3 intentos: {str(e)}"
    except Exception as e:
        return None, f"Error crítico: {str(e)}"


def extraer_audio(video_path, audio_path):
    """Extrae el audio del video usando moviepy"""
    # [Condicional 10: if]
    if not os.path.exists(video_path):
        return False, "El archivo de video no existe."
    
    try:
        video = VideoFileClip(video_path)
        # [Condicional 11: if]
        if video.audio is None:
            return False, "El video no contiene pista de audio."
        
        # [Condicional 12: elif]
        elif video.duration > 180:
            st.warning("⚠️ Video muy largo (>3 min). Procesando solo los primeros 3 minutos.")
            video = video.subclipped(0, 180)
        
        video.audio.write_audiofile(audio_path, fps=16000, nbytes=2, codec='pcm_s16le')
        video.close()
        return True, "Audio extraído correctamente."
    except Exception as e:
        return False, f"Error extrayendo audio: {str(e)}"


def dividir_audio_en_segmentos(audio_path, duracion_segmento=30):
    """Divide el audio en segmentos para procesamiento"""
    segmentos = []
    try:
        video = VideoFileClip(audio_path)
        duracion_total = video.duration
        video.close()
        
        # [Iterativa 2: while] Dividir en segmentos
        inicio = 0
        while inicio < duracion_total:
            fin = min(inicio + duracion_segmento, duracion_total)
            segmentos.append((inicio, fin))
            inicio = fin
        
        return segmentos, duracion_total
    except Exception as e:
        return [], 0


def transcribir_audio(audio_path, modelo_whisper="base"):
    """Transcribe el audio usando Whisper"""
    # [Condicional 13: if]
    if not os.path.exists(audio_path):
        return None, "Archivo de audio no encontrado."
    
    try:
        # [Condicional 14: if-elif-else] Selección de modelo
        if modelo_whisper == "tiny":
            model = whisper.load_model("tiny")
        elif modelo_whisper == "base":
            model = whisper.load_model("base")
        elif modelo_whisper == "small":
            model = whisper.load_model("small")
        else:
            model = whisper.load_model("base")
        
        resultado = model.transcribe(audio_path, language=None)
        
        # [Condicional 15: if]
        if resultado is None or 'text' not in resultado:
            return None, "Whisper no produjo resultados."
        
        return resultado, "Transcripción exitosa."
    except Exception as e:
        return None, f"Error en transcripción: {str(e)}"


def detectar_idioma(texto):
    """Detecta el idioma del texto transcrito"""
    # [Iterativa 3: for-in] Analizar caracteres
    contador_chino = 0
    contador_latin = 0
    total_caracteres = len(texto)
    
    # [Condicional 16: if]
    if total_caracteres == 0:
        return "desconocido"
    
    # [Iterativa 4: for-in] Recorrer caracteres
    for caracter in texto[:500]:
        # [Condicional 17: if]
        if '\u4e00' <= caracter <= '\u9fff':
            contador_chino += 1
        # [Condicional 18: elif]
        elif caracter.isalpha():
            contador_latin += 1
    
    # [Condicional 19: if-elif-else] Determinar idioma
    if contador_chino > contador_latin:
        return "zh"
    elif contador_latin > contador_chino:
        return "auto"
    else:
        return "desconocido"


def traducir_a_ingles(texto, idioma_origen="auto"):
    """Traduce el texto al inglés usando GoogleTranslator"""
    # [Condicional 20: if]
    if not texto or texto.strip() == "":
        return "", "Texto vacío."
    
    try:
        # [Condicional 21: if-elif-else] Configurar traductor
        if idioma_origen == "zh":
            translator = GoogleTranslator(source='zh-CN', target='en')
        elif idioma_origen == "auto":
            translator = GoogleTranslator(source='auto', target='en')
        else:
            translator = GoogleTranslator(source=idioma_origen, target='en')
        
        # [Iterativa 5: for-in] Traducir por fragmentos (límites de API)
        fragmentos = []
        max_longitud = 4500
        texto_limpio = texto.replace('\n', ' ')
        
        # [Iterativa 6: while] Dividir texto largo
        posicion = 0
        while posicion < len(texto_limpio):
            final = min(posicion + max_longitud, len(texto_limpio))
            # [Condicional 22: if] Evitar cortar palabras
            if final < len(texto_limpio):
                while final > posicion and texto_limpio[final] != ' ':
                    final -= 1
            fragmento = texto_limpio[posicion:final].strip()
            if fragmento:
                fragmentos.append(fragmento)
            posicion = final if final > posicion else posicion + 1
        
        traducciones = []
        # [Iterativa 7: for-in] Traducir cada fragmento
        for i, frag in enumerate(fragmentos):
            try:
                traduccion = translator.translate(frag)
                traducciones.append(traduccion)
            except Exception as e:
                traducciones.append(f"[Error en fragmento {i+1}]")
        
        texto_final = " ".join(traducciones)
        return texto_final, "Traducción completada."
    except Exception as e:
        return "", f"Error en traducción: {str(e)}"


def procesar_segmentos_audio(segmentos, audio_path, modelo_whisper):
    """Procesa cada segmento de audio individualmente"""
    transcripciones = []
    
    # [Iterativa 8: for-in] Procesar cada segmento
    for idx, (inicio, fin) in enumerate(segmentos):
        try:
            video = VideoFileClip(audio_path)
            clip = video.subclip(inicio, fin)
            
            temp_path = f"temp_segment_{idx}.wav"
            clip.write_audiofile(temp_path, fps=16000, nbytes=2, codec='pcm_s16le', verbose=False, logger=None)
            clip.close()
            video.close()
            
            resultado, msg = transcribir_audio(temp_path, modelo_whisper)
            
            # [Condicional 23: if]
            if resultado is not None:
                transcripciones.append({
                    "inicio": inicio,
                    "fin": fin,
                    "texto": resultado['text'],
                    "idioma": detectar_idioma(resultado['text'])
                })
            
            # Limpiar archivo temporal
            # [Condicional 24: if]
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
        except Exception as e:
            continue
    
    return transcripciones


def generar_subtitulos_srt(transcripciones_traducidas):
    """Genera archivo SRT con las traducciones"""
    lineas_srt = []
    
    # [Iterativa 9: for-in] Generar cada entrada de subtítulo
    for idx, entrada in enumerate(transcripciones_traducidas):
        # [Iterativa 10: while] Formatear tiempo
        inicio_seg = entrada['inicio']
        fin_seg = entrada['fin']
        
        def formato_tiempo(segundos):
            h = int(segundos // 3600)
            m = int((segundos % 3600) // 60)
            s = int(segundos % 60)
            ms = int((segundos - int(segundos)) * 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
        
        linea = f"{idx + 1}\n"
        linea += f"{formato_tiempo(inicio_seg)} --> {formato_tiempo(fin_seg)}\n"
        linea += f"{entrada['traduccion']}\n\n"
        lineas_srt.append(linea)
    
    return "".join(lineas_srt)


# ============================================================
# INTERFAZ PRINCIPAL DE STREAMLIT
# ============================================================

# Sidebar con configuración
st.sidebar.header("⚙️ Configuración")
url_video = st.sidebar.text_input("🔗 URL del video de Douyin/TikTok", 
                                   placeholder="https://www.douyin.com/video/...")
modelo_whisper = st.sidebar.selectbox("🎙️ Modelo de transcripción", 
                                       ["tiny", "base", "small"], 
                                       index=1)
traducir = st.sidebar.checkbox("🌐 Traducir al inglés", value=True)

# Botón principal
procesar = st.sidebar.button("🚀 Procesar Video", type="primary")

# ============================================================
# FLUJO PRINCIPAL DE PROCESAMIENTO
# ============================================================

if procesar:
    # [Condicional 25: if] Validar URL
    es_valida, msg_url = validar_url_douyin(url_video)
    
    if not es_valida:
        st.error(f"❌ {msg_url}")
        st.stop()
    
    st.success(f"✅ {msg_url}")
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, "video.mp4")
        audio_path = os.path.join(tmpdir, "audio.wav")
        
        # PASO 1: Descargar video
        st.subheader("📥 Paso 1: Descargando video...")
        progreso_descarga = st.progress(0)
        
        # [Iterativa 11: for-in] Simulación de progreso
        for i in range(10):
            tiempo_espera = 0.1
            time.sleep(tiempo_espera)
            progreso_descarga.progress((i + 1) * 10)
        
        info_video, msg_descarga = descargar_video_douyin(url_video, video_path)
        
        # [Condicional 26: if-else]
        if info_video is None:
            st.error(f"❌ {msg_descarga}")
            st.stop()
        else:
            st.success(f"✅ {msg_descarga}")
            # [Condicional 27: if]
            if 'title' in info_video:
                st.info(f"📌 Título: {info_video['title']}")
        
        # PASO 2: Extraer audio
        st.subheader("🎵 Paso 2: Extrayendo audio...")
        progreso_audio = st.progress(0)
        
        # [Iterativa 12: for-in] Progreso de extracción
        for i in range(5):
            time.sleep(0.2)
            progreso_audio.progress((i + 1) * 20)
        
        audio_ok, msg_audio = extraer_audio(video_path, audio_path)
        
        # [Condicional 28: if-else]
        if not audio_ok:
            st.error(f"❌ {msg_audio}")
            st.stop()
        else:
            st.success(f"✅ {msg_audio}")
        
        # PASO 3: Transcribir
        st.subheader("📝 Paso 3: Transcribiendo audio...")
        
        segmentos, duracion_total = dividir_audio_en_segmentos(audio_path)
        
        # [Condicional 29: if-else] Decidir estrategia
        if duracion_total <= 60:
            # Video corto: transcribir completo
            resultado_trans, msg_trans = transcribir_audio(audio_path, modelo_whisper)
            
            # [Condicional 30: if-else]
            if resultado_trans is None:
                st.error(f"❌ {msg_trans}")
                st.stop()
            else:
                st.success(f"✅ {msg_trans}")
                transcripciones = [{
                    "inicio": 0,
                    "fin": duracion_total,
                    "texto": resultado_trans['text'],
                    "idioma": detectar_idioma(resultado_trans['text'])
                }]
        else:
            # Video largo: procesar por segmentos
            st.info(f"⏱️ Duración: {duracion_total:.1f}s - Procesando en {len(segmentos)} segmentos")
            progreso_trans = st.progress(0)
            
            # [Iterativa 13: for-in] Barra de progreso por segmentos
            transcripciones = []
            for idx_seg, (inicio, fin) in enumerate(segmentos):
                progreso_trans.progress(int((idx_seg + 1) / len(segmentos) * 100))
                
                try:
                    video_full = VideoFileClip(audio_path)
                    clip = video_full.subclip(inicio, fin)
                    temp_seg = os.path.join(tmpdir, f"seg_{idx_seg}.wav")
                    clip.write_audiofile(temp_seg, fps=16000, nbytes=2, codec='pcm_s16le', verbose=False, logger=None)
                    clip.close()
                    video_full.close()
                    
                    res_seg, _ = transcribir_audio(temp_seg, modelo_whisper)
                    # [Condicional 31: if]
                    if res_seg is not None:
                        transcripciones.append({
                            "inicio": inicio,
                            "fin": fin,
                            "texto": res_seg['text'],
                            "idioma": detectar_idioma(res_seg['text'])
                        })
                except Exception:
                    continue
        
        # Mostrar transcripción original
        st.subheader("📜 Transcripción Original")
        texto_completo = " ".join([t['texto'] for t in transcripciones])
        st.text_area("Texto transcrito:", texto_completo, height=150)
        
        # PASO 4: Traducir
        if traducir:
            st.subheader("🌐 Paso 4: Traduciendo al inglés...")
            progreso_trad = st.progress(0)
            
            # [Iterativa 14: for-in] Traducir cada segmento
            traducciones = []
            for idx_t, trans in enumerate(transcripciones):
                progreso_trad.progress(int((idx_t + 1) / len(transcripciones) * 100))
                
                texto_trad, msg_trad = traducir_a_ingles(trans['texto'], trans['idioma'])
                traducciones.append({
                    "inicio": trans['inicio'],
                    "fin": trans['fin'],
                    "texto_original": trans['texto'],
                    "traduccion": texto_trad
                })
            
            st.success("✅ Traducción completada")
            
            # Mostrar traducción
            st.subheader("🇬🇧 Traducción al Inglés")
            texto_traducido = " ".join([t['traduccion'] for t in traducciones])
            st.text_area("English translation:", texto_traducido, height=150)
            
            # Generar subtítulos SRT
            contenido_srt = generar_subtitulos_srt(traducciones)
            
            # [Iterativa 15: for-in] Estadísticas por segmento
            st.subheader("📊 Estadísticas por Segmento")
            for idx_stat, seg in enumerate(traducciones):
                # [Condicional 32: if-elif-else] Clasificar longitud
                longitud = len(seg['traduccion'].split())
                if longitud > 30:
                    icono = "🔴"
                elif longitud > 15:
                    icono = "🟡"
                else:
                    icono = "🟢"
                
                st.write(f"{icono} **Segmento {idx_stat + 1}** ({seg['inicio']:.1f}s - {seg['fin']:.1f}s): {longitud} palabras")
            
            # Botón de descarga
            st.download_button(
                "💾 Descargar subtítulos (.srt)",
                contenido_srt,
                file_name="subtitulos_traducidos.srt",
                mime="text/plain"
            )
            
            st.download_button(
                "💾 Descargar traducción (.txt)",
                texto_traducido,
                file_name="traduccion_ingles.txt",
                mime="text/plain"
            )

else:
    # Estado inicial
    st.info("👈 Ingresa una URL de Douyin/TikTok en la barra lateral y presiona 'Procesar Video'")
    
    st.markdown("---")
    st.markdown("### 📋 ¿Cómo funciona?")
    
    # [Iterativa 16: for-in] Mostrar pasos
    pasos = [
        ("1️⃣", "Descarga el video desde Douyin usando `yt-dlp`"),
        ("2️⃣", "Extrae el audio con `moviepy`"),
        ("3️⃣", "Transcribe el audio con OpenAI Whisper"),
        ("4️⃣", "Detecta el idioma automáticamente"),
        ("5️⃣", "Traduce al inglés con Google Translator"),
        ("6️⃣", "Genera subtítulos SRT descargables"),
    ]
    
    for icono, descripcion in pasos:
        st.write(f"{icono} {descripcion}")
    
    st.markdown("---")
    st.markdown("### ⚠️ Notas importantes")
    st.warning("""
    - Asegúrate de que el video de Douyin sea **público**.
    - Algunos videos pueden tener restricciones geográficas.
    - El procesamiento puede tardar varios minutos según la duración.
    """)