from crud import (
    registrar_producto, realizar_venta, 
    listar_ventas_detalladas, reporte_total_ganancias
)

def menu():
    while True:
        print("\n--- SISTEMA DE VENTAS ---")
        print("1. Registrar Producto")
        print("2. Realizar Venta (Resta stock)")
        print("3. Ver Ventas Detalladas (Lookup)")
        print("4. Ver Reporte de Ganancias (Aggregation)")
        print("0. Salir")
        
        op = input("Seleccione: ")

        if op == "1":
            id_p = input("ID Producto: ")
            nom = input("Nombre: ")
            pre = float(input("Precio: "))
            stk = int(input("Stock inicial: "))
            print(registrar_producto(id_p, nom, pre, stk))

        elif op == "2":
            id_p = input("ID Producto a vender: ")
            cant = int(input("Cantidad: "))
            print(realizar_venta(id_p, cant))

        elif op == "3":
            ventas = listar_ventas_detalladas()
            print("\n--- HISTORIAL DE VENTAS ---")
            for v in ventas:
                print(f"Prod: {v['producto']} | Cant: {v['cantidad']} | Total: ${v['total_venta']}")

        elif op == "4":
            reporte = reporte_total_ganancias()
            if reporte:
                r = reporte[0]
                print(f"\nGAANANCIAS TOTALES: ${r['gran_total']}")
                print(f"PRODUCTOS VENDIDOS: {r['total_productos_vendidos']}")

        elif op == "0": break

if __name__ == "__main__":
    menu()