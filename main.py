from fastapi import FastAPI, File, UploadFile, Form, Response, HTTPException
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
from typing import Optional
import warnings

# Suppress matplotlib warnings
warnings.filterwarnings('ignore')

app = FastAPI(
    title="CSV Plotting Service",
    description="Simple API for creating various types of plots from CSV data",
    version="1.5.0"
)

@app.get("/")
async def root():
    return {
        "message": "CSV Plotting Service",
        "version": "1.5.0",
        "supported_plot_types": [
            "line", "scatter", "bar", "histogram", "box", "violin", 
            "heatmap", "area", "pie"
        ],
        "supported_formats": ["png", "jpg", "svg", "pdf"],
        "usage": "POST /plot_csv with CSV file and parameters"
    }

@app.post("/plot_csv")
async def plot_csv(
    file: UploadFile = File(...),
    x_col: str = Form(...),
    y_col: Optional[str] = Form(None),
    plot_type: str = Form("line"),
    
    # Basic customization
    xlabel: str = Form(""),
    ylabel: str = Form(""),
    title: str = Form(""),
    figsize_width: float = Form(10),
    figsize_height: float = Form(6),
    
    # Output options
    output_format: str = Form("png"),
    dpi: int = Form(300)
):
    """
    Create plots from CSV data
    
    Supported plot types:
    - line: Line plot (requires x_col and y_col)
    - scatter: Scatter plot (requires x_col and y_col)
    - bar: Bar chart (requires x_col and y_col)
    - histogram: Histogram (requires only x_col)
    - box: Box plot (requires only x_col, or x_col and y_col for grouped)
    - violin: Violin plot (requires only x_col, or x_col and y_col for grouped)
    - heatmap: Correlation heatmap (ignores x_col and y_col, uses all numeric columns)
    - area: Area plot (requires x_col and y_col)
    - pie: Pie chart (requires x_col for labels and y_col for values)
    
    Supported output formats: png, jpg, svg, pdf
    """
    
    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Create figure
        plt.figure(figsize=(figsize_width, figsize_height))
        
        # Generate plot based on type
        if plot_type == "line":
            plt.plot(df[x_col], df[y_col])
            
        elif plot_type == "scatter":
            plt.scatter(df[x_col], df[y_col])
            
        elif plot_type == "bar":
            # Aggregate data if there are multiple values for same x
            plot_data = df.groupby(x_col)[y_col].mean()
            plt.bar(plot_data.index, plot_data.values)
            
        elif plot_type == "histogram":
            plt.hist(df[x_col].dropna(), bins=30, edgecolor='black', alpha=0.7)
            
        elif plot_type == "box":
            if y_col:
                # Grouped box plot
                sns.boxplot(data=df, x=x_col, y=y_col)
            else:
                # Single box plot
                plt.boxplot(df[x_col].dropna())
                plt.xticks([1], [x_col])
                
        elif plot_type == "violin":
            if y_col:
                # Grouped violin plot
                sns.violinplot(data=df, x=x_col, y=y_col)
            else:
                # Single violin plot
                plt.violinplot(df[x_col].dropna(), positions=[1])
                plt.xticks([1], [x_col])
                
        elif plot_type == "heatmap":
            # Use all numeric columns for correlation heatmap
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            correlation_matrix = df[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
            
        elif plot_type == "area":
            plt.fill_between(df[x_col], df[y_col], alpha=0.7)
            plt.plot(df[x_col], df[y_col])
            
        elif plot_type == "pie":
            # Aggregate data for pie chart
            pie_data = df.groupby(x_col)[y_col].sum()
            plt.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%')
            plt.axis('equal')  # Equal aspect ratio ensures pie chart is circular
            
        else:
            # Default to line plot if unknown type
            plt.plot(df[x_col], df[y_col] if y_col else df[x_col])
        
        # Set labels and title
        if plot_type not in ["heatmap", "pie"]:
            plt.xlabel(xlabel if xlabel else x_col)
            if y_col and plot_type not in ["histogram"]:
                plt.ylabel(ylabel if ylabel else y_col)
        
        if title:
            plt.title(title)
        elif plot_type == "heatmap":
            plt.title("Correlation Heatmap")
        elif plot_type == "histogram":
            plt.title(f"Distribution of {x_col}")
        elif y_col:
            plt.title(f"{y_col} vs {x_col}")
        else:
            plt.title(f"{x_col}")
        
        # Add grid for most plot types
        if plot_type not in ["heatmap", "pie"]:
            plt.grid(True, alpha=0.3)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save plot
        buf = io.BytesIO()
        plt.savefig(buf, format=output_format, dpi=dpi, bbox_inches='tight')
        plt.close()
        buf.seek(0)
        
        # Set appropriate media type
        media_types = {
            "png": "image/png",
            "jpg": "image/jpeg", 
            "svg": "image/svg+xml",
            "pdf": "application/pdf"
        }
        
        return Response(content=buf.read(), media_type=media_types[output_format])
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating plot: {str(e)}")