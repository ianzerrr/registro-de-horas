from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv

app = Flask(__name__)

# Nome do arquivo CSV para armazenar os registros
ARQUIVO_REGISTROS = "registros.csv"

# Função para salvar os registros no arquivo CSV
def salvar_registro_csv(registro):
    with open(ARQUIVO_REGISTROS, "a", newline="") as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(registro)

# Função para carregar os registros do arquivo CSV
def carregar_registros_csv():
    registros = []
    try:
        with open(ARQUIVO_REGISTROS, "r") as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            for linha in leitor:
                registros.append({
                    "data": linha[0],
                    "entrada": linha[1],
                    "saida": linha[2],
                    "horas_trabalhadas": linha[3],
                    "valor_acumulado": linha[4]
                })
    except FileNotFoundError:
        pass  # Se o arquivo não existir, retornaremos uma lista vazia
    return registros

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registrar", methods=["POST"])
def registrar():
    entrada = request.form["entrada"]
    saida = request.form["saida"]
    valor_hora = float(request.form["valor_hora"])
    
    try:
        # Calcula o total de horas trabalhadas e o valor acumulado
        hora_entrada = datetime.strptime(entrada, "%H:%M")
        hora_saida = datetime.strptime(saida, "%H:%M")
        horas_trabalhadas = (hora_saida - hora_entrada).total_seconds() / 3600
        
        if horas_trabalhadas < 0:
            return "Horário inválido: a saída não pode ser antes da entrada.", 400
        
        valor_acumulado = horas_trabalhadas * valor_hora
        data_trabalho = datetime.now().strftime("%d/%m/%Y")  # Data atual no formato DD/MM/AAAA
        
        # Salva o registro no arquivo CSV
        registro = [data_trabalho, entrada, saida, f"{horas_trabalhadas:.2f}", f"{valor_acumulado:.2f}"]
        salvar_registro_csv(registro)
        
        return redirect(url_for("index"))
    
    except Exception as e:
        return f"Erro: {e}", 400

@app.route("/registros")
def registros():
    registros = carregar_registros_csv()
    return render_template("registros.html", registros=registros)

if __name__ == "__main__":
    app.run(debug=True)
