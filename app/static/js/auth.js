// Funções de manipulação do modal
function showModal() {
    const modal = document.getElementById('smsModal');
    modal.style.display = 'flex';
    showPhoneStep();
}

function hideModal() {
    const modal = document.getElementById('smsModal');
    modal.style.display = 'none';
    hideLoading();
}

function showPhoneStep() {
    document.getElementById('phoneStep').style.display = 'block';
    document.getElementById('codeStep').style.display = 'none';
    document.getElementById('phoneError').style.display = 'none';
    document.getElementById('phone').value = '';
}

function showCodeStep(phoneNumber) {
    document.getElementById('phoneStep').style.display = 'none';
    document.getElementById('codeStep').style.display = 'block';
    document.getElementById('codeError').style.display = 'none';
    document.getElementById('code').value = '';
    document.getElementById('confirmedPhone').textContent = phoneNumber;
}

function showLoading() {
    document.getElementById('globalLoading').style.display = 'block';
    // Desabilitar interações durante o loading
    document.body.style.pointerEvents = 'none';
    document.body.style.opacity = '0.7';
}

function hideLoading() {
    document.getElementById('globalLoading').style.display = 'none';
    // Reabilitar interações
    document.body.style.pointerEvents = 'auto';
    document.body.style.opacity = '1';
}

function showModalLoading() {
    const modalLoading = document.getElementById('modalLoading');
    const phoneStep = document.getElementById('phoneStep');
    const codeStep = document.getElementById('codeStep');
    
    if (modalLoading) {
        modalLoading.style.display = 'block';
    }
    
    // Desabilitar inputs durante o loading
    if (phoneStep) phoneStep.style.opacity = '0.5';
    if (codeStep) codeStep.style.opacity = '0.5';
    
    const inputs = document.querySelectorAll('#smsModal input, #smsModal button');
    inputs.forEach(input => input.disabled = true);
}

function hideModalLoading() {
    const modalLoading = document.getElementById('modalLoading');
    const phoneStep = document.getElementById('phoneStep');
    const codeStep = document.getElementById('codeStep');
    
    if (modalLoading) {
        modalLoading.style.display = 'none';
    }
    
    // Reabilitar inputs
    if (phoneStep) phoneStep.style.opacity = '1';
    if (codeStep) codeStep.style.opacity = '1';
    
    const inputs = document.querySelectorAll('#smsModal input, #smsModal button');
    inputs.forEach(input => input.disabled = false);
}

// Funções de autenticação
async function requestSmsCode() {
    const phoneInput = document.getElementById('phone');
    const phoneError = document.getElementById('phoneError');
    const phoneNumber = phoneInput.value.trim();

    // Limpar erro anterior
    phoneError.style.display = 'none';

    // Validação básica do número de telefone
    if (!phoneNumber.match(/^\+[0-9]{10,14}$/)) {
        phoneError.textContent = 'Formato inválido. Use: +5521964682154';
        phoneError.style.display = 'block';
        return;
    }

    try {
        showModalLoading();
        const response = await fetch(`${API_URL}/api/auth/phone/request`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ phone_number: phoneNumber })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Erro ao enviar código');
        }

        showCodeStep(phoneNumber);
    } catch (error) {
        console.error('Erro ao solicitar código:', error);
        phoneError.textContent = error.message || 'Erro ao enviar código. Tente novamente.';
        phoneError.style.display = 'block';
    } finally {
        hideModalLoading();
    }
}

async function verifyPhoneCode() {
    const phoneNumber = document.getElementById('confirmedPhone').textContent;
    const codeInput = document.getElementById('code');
    const codeError = document.getElementById('codeError');
    const code = codeInput.value.trim();

    // Limpar erro anterior
    codeError.style.display = 'none';

    // Validação do código
    if (!code.match(/^[0-9]{6}$/)) {
        codeError.textContent = 'O código deve ter 6 dígitos';
        codeError.style.display = 'block';
        return;
    }

    try {
        showModalLoading();
        showLoading(); // Mostrar loading global pois vamos redirecionar
        
        const response = await fetch(`${API_URL}/api/auth/phone/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
            },
            body: JSON.stringify({
                phone_number: phoneNumber,
                code: code
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Código inválido');
        }

        localStorage.setItem('accessToken', data.access_token);
        
        // Usar a URL de redirecionamento retornada pela API
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        } else {
            window.location.href = '/dashboard'; // Fallback
        }
    } catch (error) {
        console.error('Erro ao verificar código:', error);
        codeError.textContent = error.message || 'Erro ao verificar código. Tente novamente.';
        codeError.style.display = 'block';
        hideLoading(); // Esconder loading global em caso de erro
    } finally {
        hideModalLoading();
    }
}

// Função para testar rota protegida
async function testProtectedRoute() {
    try {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            throw new Error('Token não encontrado');
        }

        const response = await fetch(`${API_URL}/api/protected`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Erro ao acessar rota protegida');
        }

        const data = await response.json();
        console.log('Resposta da rota protegida:', data);
        return data;
    } catch (error) {
        console.error('Erro ao acessar rota protegida:', error);
        throw error;
    }
}

// Funções de autenticação
function handleGoogleLogin() {
    window.location.href = `${API_URL}/api/auth/google`;
}

function handlePhoneLogin() {
    showModal();
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Configurar botão de autenticação por telefone
    const phoneAuthButton = document.querySelector('.btn-phone');
    if (phoneAuthButton) {
        phoneAuthButton.addEventListener('click', showModal);
    }

    // Configurar botão de fechar modal
    const modalClose = document.querySelector('.modal-close');
    if (modalClose) {
        modalClose.addEventListener('click', hideModal);
    }

    // Fechar modal ao clicar fora
    window.addEventListener('click', (event) => {
        const modal = document.getElementById('smsModal');
        if (event.target === modal) {
            hideModal();
        }
    });

    // Configurar envio do formulário ao pressionar Enter
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                requestSmsCode();
            }
        });
    }

    const codeInput = document.getElementById('code');
    if (codeInput) {
        codeInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                verifyPhoneCode();
            }
        });
    }
}); 