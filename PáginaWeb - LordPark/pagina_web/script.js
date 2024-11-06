// Verifica se o usuário está logado ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    if (localStorage.getItem('loggedIn') === 'true') {
        const isAdmin = localStorage.getItem('isAdmin') === 'true';
        document.getElementById('login-container').style.display = 'none';

        if (isAdmin) {
            document.getElementById('admin-container').style.display = 'block';
            carregarCarrosAdmin();
        } else {
            document.getElementById('user-container').style.display = 'block';
            carregarCarrosUsuario();
        }
    } else {
        document.getElementById('login-container').style.display = 'block';
    }
});

// Lógica de autenticação ao enviar o formulário de login
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'admin' && password === 'senha123') {
        localStorage.setItem('loggedIn', 'true');
        localStorage.setItem('isAdmin', 'true');
        document.getElementById('login-container').style.display = 'none';
        carregarCarrosAdmin();
    } else if ((username === 'user1' && password === 'senha123') || 
               (username === 'user2' && password === 'senha456') || 
               (username === 'user3' && password === 'senha789')) {
        localStorage.setItem('loggedIn', 'true');
        localStorage.setItem('isAdmin', 'false');
        localStorage.setItem('username', username);  // Armazena o username para filtrar carros
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('user-container').style.display = 'block';
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
    });
});


// Função para carregar os carros do usuário logado
async function carregarCarrosUsuario() {
    const username = localStorage.getItem('username');
    try {
        const response = await fetch(`http://10.1.24.62:5000/login/${username}`);
        if (!response.ok) {
            throw new Error('Erro ao buscar carros do usuário');
        }
        const carros = await response.json();
        const tabela = document.querySelector('#user-container .table tbody');
        tabela.innerHTML = '';

        carros.forEach(carro => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${carro.placa}</td>
                <td>${carro.modelo}</td>
                <td>${carro.status}</td>
                <td>${carro.reserva}</td>
            `;
            tabela.appendChild(row);
        });
    } catch (error) {
        console.error('Erro ao carregar carros do usuário:', error);
    }
}

// Função para carregar os carros do administrador
async function carregarCarrosAdmin() {
    try {
        const response = await fetch('http://10.1.24.62:5000/carros');
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
    }
}
