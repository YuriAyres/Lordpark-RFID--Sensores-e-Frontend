// ip_teste = 192.168.18.31
// ip_atitus = 10.1.24.62
ipApi = "10.1.24.62";

// Verifica se o usuário está logado ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    const isAdmin = localStorage.getItem('isAdmin') === 'true';
    
    if (localStorage.getItem('loggedIn') === 'true') {
        document.getElementById('login-container').style.display = 'none';
        if (isAdmin) {
            document.getElementById('admin-container').style.display = 'block';
            carregarCarrosAdmin();
        } else {
            document.getElementById('user-container').style.display = 'block';
            carregarCarrosUsuario();

            // Mostra a seleção de placas apenas para usuários padrão
            document.getElementById('car-selection').style.display = 'block';
        }
    } else {
        document.getElementById('login-container').style.display = 'block';
        document.body.style.overflow = 'hidden';
        document.getElementById('faixa-preta').style.display = 'none';
        document.getElementById('titulo-superior').style.display = 'none';
        document.getElementById('titulo-principal').style.display = 'block';
        document.getElementById('vagas-disponiveis-container').style.display = 'none';
    }
});
async function carregarCarrosAdmin() {
    document.body.style.overflow = 'auto';
    document.getElementById('faixa-preta').style.display = 'block';
    try {
        const response = await fetch(`http://${ipApi}:5000/carros`);
        if (!response.ok) {
            throw new Error('Erro ao buscar todos os carros');
        }
        const carros = await response.json();
        const tabela = document.querySelector('#admin-container .table tbody');
        tabela.innerHTML = '';

        carros.forEach(carro => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${carro.placa}</td>
                <td>${carro.nome}</td>
                <td>${carro.status}</td>
                <td>${carro.reserva}</td>
            `;
            tabela.appendChild(row);
        });
    } catch (error) {
        console.error('Erro ao carregar todos os carros:', error);
    }}
        

// Lógica de autenticação ao enviar o formulário de login
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'admin' && password === 'senha123') {
        localStorage.setItem('loggedIn', 'true');
        localStorage.setItem('isAdmin', 'true');
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('admin-container').style.display = 'block';
        carregarCarrosAdmin();
    } else if ((username === 'Cristiano ronaldo' && password === 'senha123') || 
               (username === 'Mauricio Hugo' && password === 'senha456')) {
        localStorage.setItem('loggedIn', 'true');
        localStorage.setItem('isAdmin', 'false');
        localStorage.setItem('username', username);  // Armazena o username para filtrar carros
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('user-container').style.display = 'block';
        document.getElementById('titulo-principal').style.display = 'none';
        document.getElementById('vagas-disponiveis-container').style.display = 'block';
        carregarCarrosUsuario();
    } else {
        document.getElementById('login-error').style.display = 'block';
    }
});

// Função para deslogar ao clicar no botão "Logoff"
document.querySelectorAll("#logoff-button, #logoff-button-user").forEach(button => {
    button.addEventListener("click", function() {
        localStorage.removeItem('loggedIn'); // Remove o estado de login
        localStorage.removeItem('isAdmin');   // Remove a flag de admin, se existir
        
        // Oculta todos os containers e exibe o login novamente
        document.getElementById("admin-container").style.display = "none";
        document.getElementById("user-container").style.display = "none";
        document.getElementById("login-container").style.display = "block";
        document.body.style.overflow = 'hidden';
        document.getElementById('faixa-preta').style.display = 'none';
        document.getElementById('titulo-superior').style.display = 'none';
        document.getElementById('titulo-principal').style.display = 'block';
        document.getElementById('vagas-disponiveis-container').style.display = 'none';
    });
});

// Função para carregar os carros do usuário logado e preencher o select
async function carregarCarrosUsuario() {
    document.body.style.overflow = 'auto'; 
    document.getElementById('faixa-preta').style.display = 'block';
    document.getElementById('titulo-superior').style.display = 'block';
    document.getElementById('titulo-principal').style.display = 'none';
    const username = localStorage.getItem('username');
    try {
        const response = await fetch(`http://${ipApi}:5000/login/${username}`);
        if (!response.ok) {
            throw new Error('Erro ao buscar carros do usuário');
        }
        const carros = await response.json();
        const tabela = document.querySelector('#user-container .table tbody');
        tabela.innerHTML = '';
        
        const carSelect = document.getElementById('car-select');
        carSelect.innerHTML = ''; // Limpa as opções anteriores

        // Variável para somar os valores dos carros do usuário
        let valorTotal = 0;

        document.getElementById('Usuario').innerHTML =(`${username}`)

        carros.forEach(carro => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${carro.placa}</td>
                <td>${carro.modelo}</td>
                <td>${carro.status}</td>
                <td>${carro.reserva}</td>
                <td>${carro.tempo ?? ''}</td>
               <td>R$: ${!isNaN(parseFloat(carro.valor)) ? parseFloat(carro.valor).toFixed(2) : '0.00'}</td>

            `;
            tabela.appendChild(row);

            // Adiciona a placa ao select
            const option = document.createElement('option');
            option.value = carro.placa;
            option.textContent = carro.placa;
            carSelect.appendChild(option);

            // Adiciona o valor do carro ao total, se existir
            if (carro.valor) {
                valorTotal += parseFloat(carro.valor);
            }

        // Armazena o valor total no localStorage para uso em outras funções
        localStorage.setItem('valorTotal', valorTotal.toFixed(2));

        // Chama carregarValor para atualizar o valor total na tela
        carregarValor();
        });
    } catch (error) {
        console.error('Erro ao carregar carros do usuário:', error);
    }
}

// Função para enviar a solicitação de reserva
async function reservarCarro() {
    const placa = document.getElementById('car-select').value;
    try {
        const response = await fetch(`http://${ipApi}:5000/reservar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ placa }),
        });

        if (!response.ok) {
            throw new Error('Erro ao realizar reserva');
        }
        
        // Exibe mensagem de sucesso
        document.getElementById('reserve-message').style.display = 'block';

        // Oculta a mensagem após alguns segundos
        setTimeout(() => {
            document.getElementById('reserve-message').style.display = 'none';
        }, 3000);

    } catch (error) {
        console.error('Erro ao reservar carro:', error);
    }
}

// Adiciona o evento ao botão de reserva
document.getElementById('reserve-button').addEventListener('click', reservarCarro);

async function carregarVagasDisponiveis() {
    try {
        const response = await fetch(`http://${ipApi}:5000/vagas`);
        if (!response.ok) {
            throw new Error('Erro ao buscar o número de vagas disponíveis');
        }
        const data = await response.json();
        const vagas = data.sensores_inativos;
        document.getElementById('vagas-disponiveis').textContent = vagas
            ? `Existem ${vagas} vagas disponíveis.`
            : 'Nenhuma vaga disponível.';
    } catch (error) {
        console.error('Erro ao carregar vagas:', error);
        document.getElementById('vagas-disponiveis').textContent = 'Erro ao buscar o número de vagas.';
    }
}

// Função para enviar a solicitação de pagamento
async function pagar() {
    const nome = localStorage.getItem('username');
    try {
        const response = await fetch(`http://${ipApi}:5000/pagar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nome }),
        });

        if (!response.ok) {
            throw new Error('Erro ao realizar pagamento');
        }
        
        // Exibe mensagem de sucesso
        document.getElementById('pagamento-message').style.display = 'block';

        // Oculta a mensagem após alguns segundos
        setTimeout(() => {
            document.getElementById('pagamento-message').style.display = 'none';
        }, 3000);

    } catch (error) {
        console.error('Erro ao realizar pagamento:', error);
    }
}

// Adiciona o evento ao botão de pagamento
document.getElementById('pagamento-button').addEventListener('click', pagar);

async function carregarValor() {
    // Recupera o valor total do localStorage e exibe na página
    const valorTotal = localStorage.getItem('valorTotal');
    document.getElementById('valor').textContent = `Valor total: R$: ${valorTotal}`;
}


// Chamando a função carregarVagasDisponiveis a cada 5 segundos
setInterval(carregarVagasDisponiveis, 5000);

// Atualiza os carros a cada 5 segundos, mas apenas se o usuário estiver logado
setInterval(() => {
    if (localStorage.getItem('loggedIn') === 'true') {
        const isAdmin = localStorage.getItem('isAdmin') === 'true';

        // Se for admin, chama a função de carros admin
        if (isAdmin) {
            carregarCarrosAdmin();
        } else {
            // Se não for admin, chama a função de carros do usuário
            carregarCarrosUsuario();
        }
    }
}, 5000);
