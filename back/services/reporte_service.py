from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from models.vehiculo import Vehiculo

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.barcharts import VerticalBarChart

from database import Database


class ReportesService:
    @staticmethod
    def reporte_flota():
        """
        Genera un PDF estilizado con el estado de la flota.
        Retorna un BytesIO buffer con el contenido del PDF.
        """
        buffer = BytesIO()
        
        # Creamos el documento con márgenes
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=30, leftMargin=30, 
            topMargin=30, bottomMargin=30
        )
        
        elements = []
        styles = getSampleStyleSheet()

        # 1. Título del Reporte
        title_style = styles['Heading1']
        title_style.alignment = 1  # 0=Left, 1=Center, 2=Right
        elements.append(Paragraph("Reporte de Estado de Flota", title_style))
        elements.append(Spacer(1, 20)) # Espacio vertical

        # 2. Preparar los datos para la tabla
        # Encabezados de la tabla
        data = [['Patente', 'Marca', 'Modelo', 'Precio Diario', 'Estado']]
        
        # Filas de datos
        vehiculos = Vehiculo.get_all()
        for v in vehiculos:
            data.append([
                v.patente,
                v.marca,
                v.modelo,
                f"${v.precio_diario:,.2f}",  # Formato moneda
                v.estado.title()             # Capitalizar (ej: Disponible)
            ])

        # 3. Crear la Tabla
        # colWidths ajusta el ancho de cada columna (opcional)
        t = Table(data, colWidths=[80, 100, 100, 80, 100])

        # 4. Aplicar Estilos a la Tabla
        # (Coordenadas: (columna, fila). -1 significa "hasta el final")
        t.setStyle(TableStyle([
            # Estilo del Encabezado (Fila 0)
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Estilo del Cuerpo (Fila 1 en adelante)
            ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue), # Color de fondo suave
            ('GRID', (0, 0), (-1, -1), 1, colors.black),        # Bordes de celdas
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),              # Alinear texto al centro
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            
            # Alternar colores de filas (opcional, para legibilidad)
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.aliceblue]),
        ]))

        elements.append(t)

        # 5. Generar PDF
        doc.build(elements)
        
        buffer.seek(0)
        return buffer

    @staticmethod
    def reporte_alquileres_por_cliente():
        """
        Genera un PDF con el conteo de alquileres por cada cliente.
        Utiliza GROUP BY en SQL para eficiencia.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        styles = getSampleStyleSheet()

        # 1. Título
        title_style = styles['Heading1']
        title_style.alignment = 1
        elements.append(Paragraph("Reporte de Alquileres por Cliente", title_style))
        elements.append(Spacer(1, 20))

        # 2. Consulta SQL (GROUP BY)
        conn = Database().get_connection()
        cursor = conn.cursor()
        
        # Hacemos LEFT JOIN para incluir clientes que tienen 0 alquileres también
        query = """
            SELECT c.nombre, c.apellido, c.dni, COUNT(a.id_alquiler) as cantidad
            FROM Clientes c
            LEFT JOIN Alquileres a ON c.id_cliente = a.id_cliente
            WHERE a.estado IN ('finalizado', 'confirmado', 'activo')
            GROUP BY c.id_cliente
            ORDER BY cantidad DESC, c.apellido ASC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()

        # 3. Preparar Datos
        data = [['Cliente', 'DNI', 'Cantidad de Alquileres']] # Encabezados
        
        for row in resultados:
            nombre_completo = f"{row['nombre']} {row['apellido']}"
            dni = row['dni']
            cantidad = row['cantidad']
            data.append([nombre_completo, dni, str(cantidad)])

        # 4. Crear Tabla
        # Ajustamos anchos: Cliente más ancho, DNI medio, Cantidad medio
        t = Table(data, colWidths=[200, 100, 150])

        # 5. Estilos (Reutilizamos el estilo "cebra" profesional)
        estilo_tabla = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred), # Usamos rojo oscuro para distinguir este reporte
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige), 
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ])
        t.setStyle(estilo_tabla)

        elements.append(t)
        
        # Pie de página simple o totales
        total_alquileres = sum(row['cantidad'] for row in resultados)
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"<b>Total histórico de alquileres:</b> {total_alquileres}", styles['Normal']))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    @staticmethod
    def reporte_ranking_vehiculos():
        """
        Genera un PDF con el Top 5 de vehículos más alquilados
        e incluye un GRÁFICO DE TORTA.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        styles = getSampleStyleSheet()

        # 1. Título
        title_style = styles['Heading1']
        title_style.alignment = 1
        elements.append(Paragraph("Vehículos Más Alquilados (Top 5)", title_style))
        elements.append(Spacer(1, 10))

        # 2. Datos (SQL)
        conn = Database().get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT v.marca, v.modelo, v.nombre, v.patente, COUNT(a.id_alquiler) as cantidad
            FROM Vehiculos v
            JOIN Alquileres a ON v.id_vehiculo = a.id_vehiculo
                WHERE a.estado IN ('finalizado', 'confirmado', 'activo')
            GROUP BY v.id_vehiculo
            ORDER BY cantidad DESC
            LIMIT 5
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            elements.append(Paragraph("No hay datos suficientes para generar el gráfico.", styles['Normal']))
            doc.build(elements)
            buffer.seek(0)
            return buffer

        # 3. Preparar datos para el Gráfico y la Tabla
        data_labels = []
        data_values = []
        table_data = [['Vehículo', 'Patente', 'Alquileres']]

        for row in resultados:
            print('ROW', row)
            label = f"{row['marca']} {row['nombre']} {row['modelo']}"
            data_labels.append(label)
            data_values.append(row['cantidad'])
            table_data.append([label, row['patente'], row['cantidad']])

        # --- 4. CONSTRUCCIÓN DEL GRÁFICO DE TORTA ---
        
        # Creamos un "Lienzo" (Drawing) de 400x200 puntos
        d = Drawing(400, 200)
        
        # Creamos la Torta
        pc = Pie()
        pc.x = 65              # Posición X del centro
        pc.y = 15              # Posición Y del centro
        pc.width = 170         # Ancho
        pc.height = 170        # Alto
        pc.data = data_values  # Los números [10, 5, 2...]
        pc.labels = None       # No ponemos etiquetas directas para no encimar, usamos leyenda
        
        # Colores personalizados (para que se vea lindo)
        colores = [colors.royalblue, colors.limegreen, colors.orange, colors.crimson, colors.gold]
        # Asignamos colores cíclicamente
        for i, color in enumerate(colores):
            if i < len(pc.data):
                pc.slices[i].fillColor = color
        
        d.add(pc)

        # Creamos la Leyenda (Legend)
        legend = Legend()
        legend.alignment = 'right'
        legend.x = 300         # A la derecha de la torta
        legend.y = 150
        legend.columnMaximum = 10
        
        # Mapeamos colores y textos a la leyenda
        legend.colorNamePairs = []
        for i, label in enumerate(data_labels):
            color = pc.slices[i].fillColor
            # Texto: "Toyota Corolla (10)"
            texto = f"{label} ({data_values[i]})" 
            legend.colorNamePairs.append((color, texto))
            
        d.add(legend)
        
        # Agregamos el gráfico a los elementos del PDF
        elements.append(d)
        elements.append(Spacer(1, 20))

        # --- 5. TABLA DE DATOS (Debajo del gráfico) ---
        t = Table(table_data, colWidths=[200, 100, 100])
        
        estilo_tabla = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
        ])
        t.setStyle(estilo_tabla)
        elements.append(t)

        doc.build(elements)
        buffer.seek(0)
        return buffer



    @staticmethod
    def reporte_alquileres_mensuales():
        """
        Genera un reporte de barras con la cantidad de alquileres por mes.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        styles = getSampleStyleSheet()

        # 1. Título
        title_style = styles['Heading1']
        title_style.alignment = 1
        elements.append(Paragraph("Evolución Mensual de Alquileres", title_style))
        elements.append(Spacer(1, 20))

        # 2. Consulta SQL (Agrupado por Mes)
        conn = Database().get_connection()
        cursor = conn.cursor()
        # strftime('%Y-%m', ...) funciona en SQLite para agrupar por Año-Mes
        query = """
            SELECT strftime('%Y-%m', fecha_hora_inicio) as mes, COUNT(*) as cantidad
            FROM Alquileres
            WHERE estado IN ('finalizado', 'confirmado', 'activo')
            GROUP BY mes
            ORDER BY mes ASC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            elements.append(Paragraph("No hay datos históricos de alquileres.", styles['Normal']))
            doc.build(elements)
            buffer.seek(0)
            return buffer

        # 3. Preparar datos
        meses = []
        cantidades = []
        table_data = [['Mes (Año-Mes)', 'Cantidad']]

        for row in resultados:
            meses.append(row['mes'])
            cantidades.append(row['cantidad'])
            table_data.append([row['mes'], row['cantidad']])

        # 4. Crear Gráfico de Barras
        d = Drawing(400, 200)
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = [cantidades] # ReportLab espera una lista de listas
        bc.strokeColor = colors.black
        
        # Configuración de Ejes
        bc.valueAxis.valueMin = 0
        if cantidades:
            bc.valueAxis.valueMax = max(cantidades) + 2 # Un poco más alto que el máximo
        bc.valueAxis.valueStep = 1  # Saltos de 1 en 1 (porque son conteos enteros)
        
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30 # Inclinamos las etiquetas si son largas
        bc.categoryAxis.categoryNames = meses
        
        # Colores de las barras
        bc.bars[0].fillColor = colors.purple
        
        d.add(bc)
        elements.append(d)
        elements.append(Spacer(1, 20))

        # 5. Tabla de Datos
        t = Table(table_data, colWidths=[150, 100])
        estilo_tabla = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ])
        t.setStyle(estilo_tabla)
        elements.append(t)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    @staticmethod
    def reporte_facturacion_mensual():
        """
        Genera un reporte de barras con la facturación total por mes.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        styles = getSampleStyleSheet()

        # 1. Título
        title_style = styles['Heading1']
        title_style.alignment = 1
        elements.append(Paragraph("Facturación Total Mensual", title_style))
        elements.append(Spacer(1, 20))

        # 2. Consulta SQL (Agrupado por Mes sobre Facturas)
        conn = Database().get_connection()
        cursor = conn.cursor()
        query = """
            SELECT strftime('%Y-%m', fecha_hora_emision) as mes, SUM(monto_total) as total
            FROM Facturas
            GROUP BY mes
            ORDER BY mes ASC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            elements.append(Paragraph("No hay datos históricos de facturación.", styles['Normal']))
            doc.build(elements)
            buffer.seek(0)
            return buffer

        # 3. Preparar datos
        meses = []
        montos = []
        table_data = [['Mes', 'Facturación Total']]

        for row in resultados:
            meses.append(row['mes'])
            montos.append(row['total'])
            table_data.append([row['mes'], f"${row['total']:,.2f}"])

        # 4. Crear Gráfico de Barras
        d = Drawing(400, 200)
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = [montos]
        bc.strokeColor = colors.black
        
        # Ejes
        bc.valueAxis.valueMin = 0
        if montos:
            bc.valueAxis.valueMax = max(montos) * 1.1 # Margen superior del 10%
        
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = meses
        
        # Color: Verde oscuro (Dinero)
        bc.bars[0].fillColor = colors.darkgreen 
        
        d.add(bc)
        elements.append(d)
        elements.append(Spacer(1, 20))

        # 5. Tabla
        t = Table(table_data, colWidths=[150, 150])
        estilo_tabla = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.honeydew]),
        ])
        t.setStyle(estilo_tabla)
        elements.append(t)
        
        # Total global al pie
        total_global = sum(montos)
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"<b>Facturación Histórica Total:</b> ${total_global:,.2f}", styles['Normal']))

        doc.build(elements)
        buffer.seek(0)
        return buffer