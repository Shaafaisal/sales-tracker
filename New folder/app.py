from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Initialize the FastAPI app
app = FastAPI(title="NexPOS Backend")

# Enable CORS so your HTML file can communicate with this API
# (Crucial when running the frontend locally from a file:// or different localhost port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# In-memory "database" to store our transactions
sales_data = [
    # Adding a bit of dummy data so your charts aren't empty on load
    {"product": "Laptop", "amount": 65000.00},
    {"product": "Smartphone", "amount": 25000.00},
    {"product": "Wireless Headphones", "amount": 4500.00}
]

# Define the data structure expected from the frontend
class Transaction(BaseModel):
    product: str
    amount: float

@app.get("/api/sales")
async def get_sales():
    """Returns all sales data to populate the dashboard."""
    return sales_data

@app.post("/api/sales")
async def add_sale(transaction: Transaction):
    """Receives a new transaction and appends it to the database."""
    # .model_dump() converts the Pydantic model to a standard dictionary
    sales_data.append(transaction.model_dump())
    return {"status": "success", "message": "Transaction recorded"}

@app.delete("/api/sales")
async def reset_sales():
    """Wipes all data when the Reset button is clicked."""
    sales_data.clear()
    return {"status": "success", "message": "Dashboard reset"}

if __name__ == "__main__":
    import uvicorn
    # Runs the server on exactly the host and port your frontend expects
    uvicorn.run(app, host="127.0.0.1", port=8000)