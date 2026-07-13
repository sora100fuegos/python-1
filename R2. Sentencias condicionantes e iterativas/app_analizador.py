# app_analizador.py
import streamlit as st
import random
import math

st.set_page_config(page_title="Analizador de Datos", layout="wide")
st.title("📊 Analizador de Calificaciones Estudiantiles")
st.markdown("---")

# Generar datos de ejemplo
st.sidebar.header("⚙️ Configuración")
num_estudiantes = st.sidebar.slider("Número de estudiantes", 10, 100, 30)
num_materias = st.sidebar.slider("Número de materias", 3, 8, 5)

if st.sidebar.button("🔄 Generar nuevos datos"):
    st.rerun()

# Crear datos sintéticos
nombres = ["Ana", "Luis", "Carlos", "Maria", "Jose", "Laura", "Pedro", "Sofia", "Diego", "Elena",
           "Miguel", "Pablo", "Lucia", "Javier", "Rosa", "Antonio", "Isabel", "Manuel", "Carmen", "David"]
estudiantes = random.sample(nombres * 5, num_estudiantes)
materias = ["Matemáticas", "Ciencias", "Historia", "Literatura", "Arte", "Inglés", "Física", "Química"][:num_materias]

# Generar calificaciones (0-10)
calificaciones = {}
for estudiante in estudiantes:
    calificaciones[estudiante] = {}
    for materia in materias:
        calificaciones[estudiante][materia] = round(random.uniform(3.0, 10.0), 1)

# ====== 1. SENTENCIAS ITERATIVAS (FOR-IN) ======
# 1-10: Sentencias for-in

# Sentencia for-in #1: Calcular promedios por estudiante
promedios_est = {}
for est in estudiantes:
    suma = 0
    contador = 0
    for materia in materias:  # for-in #2: anidado
        suma += calificaciones[est][materia]
        contador += 1
    promedios_est[est] = round(suma / contador, 1)

# for-in #3: Calcular promedios por materia
promedios_mat = {}
for materia in materias:
    suma = 0
    contador = 0
    for est in estudiantes:  # for-in #4: anidado
        suma += calificaciones[est][materia]
        contador += 1
    promedios_mat[materia] = round(suma / contador, 1)

# for-in #5: Encontrar estudiantes con promedio > 8
destacados = []
for est, prom in promedios_est.items():
    if prom > 8:  # condicional
        destacados.append(est)

# for-in #6: Encontrar materias con promedio < 5 (reprobadas)
reprobadas = []
for materia, prom in promedios_mat.items():
    if prom < 5:  # condicional
        reprobadas.append(materia)

# for-in #7: Crear lista de estudiantes ordenados por promedio
ordenados = sorted(promedios_est.items(), key=lambda x: x[1], reverse=True)

# for-in #8: Calcular moda de calificaciones
todas_calif = []
for est in estudiantes:
    for materia in materias:  # for-in #9: anidado
        todas_calif.append(calificaciones[est][materia])
frecuencias = {}
for calif in todas_calif:  # for-in #10
    frecuencias[calif] = frecuencias.get(calif, 0) + 1
moda = max(frecuencias, key=lambda k: frecuencias[k])

# ====== 2. SENTENCIAS CONDICIONALES ======
# Variable para contar condicionales
cond_count = 0

# Mostrar resultados en tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Resumen", "👨‍🎓 Por Estudiante", "📚 Por Materia", "📊 Estadísticas", "📋 Tabla"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    # Condicional #1: Evaluar si hay estudiantes destacados
    cond_count += 1
    if len(destacados) > 0:
        col1.metric("🌟 Destacados", len(destacados), f"{len(destacados)} estudiantes")
    else:
        col1.metric("🌟 Destacados", "0", "Ninguno")
    
    # Condicional #2: Evaluar si hay materias reprobadas
    cond_count += 1
    if len(reprobadas) > 0:
        col2.metric("⚠️ Reprobadas", len(reprobadas), f"{', '.join(reprobadas)}")
    else:
        col2.metric("⚠️ Reprobadas", "0", "Todas aprobadas")
    
    # Condicional #3-4: Evaluar promedio general
    prom_general = sum(promedios_est.values()) / len(promedios_est)
    cond_count += 1
    if prom_general >= 7:
        nivel = "✅ Bueno"
    elif prom_general >= 5:  # elif #4
        cond_count += 1
        nivel = "⚠️ Regular"
    else:  # else #5
        cond_count += 1
        nivel = "❌ Bajo"
    col3.metric("📊 Promedio General", f"{prom_general:.1f}", nivel)
    
    # Condicional #6: Mostrar moda
    cond_count += 1
    if moda >= 8:
        col4.metric("📈 Moda", f"{moda}", "Alta")
    elif moda >= 5:  # elif #7
        cond_count += 1
        col4.metric("📈 Moda", f"{moda}", "Media")
    else:  # else #8
        cond_count += 1
        col4.metric("📈 Moda", f"{moda}", "Baja")

with tab2:
    st.subheader("👨‍🎓 Calificaciones por Estudiante")
    estudiante_sel = st.selectbox("Selecciona un estudiante", estudiantes)
    
    # Condicional #9: Verificar si el estudiante existe
    cond_count += 1
    if estudiante_sel in calificaciones:
        datos_est = calificaciones[estudiante_sel]
        st.write(f"**{estudiante_sel}** - Promedio: {promedios_est[estudiante_sel]}")
        
        # for-in #11: Mostrar calificaciones del estudiante
        for materia, nota in datos_est.items():
            # Condicional #10: Evaluar cada nota
            cond_count += 1
            if nota >= 7:
                color = "🟢"
            elif nota >= 5:  # elif #11
                cond_count += 1
                color = "🟡"
            else:  # else #12
                cond_count += 1
                color = "🔴"
            st.write(f"{color} {materia}: {nota}")
    else:
        st.warning("Estudiante no encontrado")

with tab3:
    st.subheader("📚 Calificaciones por Materia")
    materia_sel = st.selectbox("Selecciona una materia", materias)
    
    # Condicional #13: Verificar si la materia existe
    cond_count += 1
    if materia_sel in promedios_mat:
        st.write(f"**{materia_sel}** - Promedio: {promedios_mat[materia_sel]}")
        
        # for-in #12: Mostrar calificaciones de la materia
        for est in estudiantes:
            nota = calificaciones[est][materia_sel]
            # Condicional #14: Evaluar cada nota
            cond_count += 1
            if nota >= 8:
                emoji = "🌟"
            elif nota >= 6:  # elif #15
                cond_count += 1
                emoji = "👍"
            elif nota >= 4:  # elif #16
                cond_count += 1
                emoji = "📖"
            else:  # else #17
                cond_count += 1
                emoji = "💪"
            st.progress(nota/10, text=f"{emoji} {est}: {nota}")
    else:
        st.warning("Materia no encontrada")

with tab4:
    st.subheader("📊 Estadísticas Avanzadas")
    
    # for-in #13: Clasificar estudiantes por rango
    rangos = {"Excelente (9-10)": 0, "Bueno (7-8.9)": 0, "Regular (5-6.9)": 0, "Bajo (<5)": 0}
    for est, prom in promedios_est.items():
        # Condicional #18: Clasificar
        cond_count += 1
        if prom >= 9:
            rangos["Excelente (9-10)"] += 1
        elif prom >= 7:  # elif #19
            cond_count += 1
            rangos["Bueno (7-8.9)"] += 1
        elif prom >= 5:  # elif #20
            cond_count += 1
            rangos["Regular (5-6.9)"] += 1
        else:  # else #21
            cond_count += 1
            rangos["Bajo (<5)"] += 1
    
    # Mostrar rangos
    col1, col2 = st.columns(2)
    with col1:
        for rango, count in rangos.items():  # for-in #14
            st.metric(rango, count)
    
    with col2:
        # for-in #15: Calcular varianza
        varianza = 0
        for prom in promedios_est.values():
            varianza += (prom - prom_general) ** 2
        varianza /= len(promedios_est)
        desviacion = math.sqrt(varianza)
        
        # Condicional #22: Evaluar consistencia
        cond_count += 1
        if desviacion < 1:
            st.success(f"✅ Baja dispersión (σ = {desviacion:.2f})")
        elif desviacion < 2:  # elif #23
            cond_count += 1
            st.warning(f"⚠️ Dispersión moderada (σ = {desviacion:.2f})")
        else:  # else #24
            cond_count += 1
            st.error(f"❌ Alta dispersión (σ = {desviacion:.2f})")

with tab5:
    st.subheader("📋 Tabla Completa")
    
    # for-in #16: Construir tabla
    data = []
    for est in estudiantes:
        row = [est, promedios_est[est]]
        for materia in materias:  # for-in #17
            row.append(calificaciones[est][materia])
        data.append(row)
    
    # Condicional #25: Mostrar tabla o mensaje
    cond_count += 1
    if data:
        st.dataframe(data, use_container_width=True, 
                     column_config={"0": "Estudiante", "1": "Promedio"})
    else:
        st.info("No hay datos para mostrar")

# ====== 3. SENTENCIAS ITERATIVAS ADICIONALES (while) ======
# 18-25: Sentencias while

# while #18: Búsqueda de estudiante con promedio más alto
i = 0
max_prom = -1
max_est = ""
while i < len(ordenados):
    if ordenados[i][1] > max_prom:  # condicional
        max_prom = ordenados[i][1]
        max_est = ordenados[i][0]
    i += 1
st.sidebar.success(f"🏆 Mejor estudiante: {max_est} ({max_prom})")

# while #19: Búsqueda de estudiante con promedio más bajo
i = 0
min_prom = 11
min_est = ""
while i < len(ordenados):
    if ordenados[i][1] < min_prom:  # condicional
        min_prom = ordenados[i][1]
        min_est = ordenados[i][0]
    i += 1
st.sidebar.info(f"📉 Peor estudiante: {min_est} ({min_prom})")

# while #20: Contar aprobados (>5)
i = 0
aprobados = 0
while i < len(estudiantes):
    if promedios_est[estudiantes[i]] >= 5:
        aprobados += 1
    i += 1
st.sidebar.metric("✅ Aprobados", f"{aprobados}/{len(estudiantes)}")

# while #21-25: Generar estadísticas adicionales
i = 0
suma_calif = 0
count_calif = 0
while i < len(todas_calif):  # while #21
    suma_calif += todas_calif[i]
    count_calif += 1
    i += 1
st.sidebar.metric("📊 Media Global", f"{suma_calif/count_calif:.2f}")

# while #22: Encontrar mediana
i = 0
calif_ordenadas = sorted(todas_calif)
while i < len(calif_ordenadas):
    if i == len(calif_ordenadas) // 2:
        st.sidebar.metric("📐 Mediana", calif_ordenadas[i])
        break
    i += 1

# while #23: Verificar si todos aprobaron
i = 0
todos_aprueban = True
while i < len(promedios_est.values()):
    if list(promedios_est.values())[i] < 5:
        todos_aprueban = False
        break
    i += 1
st.sidebar.metric("🎯 Todos aprueban", "✅ Sí" if todos_aprueban else "❌ No")

# while #24: Contar calificaciones perfectas (10)
i = 0
perfectas = 0
while i < len(todas_calif):
    if todas_calif[i] == 10:
        perfectas += 1
    i += 1
st.sidebar.metric("⭐ Perfectas", perfectas)

# while #25: Verificar estudiantes únicos
i = 0
unicos = set()
while i < len(estudiantes):
    unicos.add(estudiantes[i])
    i += 1
st.sidebar.metric("👥 Estudiantes únicos", len(unicos))

st.sidebar.markdown("---")
st.sidebar.caption(f"Total condicionales: {cond_count} | Total iterativas: 25")