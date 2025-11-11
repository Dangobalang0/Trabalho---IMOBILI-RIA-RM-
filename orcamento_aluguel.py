import csv
from datetime import datetime

# --- Classes ---

class Imovel:
    def __init__(self, tipo, base, extra_quarto, extra_garagem):
        self.tipo = tipo
        self.base = base
        self.extra_quarto = extra_quarto
        self.extra_garagem = extra_garagem
        self.quartos = 1
        self.tem_garagem = False
        self.tem_criancas = False
        self.vagas_estudio = 0

    def calc_base(self):
        aluguel = self.base

        if self.quartos == 2:
            aluguel += self.extra_quarto
        
        if self.tem_garagem and self.tipo in ["Apartamento", "Casa"]:
            aluguel += self.extra_garagem

        return aluguel

    def aplicar_descontos(self, aluguel):
        return aluguel

    def calc_final(self):
        aluguel = self.calc_base()
        aluguel = self.aplicar_descontos(aluguel)
        return aluguel

class Apartamento(Imovel):
    def __init__(self):
        super().__init__("Apartamento", 700.00, 200.00, 300.00)

    def aplicar_descontos(self, aluguel):
        # Desconto de 5% para quem não tem crianças
        if not self.tem_criancas:
            aluguel *= 0.95
        return aluguel

class Casa(Imovel):
    def __init__(self):
        super().__init__("Casa", 900.00, 250.00, 300.00)

class Estudio(Imovel):
    def __init__(self):
        super().__init__("Estudio", 1200.00, 0.00, 0.00)

    def calc_base(self):
        aluguel = self.base
        
        if self.vagas_estudio > 0:
            # 2 vagas por R$ 250,00
            aluguel += 250.00
            
            # Vagas extras a R$ 60,00 cada
            if self.vagas_estudio > 2:
                vagas_extras = self.vagas_estudio - 2
                aluguel += vagas_extras * 60.00
        
        return aluguel

class Orcamento:
    CONTRATO = 2000.00
    MAX_PARCELAS = 5

    def __init__(self, imovel):
        self.imovel = imovel
        self.parcelas = 1
        self.mensal = imovel.calc_final()
        self.parcela_contrato = self.CONTRATO / self.parcelas

    def set_parcelas(self, parcelas):
        if 1 <= parcelas <= self.MAX_PARCELAS:
            self.parcelas = parcelas
            self.parcela_contrato = self.CONTRATO / self.parcelas
        else:
            raise ValueError(f"Parcelas entre 1 e {self.MAX_PARCELAS}.")

    def gerar_csv(self, nome_arquivo="orcamento_parcelas.csv"):
        data_atual = datetime.now()
        
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Mes', 'Valor_Aluguel', 'Parcela_Contrato', 'Valor_Total_Mensal']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()

            for i in range(1, 13):
                valor_aluguel = self.mensal
                parcela_contrato = self.parcela_contrato if i <= self.parcelas else 0.00
                valor_total = valor_aluguel + parcela_contrato
                
                # Cálculo de mês para evitar erro de range
                mes_atual = data_atual.month
                ano_atual = data_atual.year
                
                novo_mes = mes_atual + i
                novo_ano = ano_atual + (novo_mes - 1) // 12
                novo_mes = (novo_mes - 1) % 12 + 1
                
                mes_referencia = datetime(novo_ano, novo_mes, 1)
                
                writer.writerow({
                    'Mes': mes_referencia.strftime('%Y-%m'),
                    'Valor_Aluguel': f"{valor_aluguel:.2f}".replace('.', ','),
                    'Parcela_Contrato': f"{parcela_contrato:.2f}".replace('.', ','),
                    'Valor_Total_Mensal': f"{valor_total:.2f}".replace('.', ',')
                })
        
        return nome_arquivo

# --- Funções de Terminal ---

def get_imovel():
    while True:
        print("\n--- Tipo de Imóvel ---")
        print("1. Apartamento (R$ 700,00)")
        print("2. Casa (R$ 900,00)")
        print("3. Estúdio (R$ 1200,00)")
        escolha = input("Escolha (1, 2 ou 3): ")
        
        if escolha == '1':
            return Apartamento()
        elif escolha == '2':
            return Casa()
        elif escolha == '3':
            return Estudio()
        else:
            print("Opção inválida.")

def config_imovel(imovel):
    
    if imovel.tipo in ["Apartamento", "Casa"]:
        while True:
            quartos = input(f"Quartos (1 ou 2)? ")
            if quartos in ['1', '2']:
                imovel.quartos = int(quartos)
                break
            else:
                print("Inválido. Digite 1 ou 2.")

    if imovel.tipo in ["Apartamento", "Casa"]:
        while True:
            garagem = input(f"Garagem (S/N)? ").upper()
            if garagem in ['S', 'N']:
                imovel.tem_garagem = (garagem == 'S')
                break
            else:
                print("Inválido. Digite S ou N.")
    
    elif imovel.tipo == "Estudio":
        while True:
            try:
                vagas = int(input("Vagas de estacionamento (0, 1, 2...)? "))
                if vagas >= 0:
                    imovel.vagas_estudio = vagas
                    break
                else:
                    print("Número deve ser zero ou positivo.")
            except ValueError:
                print("Inválido. Digite um número inteiro.")

    if imovel.tipo == "Apartamento":
        while True:
            criancas = input("Tem crianças (S/N)? ").upper()
            if criancas in ['S', 'N']:
                imovel.tem_criancas = (criancas == 'S')
                break
            else:
                print("Inválido. Digite S ou N.")

def get_parcelamento(orcamento):
    while True:
        try:
            parcelas = int(input(f"Parcelar contrato de R$ {orcamento.CONTRATO:.2f} em quantas vezes (máx. {orcamento.MAX_PARCELAS})? "))
            orcamento.set_parcelas(parcelas)
            break
        except ValueError as e:
            print(f"Erro: {e}")
        except Exception:
            print("Inválido. Digite um número inteiro entre 1 e 5.")

def show_orcamento(orcamento):
    print("\n" + "="*40)
    print("        RESUMO DO ORÇAMENTO R.M.        ")
    print("="*40)
    print(f"Imóvel: {orcamento.imovel.tipo}")
    
    if orcamento.imovel.tipo in ["Apartamento", "Casa"]:
        print(f"Quartos: {orcamento.imovel.quartos}")
        if orcamento.imovel.tem_garagem:
            print("Garagem: Sim")
        if orcamento.imovel.tipo == "Apartamento" and not orcamento.imovel.tem_criancas:
            print("Desconto de 5% aplicado (sem crianças)")
    elif orcamento.imovel.tipo == "Estudio":
        print(f"Vagas: {orcamento.imovel.vagas_estudio}")

    print("-" * 40)
    print(f"Aluguel Mensal: R$ {orcamento.mensal:.2f}")
    print(f"Contrato (Total): R$ {orcamento.CONTRATO:.2f}")
    print(f"Parcelamento: {orcamento.parcelas}x")
    print(f"Parcela Contrato: R$ {orcamento.parcela_contrato:.2f}")
    print("-" * 40)
    
    primeira_mensalidade = orcamento.mensal + orcamento.parcela_contrato
    print(f"TOTAL MENSAL (Primeiras {orcamento.parcelas} parcelas): R$ {primeira_mensalidade:.2f}")
    print(f"TOTAL MENSAL (Após parcelamento): R$ {orcamento.mensal:.2f}")
    print("="*40)

def main():
    print("="*50)
    print("  APLICAÇÃO DE ORÇAMENTO DE ALUGUEL R.M.  ")
    print("="*50)
    
    imovel = get_imovel()
    config_imovel(imovel)
    
    orcamento = Orcamento(imovel)
    
    get_parcelamento(orcamento)
    
    show_orcamento(orcamento)
    
    while True:
        gerar_csv = input("\nGerar CSV com 12 parcelas (S/N)? ").upper()
        if gerar_csv in ['S', 'N']:
            if gerar_csv == 'S':
                nome_arquivo = orcamento.gerar_csv()
                print(f"\nCSV gerado: {nome_arquivo}")
            break
        else:
            print("Inválido. Digite S ou N.")

if __name__ == "__main__":
    main()
