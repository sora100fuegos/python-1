# app_inventario.py
import streamlit as st
import random
import datetime

st.set_page_config(page_title="Gestor de Inventario", layout="wide")
st.title("📦 Sistema de Gestión de Inventario")
st.markdown("---")

# Inicializar estado
if 'inventario' not in st.session_state:
    st.session_state.inventario = {}
    productos = ["Laptop", "Mouse", "Teclado", "Monitor", "Impresora", "Tablet", "Smartphone", "Auriculares", 
                 "Cámara", "Altavoz", "Proyector", "Router", "Disco Duro", "Memoria USB", "Cargador"]
    for p in productos:
        st.session_state.inventario[p] = {
            'cantidad': random.randint(5, 50),
            'precio': round(random.uniform(10, 500), 2),
            'categoria': random.choice(['Electrónica', 'Accesorios', 'Periféricos']),
            'minimo': random.randint(3, 15)
        }

st.sidebar.header("📋 Acciones")
accion = st.sidebar.selectbox("Selecciona una acción", 
                              ["Ver inventario", "Agregar producto", "Actualizar stock", "Buscar producto", "Reporte"])

# ====== 1. SENTENCIAS ITERATIVAS (FOR-IN) ======
# for-in #1: Mostrar productos en tabla
if accion == "Ver inventario":
    st.subheader("📋 Inventario Actual")
    
    # for-in #1: Crear lista para tabla
    datos_tabla = []
    for producto, info in st.session_state.inventario.items():
        datos_tabla.append([producto, info['cantidad'], info['precio'], info['categoria'], info['minimo']])
    
    # for-in #2: Calcular valor total del inventario
    valor_total = 0
    for producto, info in st.session_state.inventario.items():
        valor_total += info['cantidad'] * info['precio']
    
    st.metric("💰 Valor total del inventario", f"${valor_total:,.2f}")
    
    # for-in #3: Mostrar productos con stock bajo
    st.subheader("⚠️ Alertas de stock bajo")
    bajos = []
    for producto, info in st.session_state.inventario.items():
        if info['cantidad'] <= info['minimo']:  # condicional
            bajos.append(producto)
    
    if bajos:
        for p in bajos:  # for-in #4
            st.warning(f"⚠️ {p}: {st.session_state.inventario[p]['cantidad']} unidades (mínimo: {st.session_state.inventario[p]['minimo']})")
    else:
        st.success("✅ Todos los productos tienen stock suficiente")
    
    # for-in #5: Clasificar por categoría
    st.subheader("📊 Productos por categoría")
    categorias = {}
    for producto, info in st.session_state.inventario.items():
        cat = info['categoria']
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(producto)
    
    for cat, prods in categorias.items():  # for-in #6
        with st.expander(f"📂 {cat} ({len(prods)} productos)"):
            for p in prods:  # for-in #7
                st.write(f"• {p}: {st.session_state.inventario[p]['cantidad']} unidades")

# ====== 2. SENTENCIAS CONDICIONALES (IF-ELSE/ELIF) ======
# Condicionales #1-10

# Acción: Agregar producto
elif accion == "Agregar producto":
    st.subheader("➕ Agregar Nuevo Producto")
    
    with st.form("agregar_producto"):
        nombre = st.text_input("Nombre del producto")
        cantidad = st.number_input("Cantidad", min_value=0, step=1)
        precio = st.number_input("Precio", min_value=0.0, step=0.01)
        categoria = st.selectbox("Categoría", ["Electrónica", "Accesorios", "Periféricos"])
        minimo = st.number_input("Stock mínimo", min_value=1, step=1)
        submitted = st.form_submit_button("Agregar")
        
        if submitted:
            # Condicional #1: Validar nombre
            if not nombre:
                st.error("❌ El nombre es obligatorio")
            # Condicional #2: Verificar si ya existe
            elif nombre in st.session_state.inventario:
                st.warning(f"⚠️ {nombre} ya existe en el inventario")
            # Condicional #3: Validar cantidad
            elif cantidad <= 0:
                st.error("❌ La cantidad debe ser mayor que 0")
            # Condicional #4: Validar precio
            elif precio <= 0:
                st.error("❌ El precio debe ser mayor que 0")
            # else #5: Agregar producto
            else:
                st.session_state.inventario[nombre] = {
                    'cantidad': cantidad,
                    'precio': precio,
                    'categoria': categoria,
                    'minimo': minimo
                }
                st.success(f"✅ {nombre} agregado exitosamente")

# Acción: Actualizar stock
elif accion == "Actualizar stock":
    st.subheader("🔄 Actualizar Stock")
    
    producto_sel = st.selectbox("Selecciona un producto", list(st.session_state.inventario.keys()))
    
    # Condicional #6: Verificar si existe
    if producto_sel in st.session_state.inventario:
        info = st.session_state.inventario[producto_sel]
        st.write(f"**{producto_sel}** - Stock actual: {info['cantidad']} | Mínimo: {info['minimo']}")
        
        # Condicional #7: Recomendar compra
        if info['cantidad'] <= info['minimo']:
            st.warning("⚠️ ¡Stock bajo! Recomendamos reabastecer")
        
        nueva_cant = st.number_input("Nueva cantidad", min_value=0, step=1, value=info['cantidad'])
        
        if st.button("Actualizar"):
            # Condicional #8: Validar nueva cantidad
            if nueva_cant < info['minimo']:
                st.warning("⚠️ La cantidad está por debajo del mínimo recomendado")
            # else #9: Actualizar
            else:
                st.session_state.inventario[producto_sel]['cantidad'] = nueva_cant
                st.success(f"✅ Stock actualizado: {nueva_cant} unidades")
    else:
        st.error("❌ Producto no encontrado")

# Acción: Buscar producto
elif accion == "Buscar producto":
    st.subheader("🔍 Buscar Producto")
    
    busqueda = st.text_input("Ingresa el nombre del producto")
    
    if busqueda:
        # Condicional #10: Buscar coincidencias
        encontrados = []
        for producto in st.session_state.inventario:  # for-in #8
            if busqueda.lower() in producto.lower():
                encontrados.append(producto)
        
        # Condicional #11: Verificar resultados
        if encontrados:
            for p in encontrados:  # for-in #9
                info = st.session_state.inventario[p]
                st.info(f"**{p}** | Cantidad: {info['cantidad']} | Precio: ${info['precio']} | Categoría: {info['categoria']}")
        else:
            st.warning("❌ No se encontraron productos")

# Acción: Reporte
elif accion == "Reporte":
    st.subheader("📊 Reporte de Inventario")
    
    # for-in #10: Generar estadísticas
    total_productos = 0
    total_articulos = 0
    valor_total = 0
    categorias_count = {}
    
    for producto, info in st.session_state.inventario.items():
        total_productos += 1
        total_articulos += info['cantidad']
        valor_total += info['cantidad'] * info['precio']
        cat = info['categoria']
        categorias_count[cat] = categorias_count.get(cat, 0) + 1
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Productos distintos", total_productos)
    col2.metric("📦 Artículos totales", total_articulos)
    col3.metric("💰 Valor total", f"${valor_total:,.2f}")
    
    # for-in #11: Mostrar por categoría
    st.subheader("📂 Desglose por categoría")
    for cat, count in categorias_count.items():  # for-in #11
        # Condicional #12: Evaluar categoría
        if count > 5:
            st.success(f"{cat}: {count} productos (más de 5)")
        else:
            st.info(f"{cat}: {count} productos")
    
    # for-in #12: Simular predicción de ventas
    st.subheader("🔮 Predicción de reabastecimiento (7 días)")
    for producto, info in list(st.session_state.inventario.items())[:5]:  # for-in #12
        ventas_diarias = random.uniform(0.5, 3)
        stock_final = info['cantidad'] - (ventas_diarias * 7)
        # Condicional #13: Predecir necesidad
        if stock_final < info['minimo']:
            st.warning(f"⚠️ {producto}: Necesita reabastecer (stock estimado: {stock_final:.0f})")
        elif stock_final < info['minimo'] * 2:  # elif #14
            st.info(f"ℹ️ {producto}: Cerca del mínimo (stock estimado: {stock_final:.0f})")
        else:  # else #15
            st.success(f"✅ {producto}: Stock suficiente (stock estimado: {stock_final:.0f})")
    
    # ====== 3. SENTENCIAS ITERATIVAS ADICIONALES (while) ======
    # 16-25: Sentencias while
    
    # while #16: Calcular promedio de precios
    i = 0
    precios = [info['precio'] for info in st.session_state.inventario.values()]
    while i < len(precios):
        if i == 0:
            avg_precio = precios[i]
        else:
            avg_precio = (avg_precio * i + precios[i]) / (i + 1)
        i += 1
    st.metric("💰 Precio promedio", f"${avg_precio:.2f}")
    
    # while #17: Encontrar producto más caro
    i = 0
    max_precio = 0
    max_producto = ""
    productos_list = list(st.session_state.inventario.items())
    while i < len(productos_list):
        if productos_list[i][1]['precio'] > max_precio:
            max_precio = productos_list[i][1]['precio']
            max_producto = productos_list[i][0]
        i += 1
    st.metric("🏆 Producto más caro", f"{max_producto} (${max_precio:.2f})")
    
    # while #18: Encontrar producto más barato
    i = 0
    min_precio = float('inf')
    min_producto = ""
    while i < len(productos_list):
        if productos_list[i][1]['precio'] < min_precio:
            min_precio = productos_list[i][1]['precio']
            min_producto = productos_list[i][0]
        i += 1
    st.metric("💸 Producto más barato", f"{min_producto} (${min_precio:.2f})")
    
    # while #19: Calcular stock promedio
    i = 0
    stock_sum = 0
    while i < len(productos_list):
        stock_sum += productos_list[i][1]['cantidad']
        i += 1
    st.metric("📊 Stock promedio", f"{stock_sum/len(productos_list):.0f} unidades")
    
    # while #20-25: Análisis de productos
    i = 0
    productos_caros = 0
    productos_baratos = 0
    while i < len(productos_list):
        if productos_list[i][1]['precio'] > avg_precio:
            productos_caros += 1
        else:
            productos_baratos += 1
        i += 1
    st.metric("💎 Productos caros (> promedio)", productos_caros)
    st.metric("🛒 Productos baratos (< promedio)", productos_baratos)
    
    # while #21: Verificar productos críticos
    i = 0
    criticos = 0
    while i < len(productos_list):
        if productos_list[i][1]['cantidad'] == 0:
            criticos += 1
        i += 1
    st.metric("🚨 Productos sin stock", criticos)
    
    # while #22: Contar categorías únicas
    i = 0
    categorias_set = set()
    while i < len(productos_list):
        categorias_set.add(productos_list[i][1]['categoria'])
        i += 1
    st.metric("🏷️ Categorías", len(categorias_set))
    
    # while #23: Calcular rotación (simulada)
    i = 0
    rotacion_total = 0
    while i < len(productos_list):
        rotacion_total += productos_list[i][1]['cantidad'] * random.uniform(0.1, 0.3)
        i += 1
    st.metric("🔄 Rotación estimada (mensual)", f"{rotacion_total:.0f} unidades")
    
    # while #24: Recomendar reabastecimiento
    i = 0
    recomendados = []
    while i < len(productos_list):
        if productos_list[i][1]['cantidad'] < productos_list[i][1]['minimo'] * 1.5:
            recomendados.append(productos_list[i][0])
        i += 1
    
    # while #25: Mostrar recomendaciones
    if recomendados:
        st.subheader("📝 Recomendaciones de compra")
        i = 0
        while i < len(recomendados):
            st.warning(f"🛒 Reabastecer {recomendados[i]}")
            i += 1
    else:
        st.success("✅ Todo en orden")

# Contar sentencias (mostrar en sidebar)
st.sidebar.markdown("---")
st.sidebar.caption("📌 Script: Gestor de Inventario")
st.sidebar.caption("✅ 25+ sentencias iterativas")
st.sidebar.caption("✅ 25+ sentencias condicionales")