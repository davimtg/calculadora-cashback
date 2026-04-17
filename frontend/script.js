const API_URL = 'https://calculadora-cashback-production.up.railway.app'; 

carregarHistorico();

document.getElementById('cashbackForm').onsubmit = function(event) {
    event.preventDefault();

    let valorCompra = document.getElementById('valorCompra').value;
    let descontoCupom = document.getElementById('descontoCupom').value;
    let tipoCliente = document.getElementById('tipoCliente').value;
    
    let eVip = false;
    if (tipoCliente === 'vip') {
        eVip = true;
    }

    if (descontoCupom === "") {
        descontoCupom = 0;
    }

    let payload = {
        valor_compra: parseFloat(valorCompra),
        e_vip: eVip,
        desconto_cupom: parseFloat(descontoCupom)
    };

    fetch(API_URL + '/calcular', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            alert("Erro ao calcular o cashback na API.");
        }
    })
    .then(function(data) {
        if (data) {
            document.getElementById('valorCashback').innerText = data.cashback.toFixed(2);
            document.getElementById('resultBox').style.display = 'block';
            carregarHistorico(); 
        }
    })
    .catch(function(error) {
        console.log("Erro de conexão:", error);
        alert("Não foi possível conectar à API.");
    });
};

function carregarHistorico() {
    fetch(API_URL + '/historico')
    .then(function(response) {
        return response.json();
    })
    .then(function(dados) {
        let tbody = document.querySelector('#historicoTable tbody');
        tbody.innerHTML = ''; 

        if (dados.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3">Nenhum histórico encontrado para o seu IP.</td></tr>';
        } else {
            for (let i = 0; i < dados.length; i++) {
                let item = dados[i];
                let linha = '<tr>' +
                    '<td>R$ ' + parseFloat(item.valor_compra).toFixed(2) + '</td>' +
                    '<td>' + item.tipo_cliente + '</td>' +
                    '<td>R$ ' + parseFloat(item.cashback_gerado).toFixed(2) + '</td>' +
                '</tr>';
                
                tbody.innerHTML += linha;
            }
        }
    });
}