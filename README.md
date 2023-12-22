# Descripción
Programa de vendedor virtual

# Como ejecutar
El programa esta hecho en FastAPI (Python 3.10+) por lo que debemos tenerlo instalado. Para esto primero debemos instalar las librerias con `pip install -r requeriments.txt` donde viene `uvicorn` con el que se ejecutara la API. Para iniciar el programa hacemos `uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload`

## Descripción algoritmo
Para hacer el cálculo del score se dividió en cinco ejes principales en donde cada uno de estos otorga un porcentaje del score final:

- Cantidad de mensajes enviados: Este otorga el 10% del score final del usuario, donde cada mensaje brinda cierta cantidad puntaje, disminuyendo el extra exponencialmente cada vez que el usuario envía un mensaje nuevo.
- Cantidad ahorrada: Este otorga el 30% del score final del usuario. Este se basó en cuanta cantidad del pie de la propiedad tiene ahorrado el cliente, otorgando puntaje máximo si ese ahorro es mayor a este pie base. En caso de no tenerlo se otorga un menor porcentaje, el cual va disminuyendo linealmente.
- Salario del cliente: Este otorga el 30% del score final del usuario. En este caso trabajamos directamente con el monto de crédito que necesita pedir el usuario y asumimos que se pagaran en 300 cuotas (25 años). Otro factor sé que asumió fue que el 30% del salario del usuario debía ser mayor a la cuota mensual del crédito en donde si cumplía esto se le otorgaba puntaje máximo, en caso contrario el puntaje disminuye linealmente.
- Fechas de las deudas: Este otorga un 10% del score final del usuario. Para esto solo sacamos la cantidad de días de atraso de todas las deudas morosas (+30 días). Si el cliente suma 0 días de atraso en estas deudas se otorga puntaje máximo, en caso contrario el puntaje va disminuyendo de manera exponencial.
- Monto de las deudas: Este otorga un 20% del score final del usuario. Aquí se saca el monto total de deuda morosa (+30 días). Aquí se otorga puntaje máximo en caso de que este monto sume cero, en caso contrario el puntaje va disminuyendo de manera exponencial.

  
