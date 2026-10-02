// =========================
// ELEMENTOS DO HTML
// =========================

// CONTEÚDOS
const conteudoCadastrar = document.getElementById("conteudo-cadastrar")
const conteudoListar = document.getElementById("conteudo-listar")
const conteudoEditar = document.getElementById("conteudo-editar")
const conteudoStatus = document.getElementById("conteudo-status")

const listaMotoristas = document.getElementById("lista-motoristas")

// AÇÕES
const menuCadastrar = document.getElementById("menu-cadastrar")
const menuListar = document.getElementById("menu-listar")
const formularioCadastro = document.getElementById("form-motorista")
const menuEditar = document.getElementById("menu-editar")
const botaoBuscarMotorista = document.getElementById("btn-buscar-motorista")
const formularioEditar = document.getElementById("form-editar-motorista")
const menuStatus = document.getElementById("menu-status")
const botaoAtivarMotorista = document.getElementById("btn-ativar-motorista")
const botaoInativarMotorista = document.getElementById("btn-inativar-motorista")




// =========================
// FUNÇÕES
// =========================

function mostrarCadastro() {

    conteudoCadastrar.style.display = "block"

    conteudoListar.style.display = "none"
    conteudoEditar.style.display = "none"
    conteudoStatus.style.display = "none"

}


async function cadastrarMotorista(evento) {

    evento.preventDefault()

    const matricula = document.getElementById("matricula").value
    const nome = document.getElementById("nome").value

    const dados = {
        matricula: matricula,
        nome: nome
    }

    const resposta = await fetch("/api/motoristas", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(dados)
    })

    const resultado = await resposta.json()

    if (resposta.ok) {
    document.getElementById("resposta-cadastro").textContent = resultado.mensagem
    } else {
        document.getElementById("resposta-cadastro").textContent = resultado.erro
    }
    }

function mostrarListar() {

    conteudoCadastrar.style.display = "none"

    conteudoListar.style.display = "block"

    conteudoEditar.style.display = "none"
    conteudoStatus.style.display = "none"

}

async function listarMotoristas() {

    const resposta = await fetch("/api/motoristas")

    const motoristas = await resposta.json()

    listaMotoristas.innerHTML = ""

        for (let motorista of motoristas) {

        let status

        if (motorista.ativo) {
            status = "Ativo"
        } else {
            status = "Inativo"
        }

            listaMotoristas.innerHTML += `
        <div class="motorista-item">

            <span class="motorista-id">
                #${motorista.id}
            </span>

            <span class="motorista-nome">
                ${motorista.nome}
            </span>

            <span class="motorista-matricula">
                Matrícula ${motorista.matricula}
            </span>

            <span class="motorista-status">
                ${status}
            </span>

        </div>
    `
    }

    }



function mostrarEditar() {

    conteudoCadastrar.style.display = "none"
    conteudoListar.style.display = "none"
    conteudoEditar.style.display = "block"
    conteudoStatus.style.display = "none"

}

async function buscarMotorista() {

    const id = document.getElementById("editar-id").value

    const resposta = await fetch(`/api/motoristas/${id}`)

    const motorista = await resposta.json()

    document.getElementById("editar-matricula").value = motorista.matricula
    document.getElementById("editar-nome").value = motorista.nome

}

async function atualizarMotorista(evento) {

    evento.preventDefault()

    const id = document.getElementById("editar-id").value
    const matricula = document.getElementById("editar-matricula").value
    const nome = document.getElementById("editar-nome").value

    const dados = {
        matricula: matricula,
        nome: nome
    }

    const resposta = await fetch(`/api/motoristas/${id}`, {
        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(dados)
    })

    const resultado = await resposta.json()

    document.getElementById("resposta-editar").textContent = resultado.mensagem

}

function mostrarStatus() {

    conteudoCadastrar.style.display = "none"
    conteudoListar.style.display = "none"
    conteudoEditar.style.display = "none"
    conteudoStatus.style.display = "block"

}


async function atualizarStatusMotorista(ativo) {

    const id = document.getElementById("status-id").value

    const dados = {
        ativo: ativo
    }

    const resposta = await fetch(`/api/motoristas/${id}/status`, {
        method: "PATCH",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(dados)
    })

    const resultado = await resposta.json()

    document.getElementById("resposta-status").textContent = resultado.mensagem

}

// =========================
// EVENTOS
// =========================

menuCadastrar.addEventListener("click", mostrarCadastro)

formularioCadastro.addEventListener("submit", cadastrarMotorista)

menuListar.addEventListener("click", mostrarListar)

menuListar.addEventListener("click", listarMotoristas)

menuEditar.addEventListener("click", mostrarEditar)

botaoBuscarMotorista.addEventListener("click", buscarMotorista)

formularioEditar.addEventListener("submit", atualizarMotorista)

menuStatus.addEventListener("click", mostrarStatus)

botaoAtivarMotorista.addEventListener("click", function () {
    atualizarStatusMotorista(true)
})

botaoInativarMotorista.addEventListener("click", function () {
    atualizarStatusMotorista(false)
})


// =========================
// INICIALIZAÇÃO
// =========================

mostrarCadastro()