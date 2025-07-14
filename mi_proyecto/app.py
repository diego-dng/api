from flask import Flask, request, jsonify
import pandas as pd
import os
import pickle
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods = ['GET'])
def main():
    return "API del modelo"

# 1. Ofrezca la predicción de ventas a partir de todos los valores de gastos en publicidad. (/predict)
@app.route("/predict", methods = ['GET'])
def predict():
    try:
        data = request.get_json()
        print(data)
        if not data or 'data' not in data:
            return jsonify({"Error":"No se han proporcionado datos"}), 400

        data = data.get("data", None) 
        print("----------------------", data)
        modelo = pickle.load(open("data/modelo_advertising.pkl", "rb"))
        pred = modelo.predict(data)
        print("fdsfsdsfdsfdsfdsfdfdssfdsfdsfdsfdsfdsfdhola", pred)
        # return f"La predicción es: {round(pred[0], 2)}"
        return jsonify({"prediction": f"prediction {pred}"}), 200

    except Exception as e:
        return jsonify({"Error": f"Se ha producido un error ----- {e}"}), 500 

# 2. Un endpoint para almacenar nuevos registros en la base de datos que deberás crear previamente.(/ingest)

@app.route("/ingest", methods = ['POST'])
def ingest():
    data = request.get_json()
    if not data:
        return jsonify({"Error": "No se han proporcionado datos"})
    try:
        data = data.get("data", None)


        con = sqlite3.connect('data/advertising.db')
        cursor = con.cursor()
        query = "INSERT INTO campañas VALUES (?,?,?,?)"
        for i in data:
            cursor.execute(query, i)
        
        con.commit()
        con.close()

        return jsonify({"message": "Datos ingresados correctamente"}), 200
    except Exception as e:
        return jsonify({"Error": f"Se ha producido un error ---- {e}"})

# 3. Posibilidad de reentrenar de nuevo el modelo con los posibles nuevos registros que se recojan. (/retrain)
@app.route("/retrain", methods = ['POST'])
def retrain():
    try:
        con = sqlite3.connect("data/advertising.db")
        cursor = con.cursor()
        query = "SELECT * FROM campañas"
        result = cursor.execute(query).fetchall()
        df = pd.DataFrame(result)
        con.close()
        modelo = pickle.load(open("data/modelo_advertising.pkl", "rb"))
        modelo.fit(df.iloc[:, :-1], df.iloc[:, -1])
        with open("data/advertising_model_nuevo.pkl", "wb") as file:
            pickle.dump(modelo, file)
        return {"message": "Modelo reentrenado correctamente."}, 200
    except Exception as e:
        return jsonify({"error": f"Se ha produccido este error --- {e}"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)