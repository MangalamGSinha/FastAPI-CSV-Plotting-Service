# 📊 FastAPI-CSV-Plotting-Service
---

A FastAPI-powered backend service to generate a wide range of plots from uploaded CSV files. It supports common chart types like line, scatter, histogram, bar, box, violin, pie, heatmap, and area — and returns the plots in various formats (PNG, JPG, SVG, PDF).

---

## 🚀 Features

- ✅ Accepts CSV file upload via POST request
- ✅ Supports 9 different plot types
- ✅ Outputs plots in PNG, JPG, SVG, or PDF
- ✅ Customizable titles, axis labels, figure size, and DPI
- ✅ Automatically handles grouped plots and heatmaps

---

## 📦 Installation

### Clone the repository and install the required packages.

```bash
git clone https://github.com/your-username/csv-plotting-api.git
cd csv-plotting-api
pip install fastapi uvicorn pandas matplotlib seaborn numpy
```

---

### ▶️ Running the API

Start the server using:

```bash
python -m uvicorn main:app --reload
```

---
### 🧪 Using Swagger UI

After starting the server, open your browser and navigate to:

👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

* This will open **FastAPI Swagger UI**, an interactive interface to:

  * Upload your CSV file
  * Select plot type and configure parameters
  * Preview responses and download images

Scroll to the /plot/ endpoint → Click Try it out → Fill JSON → Click Execute.

---


## 📤 API Endpoints

### `GET /`

Returns basic information about the API.

---

### `POST /plot_csv`

Generates a plot based on the uploaded CSV and form parameters.

#### Form Parameters:

| Parameter        | Required | Description                                                                                 |
| ---------------- | -------- | ------------------------------------------------------------------------------------------- |
| `file`           | ✅        | CSV file to upload                                                                          |
| `x_col`          | ✅        | Column name for X-axis                                                                      |
| `y_col`          | ❌        | Column name for Y-axis (optional for some plot types)                                       |
| `plot_type`      | ❌        | Plot type: `line`, `scatter`, `bar`, `histogram`, `box`, `violin`, `heatmap`, `area`, `pie` |
| `xlabel`         | ❌        | Label for X-axis                                                                            |
| `ylabel`         | ❌        | Label for Y-axis                                                                            |
| `title`          | ❌        | Plot title                                                                                  |
| `figsize_width`  | ❌        | Width of the plot (default: 10)                                                             |
| `figsize_height` | ❌        | Height of the plot (default: 6)                                                             |
| `output_format`  | ❌        | Output format: `png`, `jpg`, `svg`, `pdf`                                                   |
| `dpi`            | ❌        | DPI (image resolution)                                                                      |

---

## 📈 Supported Plot Types

| Type        | Notes                                        |
| ----------- | -------------------------------------------- |
| `line`      | Requires `x_col` and `y_col`                 |
| `scatter`   | Requires `x_col` and `y_col`                 |
| `bar`       | Aggregates `y_col` by `x_col`                |
| `histogram` | Only `x_col` is used                         |
| `box`       | Optionally grouped by `x_col`                |
| `violin`    | Optionally grouped by `x_col`                |
| `heatmap`   | Uses correlation between all numeric columns |
| `area`      | Area between `x_col` and `y_col`             |
| `pie`       | `x_col` is label, `y_col` is value           |

---

## 🧪 Example Request (Using `curl`)

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/plot_csv' \
  -H 'accept: image/png' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_data.csv' \
  -F 'x_col=column1' \
  -F 'y_col=column2' \
  -F 'plot_type=line' \
  --output result.png
```

---

## ⚙️ Requirements

* Python 3.7+
* FastAPI
* Uvicorn
* Pandas
* Matplotlib
* Seaborn
* NumPy

