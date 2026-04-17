def calculaCashback(valorCompra, eVip, descontoCupom):
    cashbackBase = 0.05
    valorTotal= valorCompra - (valorCompra*(descontoCupom/100))
    cashback = valorTotal*cashbackBase
    # Usei o multiplicador fatorPromocao afim de evitar o uso de mais if's tornando o codigo mais otimizafdo
    fatorPromocao = 1
    if valorTotal > 500:
        fatorPromocao = 2
    if eVip == True:
        
        cashbackVip = (cashback+cashback*0.10)
        #print (cashbackVip * fatorPromocao)
        return cashbackVip * fatorPromocao
    else:
        #print (cashback * fatorPromocao)
        return cashback * fatorPromocao
    
if __name__ == '__main__':
    print("="*40)
    print(" CALCULADORA DE CASHBACK (Terminal) ")
    print("="*40)
    
    try:
        valor_input = float(input("Digite o valor da compra (R$): "))
        cupom_input = float(input("Digite o '%' de desconto do cupom (0 se não houver): "))
        vip_input = input("O cliente é VIP? (S/N): ").strip().upper()
        
        is_vip = True if vip_input == 'S' else False
        
        # Chamando a func
        resultado_cashback = calculaCashback(valor_input, is_vip, cupom_input)
        
        print("\n" + "-"*40)
        print("REsSUMO DA COMPRA ")
        print("-"*40)
        print(f"Cliente VIP     : {'Sim' if is_vip else 'Não'}")
        print(f"Cashback Gerado : R$ {resultado_cashback:.2f}")
        print("="*40 + "\n")
        
    except ValueError:
        print("\nDigite numeros válidos.")