import flet as ft
import requests

URL_API = "https://piuratasador-api.onrender.com"

def main(page: ft.Page):
    page.title = "PiuraTasador AI"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = "auto"

    titulo = ft.Text("🏠 PiuraTasador AI", size=28, weight="bold", color="blue")
    subtitulo = ft.Text("Tasador inteligente de alquileres en Piura", size=14, color="grey")

    resultado = ft.Text("Completa los datos y presiona Calcular", size=18, weight="bold", color="blue")
    caja_resultado = ft.Container(
        content=resultado,
        padding=15,
        bgcolor="#EEF2FF",
        border_radius=10,
    )

    distrito = ft.Dropdown(
        label="Distrito",
        options=[
            ft.dropdown.Option("Piura"),
            ft.dropdown.Option("Castilla"),
            ft.dropdown.Option("Veintiseis de Octubre"),
            ft.dropdown.Option("Lourdes"),
        ],
        value="Piura"
    )

    zona = ft.TextField(
        label="Urbanización o Zona (ej. El Chipe, Miraflores, Los Ejidos)",
        value="Miraflores"
    )

    tipo = ft.Dropdown(
        label="Tipo de Inmueble",
        options=[
            ft.dropdown.Option("Departamento"),
            ft.dropdown.Option("Casa"),
            ft.dropdown.Option("Minidepartamento"),
            ft.dropdown.Option("Habitacion"),
        ],
        value="Departamento"
    )

    habitaciones = ft.TextField(label="N° Habitaciones", value="3", keyboard_type=ft.KeyboardType.NUMBER)
    banos = ft.TextField(label="N° Baños", value="2", keyboard_type=ft.KeyboardType.NUMBER)
    area_m2 = ft.TextField(label="Área total (m²)", value="100", keyboard_type=ft.KeyboardType.NUMBER)
    cochera = ft.Switch(label="¿Tiene cochera?", value=True)
    amoblado = ft.Switch(label="¿Está amoblado?", value=False)

    def calcular_precio(e):
        resultado.value = "⏳ Conectando con la IA..."
        resultado.color = "orange"
        page.update()

        datos = {
            "distrito": distrito.value,
            "zona": zona.value,
            "tipo": tipo.value,
            "habitaciones": float(habitaciones.value or 1),
            "banos": float(banos.value or 1),
            "area_m2": float(area_m2.value or 50),
            "cochera": 1.0 if cochera.value else 0.0,
            "amoblado": 1.0 if amoblado.value else 0.0
        }

        try:
            respuesta = requests.post(URL_API, json=datos, timeout=60)
            if respuesta.status_code == 200:
                precio = respuesta.json()["precio"]
                resultado.value = f"💰 Alquiler estimado: S/ {precio:,.2f} / mes"
                resultado.color = "green"
            else:
                resultado.value = f"❌ Error {respuesta.status_code} en {respuesta.url}\nDetalle: {respuesta.text}"
                resultado.color = "red"
        except Exception as err:
            resultado.value = f"❌ Error de red: {str(err)}"
            resultado.color = "red"
        
        page.update()

    boton = ft.Button(
        content=ft.Text("Calcular Precio", size=16, weight="bold"),
        on_click=calcular_precio,
        bgcolor="blue",
        color="white",
        height=50,
        width=300
    )

    page.add(
        titulo, subtitulo, caja_resultado, ft.Divider(),
        distrito, zona, tipo, habitaciones, banos, area_m2,
        cochera, amoblado, boton
    )

ft.run(main)
