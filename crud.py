from connection_bd import get_db
from datetime import datetime

db = get_db()
productos_col = db["productos"]
ventas_col = db["ventas"]

# --- CASO 1: Crear con validación ---
def registrar_producto(id_p, nombre, precio, stock):
    if productos_col.find_one({"id_p": id_p}):
        return "Error: El producto ya existe."
    productos_col.insert_one({"id_p": id_p, "nombre": nombre, "precio": precio, "stock": stock})
    return "Producto registrado."

# --- CASO 2: Transacción manual (Venta con resta de stock) ---
def realizar_venta(id_p, cantidad):
    producto = productos_col.find_one({"id_p": id_p})
    if not producto:
        return "Producto no encontrado."
    
    if producto["stock"] < cantidad:
        return f"Stock insuficiente. Solo quedan {producto['stock']} unidades."

    # 1. Restar stock
    productos_col.update_one({"id_p": id_p}, {"$inc": {"stock": -cantidad}})
    
    # 2. Registrar venta con fecha
    venta = {
        "id_p": id_p,
        "cantidad": cantidad,
        "precio_unitario": producto["precio"],
        "fecha": datetime.now()
    }
    ventas_col.insert_one(venta)
    return "Venta realizada con éxito."

# --- CASO 3: Agregación Compleja ($lookup + $project + $addFields) ---
def listar_ventas_detalladas():
    """Une ventas con productos y calcula el total de cada venta"""
    pipeline = [
        {
            "$lookup": {
                "from": "productos",
                "localField": "id_p",
                "foreignField": "id_p",
                "as": "info_producto"
            }
        },
        {"$unwind": "$info_producto"},
        {
            "$project": {
                "_id": 0,
                "fecha": 1,
                "producto": "$info_producto.nombre",
                "cantidad": 1,
                "total_venta": {"$multiply": ["$cantidad", "$precio_unitario"]}
            }
        }
    ]
    return list(ventas_col.aggregate(pipeline))

# --- CASO 4: Reporte de Ganancias ($group + $sum) ---
def reporte_total_ganancias():
    """Calcula cuánto dinero ha ganado la tienda en total"""
    pipeline = [
        {
            "$group": {
                "_id": None,
                "gran_total": {"$sum": {"$multiply": ["$cantidad", "$precio_unitario"]}},
                "total_productos_vendidos": {"$sum": "$cantidad"}
            }
        }
    ]
    return list(ventas_col.aggregate(pipeline))