# 🛒 MELI Automation

Este proyecto realiza **web scraping de Mercado Libre Argentina** para extraer información de productos, incluyendo títulos, precios en pesos, valoraciones y enlaces. Además, convierte los precios a **dólares MEP**, obteniendo la cotización actual desde [DólarHoy.com](https://dolarhoy.com).

Ideal para comparar precios entre productos y entender su valor en moneda extranjera 🇦🇷💵

---

## ⚙️ Tecnologías utilizadas

- `Python 3.10+`
- `BeautifulSoup` – Web scraping
- `Requests` – Peticiones HTTP
- `Pandas` – Estructura y manipulación de datos
- `ExcelWriter` – Exportación a archivos `.xlsx`

---

## 🚀 ¿Qué hace este script?

- Solicita el nombre de un producto al usuario.
- Realiza una búsqueda en MercadoLibre.
- Extrae título, precio, rating y link de los primeros resultados.
- Convierte el precio a **USD MEP** en tiempo real.
- Genera un archivo `.xlsx` ordenado por precio.
- Listo para análisis o comparación de productos.

---

## 📦 Ejemplo de columnas exportadas

| Title          | Price (in Pesos) | Price (in USD MEP Dolars) | Rating      | Link      |
|----------------|------------------|----------------------------|-------------|-----------|
| Celular Moto G | 120.000          | 150,22                     | ⭐⭐⭐⭐        | ver link  |
| Smart TV LG    | 180.000          | 225,34                     | No Rating   | ver link  |

---

## ▶️ Cómo correr el script

1. Cloná el repositorio:

```bash
git clone https://github.com/juanifmera/MELI-Automation.git
cd MELI-Automation
